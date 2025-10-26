#!/usr/bin/env python3
"""
Quiz Socket.IO Namespace Handler
Handles real-time quiz sessions via Socket.IO /quiz namespace
"""

import os
import json
import uuid
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from flask import request
from flask_socketio import emit, join_room, leave_room

# Setup logging
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(backend_dir, "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "quiz_socket.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import teacher module for quiz questions
try:
    from backend.trainer.teacher import LESSONS, get_all_quiz_questions
except ImportError:
    from teacher import LESSONS, get_all_quiz_questions

# Session storage (in-memory with TTL)
sessions: Dict[str, Dict[str, Any]] = {}
SESSION_TTL = timedelta(hours=2)  # 2 hour TTL
MAX_QUESTIONS = int(os.environ.get('QUIZ_MAX_QUESTIONS', 10))

# Diagnostics log path
DIAGNOSTICS_DIR = os.path.join(backend_dir, "diagnostics")
os.makedirs(DIAGNOSTICS_DIR, exist_ok=True)
QUIZ_SESSIONS_LOG = os.path.join(DIAGNOSTICS_DIR, "quiz_sessions.log")


def log_session_event(session_id: str, event: str, data: Dict[str, Any]):
    """Log quiz session events to diagnostics/quiz_sessions.log"""
    try:
        # Check file size and rotate if > 10MB
        if os.path.exists(QUIZ_SESSIONS_LOG):
            file_size = os.path.getsize(QUIZ_SESSIONS_LOG)
            if file_size > 10 * 1024 * 1024:  # 10MB
                # Rotate: move current to .old and start fresh
                old_log = QUIZ_SESSIONS_LOG + '.old'
                if os.path.exists(old_log):
                    os.remove(old_log)
                os.rename(QUIZ_SESSIONS_LOG, old_log)
        
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'session_id': session_id,
            'event': event,
            'data': {k: v for k, v in data.items() if k not in ['userId', 'email']}  # No PII
        }
        with open(QUIZ_SESSIONS_LOG, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    except Exception as e:
        logger.warning(f"Failed to log session event: {e}")


def cleanup_expired_sessions():
    """Remove expired sessions"""
    now = datetime.utcnow()
    expired = [
        sid for sid, session in sessions.items()
        if now - session['created_at'] > SESSION_TTL
    ]
    for sid in expired:
        del sessions[sid]
        logger.info(f"Cleaned up expired session: {sid}")


def get_or_create_session(user_id: str, topic: str, existing_session_id: Optional[str] = None) -> Dict[str, Any]:
    """Get existing session or create new one"""
    cleanup_expired_sessions()
    
    # Try to resume existing session
    if existing_session_id and existing_session_id in sessions:
        session = sessions[existing_session_id]
        # Check if expired
        if datetime.utcnow() - session['created_at'] <= SESSION_TTL:
            logger.info(f"Resuming session: {existing_session_id}")
            return session
        else:
            logger.info(f"Session expired: {existing_session_id}")
            del sessions[existing_session_id]
    
    # Create new session
    session_id = str(uuid.uuid4())
    
    # Get quiz questions for topic
    if topic in LESSONS:
        questions = LESSONS[topic]['quiz']
    else:
        # Fallback to mixed questions
        questions = get_all_quiz_questions()
    
    # Limit to MAX_QUESTIONS
    questions = questions[:MAX_QUESTIONS]
    
    session = {
        'session_id': session_id,
        'user_id': user_id,
        'topic': topic,
        'questions': questions,
        'current_index': 0,
        'total': 0,
        'correct_count': 0,
        'wrong_count': 0,
        'history': [],
        'created_at': datetime.utcnow(),
        'last_activity': datetime.utcnow()
    }
    
    sessions[session_id] = session
    log_session_event(session_id, 'session_created', {'topic': topic, 'question_count': len(questions)})
    logger.info(f"Created new session: {session_id} for topic: {topic}")
    
    return session


def score_answer(choice_index: int, answer_index: int) -> tuple[int, bool]:
    """
    Score an answer: +10 for correct, -10 for wrong
    Returns (delta, is_correct)
    """
    if choice_index == -1:  # No answer / timeout
        return (-10, False)
    
    is_correct = choice_index == answer_index
    delta = 10 if is_correct else -10
    return (delta, is_correct)


def register_quiz_socketio_handlers(socketio):
    """Register Socket.IO handlers for /quiz namespace"""
    
    @socketio.on('connect', namespace='/quiz')
    def handle_connect(auth):
        """Handle client connection to /quiz namespace"""
        logger.info(f"Client connected to /quiz namespace: {request.sid}")
        emit('connected', {'namespace': '/quiz', 'sid': request.sid})
    
    @socketio.on('disconnect', namespace='/quiz')
    def handle_disconnect():
        """Handle client disconnection"""
        logger.info(f"Client disconnected from /quiz namespace: {request.sid}")
    
    @socketio.on('quiz:join', namespace='/quiz')
    def handle_join(data):
        """Handle quiz session join/init"""
        try:
            user_id = data.get('userId', 'anonymous')
            topic = data.get('topic', 'suspicious_link')
            existing_session_id = data.get('sessionId')
            
            # Validate topic
            if topic not in LESSONS:
                logger.warning(f"Invalid topic: {topic}, using mixed questions")
            
            # Get or create session
            session = get_or_create_session(user_id, topic, existing_session_id)
            
            # Join room for this session
            join_room(session['session_id'])
            
            # Emit initialization
            emit('quiz:init', {
                'sessionId': session['session_id'],
                'userId': user_id,
                'topic': topic,
                'totalQuestions': len(session['questions'])
            })
            
            log_session_event(session['session_id'], 'join', {'topic': topic})
            
            # Send first question if available
            if session['current_index'] < len(session['questions']):
                send_question(session['session_id'])
            
        except Exception as e:
            logger.error(f"Error in quiz:join: {e}", exc_info=True)
            emit('quiz:error', {'message': str(e)})
    
    @socketio.on('quiz:answer', namespace='/quiz')
    def handle_answer(data):
        """Handle answer submission"""
        try:
            logger.info(f"quiz:answer - Received: {data}")
            session_id = data.get('sessionId')
            qid = data.get('qid')
            choice_index = data.get('choiceIndex')
            
            if not session_id or session_id not in sessions:
                logger.warning(f"quiz:answer - Invalid session: {session_id}")
                emit('quiz:error', {'message': 'Invalid session'})
                return
            
            session = sessions[session_id]
            
            # Throttle: check if already answered this question
            if qid in [h['qid'] for h in session['history']]:
                logger.warning(f"Duplicate answer for qid {qid} in session {session_id}")
                return
            
            # Find current question by qid or by last sent index
            current_q = None
            # current_index points to next question, so last sent is current_index - 1
            last_sent_index = session['current_index'] - 1
            
            for i, q in enumerate(session['questions']):
                if q.get('qid') == qid or (qid is None and i == last_sent_index):
                    current_q = q
                    break
            
            if not current_q:
                emit('quiz:error', {'message': 'Question not found'})
                return
            
            # Validate choice_index
            if choice_index < -1 or choice_index >= len(current_q['options']):
                emit('quiz:error', {'message': 'Invalid choice index'})
                return
            
            # Score answer
            answer_index = current_q['answer_index']
            delta, is_correct = score_answer(choice_index, answer_index)
            
            # Update session
            session['total'] += delta
            if is_correct:
                session['correct_count'] += 1
            else:
                session['wrong_count'] += 1
            
            session['history'].append({
                'qid': qid,
                'choice_index': choice_index,
                'correct': is_correct,
                'delta': delta
            })
            
            session['last_activity'] = datetime.utcnow()
            
            # Emit score update
            logger.info(f"quiz:answer - Emitting score update for session {session_id}, qid {qid}, correct={is_correct}, total={session['total']}")
            emit('quiz:score:update', {
                'qid': qid,
                'correct': is_correct,
                'delta': delta,
                'total': session['total']
            }, room=session_id)
            
            log_session_event(session_id, 'answer', {
                'qid': qid,
                'correct': is_correct,
                'delta': delta
            })
            
        except Exception as e:
            logger.error(f"Error in quiz:answer: {e}", exc_info=True)
            emit('quiz:error', {'message': str(e)})
    
    @socketio.on('quiz:next', namespace='/quiz')
    def handle_next(data):
        """Handle request for next question"""
        try:
            logger.info(f"quiz:next - Received request: {data}")
            session_id = data.get('sessionId')
            
            if not session_id or session_id not in sessions:
                logger.warning(f"quiz:next - Invalid session: {session_id}, available sessions: {list(sessions.keys())[:5]}")
                emit('quiz:error', {'message': 'Invalid session'})
                return
            
            session = sessions[session_id]
            logger.info(f"quiz:next - Session {session_id}, current_index={session['current_index']}, total={len(session['questions'])}")
            
            # Check if quiz is complete
            if session['current_index'] >= len(session['questions']):
                # Quiz complete
                logger.info(f"quiz:next - Quiz complete for session {session_id}")
                emit('quiz:complete', {
                    'total': session['total'],
                    'correctCount': session['correct_count'],
                    'wrongCount': session['wrong_count'],
                    'history': session['history']
                })
                
                log_session_event(session_id, 'complete', {
                    'total': session['total'],
                    'correct_count': session['correct_count'],
                    'wrong_count': session['wrong_count']
                })
                
                # Cleanup session after a delay
                # Keep in memory for TTL in case of reconnection
                return
            
            # Send next question
            logger.info(f"quiz:next - Sending question {session['current_index']} for session {session_id}")
            send_question(session_id)
            
        except Exception as e:
            logger.error(f"Error in quiz:next: {e}", exc_info=True)
            emit('quiz:error', {'message': str(e)})
    
    @socketio.on('quiz:leave', namespace='/quiz')
    def handle_leave(data):
        """Handle client leaving quiz"""
        try:
            session_id = data.get('sessionId')
            if session_id:
                leave_room(session_id)
                logger.info(f"Client left session: {session_id}")
        except Exception as e:
            logger.error(f"Error in quiz:leave: {e}", exc_info=True)


def send_question(session_id: str):
    """Send current question to client"""
    if session_id not in sessions:
        logger.warning(f"send_question - Session {session_id} not found")
        return
    
    session = sessions[session_id]
    
    if session['current_index'] >= len(session['questions']):
        logger.warning(f"send_question - No more questions (index {session['current_index']} >= {len(session['questions'])})")
        return
    
    question = session['questions'][session['current_index']]
    
    # Assign qid if not present
    if 'qid' not in question:
        question['qid'] = f"q{session['current_index']}"
    
    logger.info(f"send_question - Sending question {session['current_index']} with qid {question['qid']} to session {session_id}")
    
    # Emit question
    emit('quiz:question', {
        'qid': question['qid'],
        'index': session['current_index'],
        'text': question['question'],
        'options': question['options'],
        'answer_index': question['answer_index'],  # For frontend validation
        'seconds': None  # Optional timer, can be added later
    }, room=session_id)
    
    # Increment index AFTER sending
    old_index = session['current_index']
    session['current_index'] += 1
    session['last_activity'] = datetime.utcnow()
    
    logger.info(f"send_question - Incremented index from {old_index} to {session['current_index']}")
    
    log_session_event(session_id, 'question_sent', {
        'qid': question['qid'],
        'index': old_index
    })

