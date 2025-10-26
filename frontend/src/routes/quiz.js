import React, { useState, useEffect, useRef } from 'react'
import '../styles/quiz.css'
import fisherman from '../styles/images/fishing1.png'
import FishHook from '../styles/images/fishHook.png'
import FishA from '../styles/images/fishA.png'
import FishB from '../styles/images/fishB.png'
import FishC from '../styles/images/fishC.png'
//Decoration Images
import crab from '../styles/images/assets/crab.png'
import dolphi from '../styles/images/assets/dolphi .png'
import octo from '../styles/images/assets/octo.png'
import seahorse from '../styles/images/assets/seahorse.png'
import squid from '../styles/images/assets/squid.png'
import star from '../styles/images/assets/star.png'
import turtle from '../styles/images/assets/turtle.png'
import whale from '../styles/images/assets/whale.png'

import { createQuizSocket, setupReconnectHandler } from '../quiz/socket'

export default function Quiz() {
    const fishermanRef = useRef(null);
    const socketRef = useRef(null);
    const sessionIdRef = useRef(null);
    const completedRef = useRef(false);
    const nextQuestionTimeoutRef = useRef(null);
    const [anchor, setAnchor] = useState({ x: 100, y: 100 });
    const [socket, setSocket] = useState(null);
    const [sessionId, setSessionId] = useState(null);
    const [isConnected, setIsConnected] = useState(false);

    // Socket quiz state
    const [userId, setUserId] = useState('anonymous');
    const [topic, setTopic] = useState('suspicious_link');
    const [currentQuestion, setCurrentQuestion] = useState(null);
    const [isAnswerLocked, setIsAnswerLocked] = useState(false);
    const [feedback, setFeedback] = useState(null);
    const [totalQuestions, setTotalQuestions] = useState(10);
    const [currentQuestionNum, setCurrentQuestionNum] = useState(0);
    const [correctCount, setCorrectCount] = useState(0);
    const [score, setScore] = useState(0);
    const [completed, setCompleted] = useState(false);
    const [results, setResults] = useState(null);

    // Get userId from session/localStorage if available
    useEffect(() => {
        const storedUserId = localStorage.getItem('userId') || sessionStorage.getItem('userId');
        if (storedUserId) {
            setUserId(storedUserId);
        }

        const params = new URLSearchParams(window.location.search);
        const topicParam = params.get('topic');
        if (topicParam && ['suspicious_link', 'abnormal_email', 'random_email_address'].includes(topicParam)) {
            setTopic(topicParam);
        }
    }, []);

    // Initialize socket connection (only once)
    useEffect(() => {
        if (window.__ENABLE_QUIZ__ === false) return;

        // Prevent multiple socket instances
        if (socketRef.current) {
            console.log('[Quiz] Socket already exists, skipping re-initialization');
            return;
        }

        console.log('[Quiz] Creating new socket connection...');
        const socketInstance = createQuizSocket();
        setSocket(socketInstance);
        socketRef.current = socketInstance;

        socketInstance.on('connect', () => {
            console.log('[Quiz] ✅ Connected to quiz namespace');
            setIsConnected(true);
            socketInstance.emit('quiz:join', { userId, topic });
        });

        // Use refs for reconnect handler to avoid stale closures
        setupReconnectHandler(socketInstance, sessionIdRef.current, userId, topic);

        socketInstance.on('quiz:init', (data) => {
            console.log('[Quiz] Initialized:', data);
            setSessionId(data.sessionId);
            sessionIdRef.current = data.sessionId;
            setTotalQuestions(data.totalQuestions || 10);
            if (window.__quiz_onEvent) {
                window.__quiz_onEvent('init', data);
            }
        });

        socketInstance.on('quiz:question', (data) => {
            console.log('[Quiz] Question received:', data);

            // Only update if this is a different question (check by qid or index)
            if (currentQuestion && currentQuestion.qid === data.qid) {
                console.log('[Quiz] Ignoring duplicate question:', data.qid);
                return;
            }

            setCurrentQuestion(data);
            setIsAnswerLocked(false);
            setFeedback(null);
            setSelectedFish(null);
            setCurrentQuestionNum(data.index + 1);

            // Reset fish states for new question
            setFishStates({ fishA: 'playing1', fishB: 'playing1', fishC: 'playing1' });

            // Update question text via CSS variable
            const innerBox = document.querySelector('.inner-white-box');
            if (innerBox) {
                innerBox.style.setProperty('--quiz-question', `"${data.text}"`);
            }

            if (window.__quiz_onEvent) {
                window.__quiz_onEvent('question', data);
            }
        });

        socketInstance.on('quiz:score:update', (data) => {
            console.log('[Quiz] Score update received:', data);
            setScore(data.total);
            setFeedback({
                qid: data.qid,
                correct: data.correct,
                delta: data.delta,
                selectedIndex: currentQuestion ? currentQuestion.options.findIndex((_, idx) => {
                    // Find which fish was selected
                    return (selectedFish === 'fishA' && idx === 0) ||
                        (selectedFish === 'fishB' && idx === 1) ||
                        (selectedFish === 'fishC' && idx === 2);
                }) : -1
            });
            if (data.correct) {
                setCorrectCount(prev => prev + 1);
            }

            if (window.__quiz_onEvent) {
                window.__quiz_onEvent('score', data);
            }

            // Auto-request next question after showing feedback
            // Clear any existing timeout to prevent duplicates
            if (nextQuestionTimeoutRef.current) {
                clearTimeout(nextQuestionTimeoutRef.current);
            }

            console.log('[Quiz] Scheduling next question request in 3 seconds...');
            console.log('[Quiz] Current socket state:', {
                hasSocket: !!socketRef.current,
                connected: socketRef.current?.connected,
                sessionId: sessionIdRef.current
            });

            nextQuestionTimeoutRef.current = setTimeout(() => {
                // Use refs to get current values (not stale closure)
                const currentSocket = socketRef.current;
                const currentSession = sessionIdRef.current;
                const isComplete = completedRef.current;

                console.log('[Quiz] Timeout fired! Checking state:', {
                    hasSocket: !!currentSocket,
                    sessionId: currentSession,
                    completed: isComplete,
                    socketConnected: currentSocket?.connected
                });

                if (!isComplete && currentSocket && currentSession && currentSocket.connected) {
                    console.log('[Quiz] ✅ Requesting next question for session:', currentSession);
                    currentSocket.emit('quiz:next', { sessionId: currentSession });
                } else {
                    console.error('[Quiz] ❌ Not requesting next question:', {
                        completed: isComplete,
                        hasSocket: !!currentSocket,
                        sessionId: currentSession,
                        socketConnected: currentSocket?.connected
                    });
                }
                nextQuestionTimeoutRef.current = null;
            }, 3000); // 3 seconds to show feedback
        });

        socketInstance.on('quiz:complete', (data) => {
            console.log('[Quiz] Complete:', data);
            setCompleted(true);
            completedRef.current = true;
            setResults(data);
            setIsAnswerLocked(true);

            if (window.__quiz_onEvent) {
                window.__quiz_onEvent('complete', data);
            }
        });

        socketInstance.on('quiz:error', (data) => {
            console.error('[Quiz] Error:', data);
        });

        return () => {
            // Clear timeout on cleanup
            if (nextQuestionTimeoutRef.current) {
                clearTimeout(nextQuestionTimeoutRef.current);
                nextQuestionTimeoutRef.current = null;
            }

            // Only disconnect on unmount, not on dependency changes
            // Keep socket alive during the quiz session
        };
    }, []); // Empty deps - only run once on mount

    // Update anchor from fisherman image
    const updateAnchorFromImage = () => {
        const el = fishermanRef.current;
        if (!el) return;
        const rect = el.getBoundingClientRect();
        const pixelAnchor = { x: 786, y: 233 };
        const naturalW = el.naturalWidth || rect.width;
        const naturalH = el.naturalHeight || rect.height;
        const anchorX = rect.left + (pixelAnchor.x / naturalW) * rect.width;
        const anchorY = rect.top + (pixelAnchor.y / naturalH) * rect.height;
        setAnchor({
            x: Math.round(anchorX),
            y: Math.round(anchorY)
        });
    };

    useEffect(() => {
        updateAnchorFromImage();
        window.addEventListener('resize', updateAnchorFromImage);
        return () => window.removeEventListener('resize', updateAnchorFromImage);
    }, []);

    // Fish state for animations
    const [fishStates, setFishStates] = useState({
        fishA: 'playing1',
        fishB: 'playing1',
        fishC: 'playing1'
    });
    const [selectedFish, setSelectedFish] = useState(null);

    // Handle fish selection (maps to quiz answer)
    const handleFishSelect = (fishKey, optionIndex) => {
        if (isAnswerLocked || completed || !currentQuestion) return;

        // Use refs to get current socket (not stale closure)
        const currentSocket = socketRef.current;
        const currentSessionId = sessionIdRef.current;

        if (!currentSocket || !currentSocket.connected) {
            console.error('[Quiz] Cannot send answer - socket not connected:', {
                hasSocket: !!currentSocket,
                connected: currentSocket?.connected
            });
            return;
        }

        const currentQid = currentQuestion.qid;

        setSelectedFish(fishKey);
        setIsAnswerLocked(true);

        // Stop the selected fish
        setFishStates(prev => ({ ...prev, [fishKey]: 'stopped' }));

        // Send answer
        console.log('[Quiz] Sending answer:', {
            sessionId: currentSessionId,
            qid: currentQid,
            choiceIndex: optionIndex,
            socketConnected: currentSocket.connected
        });
        currentSocket.emit('quiz:answer', {
            sessionId: currentSessionId,
            qid: currentQid,
            choiceIndex: optionIndex
        });

        if (window.__quiz_onEvent) {
            window.__quiz_onEvent('answer', {
                qid: currentQid,
                choiceIndex: optionIndex
            });
        }

        // Note: Next question request is now handled in quiz:score:update handler
    };

    // Map fish to options
    const fishOptionMap = currentQuestion ? {
        fishA: { index: 0, option: currentQuestion.options[0] },
        fishB: { index: 1, option: currentQuestion.options[1] },
        fishC: { index: 2, option: currentQuestion.options[2] }
    } : null;

    // Determine feedback classes for each fish
    const getFishFeedbackClass = (fishKey, optionIndex) => {
        if (!feedback || feedback.qid !== currentQuestion?.qid) return '';

        const isSelected = selectedFish === fishKey;
        const isCorrectAnswer = currentQuestion?.answer_index === optionIndex;

        if (isSelected && feedback.correct) return 'correct';
        if (isSelected && !feedback.correct) return 'wrong';
        if (!isSelected && isCorrectAnswer && isAnswerLocked) return 'correct-answer'; // Show correct answer

        return '';
    };

    // Show loading if not connected or no question
    if (!isConnected || !currentQuestion) {
        return (
            <div className='quiz-scene'>
                <div className='white-box'>
                    <div className='inner-white-box'>
                        <h2 className='quiz-question'>
                            {!isConnected ? 'Connecting to quiz server...' : 'Waiting for question...'}
                        </h2>
                    </div>
                </div>
            </div>
        );
    }

    // Show completion screen
    if (completed && results) {
        return (
            <div className='quiz-scene'>
                <div className='white-box'>
                    <div className='inner-white-box'>
                        <h2 className='quiz-question'>Quiz Complete!</h2>
                        <p className='quiz-instructions'>
                            Score: {results.total} | Correct: {results.correctCount} | Wrong: {results.wrongCount}
                        </p>
                    </div>
                </div>
                <div className='top-right-panel'>
                    <div className='tracker-box score-box'>
                        <div className='tracker-label'>Final Score</div>
                        <div className='tracker-value'>{results.total}</div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className='quiz-scene'>
            {/* Question box */}
            <div className='white-box'>
                <div className='inner-white-box'>
                    <h2 className='quiz-question'>{currentQuestion.text}</h2>
                    <p className='quiz-instructions'>
                        {isAnswerLocked && feedback
                            ? (feedback.correct ? '✓ Correct! Loading next question...' : '✗ Wrong. Showing correct answer...')
                            : 'Click on the fish that represents the correct answer'}
                    </p>
                </div>
            </div>

            {/* Top-right trackers */}
            <div className='top-right-panel'>
                <div className='tracker-box correct-box'>
                    <div className='tracker-label'>Questions</div>
                    <div className='tracker-value'>{currentQuestionNum} / {totalQuestions}</div>
                </div>
                <div className='tracker-box score-box'>
                    <div className='tracker-label'>Score</div>
                    <div className='tracker-value'>{score}</div>
                </div>
            </div>
            {/* Quiz body with fish */}
            <div className='quiz-body'>
                <div className='quiz-midbar' />
                <div className='d-flex flex-row justify-content-between'>
                    <img
                        src={fisherman}
                        ref={fishermanRef}
                        alt="fisherman"
                        className='fisherman-image'
                        onLoad={updateAnchorFromImage}
                    />
                </div>
        <div className='quiz-body'>
            <div className='quiz-midbar' />
            <div className='d-flex flex-row justify-content-between'>
                <img 
                    src={fisherman}
                    ref={fishermanRef} 
                    alt="fisherman" 
                    className='fisherman-image'
                    onLoad={updateAnchorFromImage}
                    draggable={false}
                    onDragStart={(e) => e.preventDefault()}
                />

                <img
                    src={crab}
                    alt="crab"
                    className="crab-image"
                    style={{
                        '--crab-width': '120px',
                        '--crab-height': '80px',
                        '--crab-top': '350px',
                        '--crab-left': '600px'
                    }}
                />
                <img
                    src={dolphi}
                    alt="dolphi"
                    className="dolphi-image"
                    style={{
                        '--dolphi-width': '120px',
                        '--dolphi-height': '80px',
                        '--dolphi-top': '360px',
                        '--dolphi-left': '300px'
                    }}
                />
                <img
                    src={octo}
                    alt="octo"
                    className="octo-image"
                    style={{
                        '--octo-width': '120px',
                        '--octo-height': '80px',
                        '--octo-top': '400px',
                        '--octo-left': '500px'
                    }}
                />
                <img
                    src={seahorse}
                    alt="seahorse"
                    className="seahorse-image"
                    style={{
                        '--seahorse-width': '120px',
                        '--seahorse-height': '80px',
                        '--seahorse-top': '200px',
                        '--seahorse-left': '500px'
                    }}
                />
                <img
                    src={squid}
                    alt="squid"
                    className="squid-image"
                    style={{
                        '--squid-width': '120px',
                        '--squid-height': '80px',
                        '--squid-top': '300px',
                        '--squid-left': '500px'
                    }}
                />
                <img
                    src={star}
                    alt="star"
                    className="star-image"
                    style={{
                        '--star-width': '120px',
                        '--star-height': '80px',
                        '--star-top': '300px',
                        '--star-left': '500px'
                    }}
                />
                <img
                    src={turtle}
                    alt="turtle"
                    className="turtle-image"
                    style={{
                        '--turtle-width': '120px',
                        '--turtle-height': '80px',
                        '--turtle-top': '300px',
                        '--turtle-left': '500px'
                    }}
                />
                <img
                    src={whale}
                    alt="whale"
                    className="whale-image"
                    style={{
                        '--whale-width': '120px',
                        '--whale-height': '80px',
                        '--whale-top': '300px',
                        '--whale-left': '500px'
                    }}
                />
            </div>
                {/* Fish A - Option 0 */}
                <button
                    type="button"
                    className={`fishiesA ${fishStates.fishA} ${selectedFish === 'fishA' ? 'selected' : ''} ${isAnswerLocked ? 'locked' : ''} ${getFishFeedbackClass('fishA', 0)}`}
                    onClick={() => handleFishSelect('fishA', 0)}
                    disabled={isAnswerLocked}
                    aria-pressed={selectedFish === 'fishA'}
                    title={fishOptionMap?.fishA.option}
                >
                    {fishOptionMap?.fishA.option || 'Fish A'}
                    {feedback && feedback.qid === currentQuestion?.qid && selectedFish === 'fishA' && (
                        <span className="feedback-indicator">{feedback.correct ? '✓' : '✗'}</span>
                    )}
                </button>

                {/* Fish B - Option 1 */}
                <button
                    type="button"
                    className={`fishiesB ${fishStates.fishB} ${selectedFish === 'fishB' ? 'selected' : ''} ${isAnswerLocked ? 'locked' : ''} ${getFishFeedbackClass('fishB', 1)}`}
                    onClick={() => handleFishSelect('fishB', 1)}
                    disabled={isAnswerLocked}
                    aria-pressed={selectedFish === 'fishB'}
                    title={fishOptionMap?.fishB.option}
                >
                    {fishOptionMap?.fishB.option || 'Fish B'}
                    {feedback && feedback.qid === currentQuestion?.qid && selectedFish === 'fishB' && (
                        <span className="feedback-indicator">{feedback.correct ? '✓' : '✗'}</span>
                    )}
                </button>

                {/* Fish C - Option 2 */}
                <button
                    type="button"
                    className={`fishiesC ${fishStates.fishC} ${selectedFish === 'fishC' ? 'selected' : ''} ${isAnswerLocked ? 'locked' : ''} ${getFishFeedbackClass('fishC', 2)}`}
                    onClick={() => handleFishSelect('fishC', 2)}
                    disabled={isAnswerLocked}
                    aria-pressed={selectedFish === 'fishC'}
                    title={fishOptionMap?.fishC.option}
                >
                    {fishOptionMap?.fishC.option || 'Fish C'}
                    {feedback && feedback.qid === currentQuestion?.qid && selectedFish === 'fishC' && (
                        <span className="feedback-indicator">{feedback.correct ? '✓' : '✗'}</span>
                    )}
                </button>
            </div>

            <CursorFollowImage anchor={anchor} />
        </div>
    )
}

function CursorFollowImage({ anchor }) {
    const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

    useEffect(() => {
        const handleMouseMove = (event) => {
            setMousePosition({ x: event.clientX, y: event.clientY });
        };

        window.addEventListener('mousemove', handleMouseMove);
        return () => {
            window.removeEventListener('mousemove', handleMouseMove);
        };
    }, []);

    const svgStyle = {
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        pointerEvents: 'none',
        zIndex: 2
    }

    return (
        <div className="quiz-container">
            <svg style={svgStyle}>
                <line
                    x1={mousePosition.x}
                    y1={mousePosition.y}
                    x2={anchor.x}
                    y2={anchor.y}
                    stroke="#000"
                    strokeWidth="1"
                />
            </svg>
        </div>
    );
}
