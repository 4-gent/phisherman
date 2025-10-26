#!/usr/bin/env python3
"""
Teacher Agent - Safe Phishing Awareness Training
Provides educational lessons on phishing detection without generating harmful content.
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
import requests

# Setup logging
# Get backend directory (one level up from trainer/)
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(backend_dir, "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "trainer_teacher.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Lessons data for three topics
LESSONS = {
    "suspicious_link": {
        "lesson_id": "LESSON_SUSP_LINK_001",
        "title": "Identifying Suspicious Links",
        "bullets": [
            "Hover over links to check destination URLs",
            "Watch for misspelled domain names",
            "Avoid shortened URLs from unknown services",
            "Verify links before clicking"
        ],
        "quiz": [
            {
                "question": "What should you do before clicking a suspicious link?",
                "options": ["hover", "click", "ignore"],
                "answer_index": 0
            },
            {
                "question": "Misspelled domains are a warning sign?",
                "options": ["true", "false", "maybe"],
                "answer_index": 0
            },
            {
                "question": "Shortened URLs are always safe?",
                "options": ["yes", "no", "sometimes"],
                "answer_index": 1
            },
            {
                "question": "IP addresses in links are suspicious?",
                "options": ["yes", "no", "rarely"],
                "answer_index": 0
            },
            {
                "question": "Always verify links through official channels?",
                "options": ["yes", "no", "optional"],
                "answer_index": 0
            },
            {
                "question": "HTTP links are safer than HTTPS?",
                "options": ["yes", "no", "same"],
                "answer_index": 1
            },
            {
                "question": "Links in unexpected emails need verification?",
                "options": ["yes", "no", "maybe"],
                "answer_index": 0
            },
            {
                "question": "Similar-looking domains are safe?",
                "options": ["yes", "no", "usually"],
                "answer_index": 1
            },
            {
                "question": "Type important URLs directly instead of clicking?",
                "options": ["yes", "no", "depends"],
                "answer_index": 0
            },
            {
                "question": "When in doubt, verify the sender?",
                "options": ["yes", "no", "optional"],
                "answer_index": 0
            }
        ]
    },
    "abnormal_email": {
        "lesson_id": "LESSON_ABN_EMAIL_002",
        "title": "Recognizing Abnormal Email Patterns",
        "bullets": [
            "Check sender address matches display name",
            "Watch for poor grammar and spelling errors",
            "Be suspicious of urgent unexpected requests",
            "Verify emails through alternative channels"
        ],
        "quiz": [
            {
                "question": "Sender address should match display name?",
                "options": ["yes", "no", "maybe"],
                "answer_index": 0
            },
            {
                "question": "Poor grammar in professional emails is normal?",
                "options": ["yes", "no", "sometimes"],
                "answer_index": 1
            },
            {
                "question": "Generic greetings are suspicious?",
                "options": ["yes", "no", "rarely"],
                "answer_index": 0
            },
            {
                "question": "Inconsistent branding is a red flag?",
                "options": ["yes", "no", "maybe"],
                "answer_index": 0
            },
            {
                "question": "Unexpected urgent emails need verification?",
                "options": ["yes", "no", "optional"],
                "answer_index": 0
            },
            {
                "question": "Reply-to address differences are normal?",
                "options": ["yes", "no", "sometimes"],
                "answer_index": 1
            },
            {
                "question": "Check email headers for routing info?",
                "options": ["yes", "no", "optional"],
                "answer_index": 0
            },
            {
                "question": "Report suspicious emails to IT security?",
                "options": ["yes", "no", "maybe"],
                "answer_index": 0
            },
            {
                "question": "Contact sender through alternative channels?",
                "options": ["yes", "no", "depends"],
                "answer_index": 0
            },
            {
                "question": "Unusual timing is suspicious?",
                "options": ["yes", "no", "rarely"],
                "answer_index": 0
            }
        ]
    },
    "random_email_address": {
        "lesson_id": "LESSON_RAND_EMAIL_003",
        "title": "Dealing with Suspicious Email Addresses",
        "bullets": [
            "Verify addresses match organization's official domain",
            "Be skeptical of random character combinations",
            "Watch for similar-looking domains with misspellings",
            "Check official website for legitimate contact addresses"
        ],
        "quiz": [
            {
                "question": "Random character combinations are suspicious?",
                "options": ["yes", "no", "maybe"],
                "answer_index": 0
            },
            {
                "question": "Personal emails claiming to be businesses are safe?",
                "options": ["yes", "no", "sometimes"],
                "answer_index": 1
            },
            {
                "question": "Similar-looking domains need verification?",
                "options": ["yes", "no", "optional"],
                "answer_index": 0
            },
            {
                "question": "Business emails from free services are normal?",
                "options": ["yes", "no", "rarely"],
                "answer_index": 1
            },
            {
                "question": "Check organization's official website for addresses?",
                "options": ["yes", "no", "optional"],
                "answer_index": 0
            },
            {
                "question": "Misspelled domains are safe?",
                "options": ["yes", "no", "sometimes"],
                "answer_index": 1
            },
            {
                "question": "Numbers before @ symbol in business emails are normal?",
                "options": ["yes", "no", "rarely"],
                "answer_index": 1
            },
            {
                "question": "Never respond to unverified addresses?",
                "options": ["yes", "no", "maybe"],
                "answer_index": 0
            },
            {
                "question": "Report suspicious addresses to email providers?",
                "options": ["yes", "no", "optional"],
                "answer_index": 0
            },
            {
                "question": "When unsure, contact through official website?",
                "options": ["yes", "no", "depends"],
                "answer_index": 0
            }
        ]
    }
}

def build_lesson_payload(topic: str) -> Optional[Dict[str, Any]]:
    """Build lesson payload for a given topic"""
    if topic not in LESSONS:
        return None
    return LESSONS[topic].copy()

def is_harmful_request(text: str) -> bool:
    """Check if request tries to generate phishing content or harmful content"""
    harmful_patterns = [
        "generate phishing",
        "create phishing",
        "make phishing",
        "phishing template",
        "phishing email",
        "impersonate",
        "spoof",
        "steal credentials",
        "fake email",
        "malicious link",
        "actual phishing",
        "real phishing",
        "send phishing",
        "click here to",
        "http://",
        "https://",
        ".com",
        ".org",
        "steal",
        "hack"
    ]
    
    text_lower = text.lower()
    for pattern in harmful_patterns:
        if pattern in text_lower:
            return True
    return False

def paraphrase_with_llm(text: str) -> Optional[str]:
    """Optionally paraphrase lesson text using ASI-1 API if key is available"""
    api_key = os.getenv("ASI1_API_KEY", "")
    base_url = os.getenv("ASI1_BASE_URL", "https://api.asi1.ai/v1")
    
    if not api_key:
        return None
    
    try:
        # Simple paraphrase request - only clarify/paraphrase, no content generation
        prompt = f"Please paraphrase the following educational text in a clear, concise way without adding examples or actionable instructions. Keep it defensive and educational only:\n\n{text}"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",  # Adjust model name if needed
            "messages": [
                {"role": "system", "content": "You are a helpful educational assistant. Only paraphrase and clarify. Never generate phishing content, links, or actionable examples."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500,
            "temperature": 0.3
        }
        
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("choices", [{}])[0].get("message", {}).get("content", None)
        else:
            logger.warning(f"LLM API returned status {response.status_code}")
            return None
            
    except Exception as e:
        logger.warning(f"LLM paraphrase failed: {e}")
        return None

def format_lesson_for_terminal(lesson: Dict[str, Any], use_llm: bool = False) -> str:
    """Format lesson data for terminal display"""
    output = []
    output.append("\n" + "="*70)
    output.append(f"📚 LESSON: {lesson['title']}")
    output.append("="*70)
    
    # Bullet points
    output.append("\n💡 Key Points:")
    output.append("-"*70)
    for bullet in lesson['bullets']:
        output.append(f"   • {bullet}")
    output.append("-"*70)
    
    output.append("="*70)
    
    return "\n".join(output)

def format_quiz_for_terminal(lesson: Dict[str, Any], question_num: int = 0) -> tuple[str, int, bool]:
    """Format quiz question and return formatted text, correct answer, and whether there are more questions"""
    quiz = lesson['quiz']
    if question_num >= len(quiz):
        return "", 0, False
    
    q = quiz[question_num]
    output = []
    output.append("\n" + "="*70)
    output.append(f"📝 QUIZ: {lesson['title']} (Question {question_num + 1}/10)")
    output.append("="*70)
    output.append(f"\n❓ {q['question']}")
    output.append("\n📋 Options:")
    for i, option in enumerate(q['options'], 1):
        output.append(f"   {i}. {option}")
    output.append("\n" + "-"*70)
    output.append("Enter your answer (1-3) or 'back' to return:")
    output.append("="*70)
    
    has_more = question_num < len(quiz) - 1
    return "\n".join(output), q['answer_index'], has_more

def evaluate_quiz_answer(lesson: Dict[str, Any], question_num: int, user_answer: int) -> str:
    """Evaluate quiz answer and return feedback"""
    quiz = lesson['quiz']
    q = quiz[question_num]
    # answer_index is 0-based, convert to 1-based for comparison with user input
    correct_index_0based = q['answer_index']
    correct_index_1based = correct_index_0based + 1
    
    output = []
    output.append("\n" + "="*70)
    
    if user_answer == correct_index_1based:
        output.append("✅ CORRECT!")
    else:
        output.append("❌ INCORRECT")
        output.append(f"\nThe correct answer is: {correct_index_1based}. {q['options'][correct_index_0based]}")
    
    output.append("="*70)
    
    return "\n".join(output)

def get_available_topics() -> List[str]:
    """Get list of available lesson topics"""
    return list(LESSONS.keys())

def get_all_quiz_questions() -> List[Dict[str, Any]]:
    """Get all quiz questions from all topics, shuffled"""
    import random
    all_questions = []
    for topic, lesson in LESSONS.items():
        for q in lesson['quiz']:
            q_with_topic = q.copy()
            q_with_topic['topic'] = topic
            q_with_topic['topic_title'] = lesson['title']
            all_questions.append(q_with_topic)
    random.shuffle(all_questions)
    return all_questions[:10]  # Return 10 mixed questions

