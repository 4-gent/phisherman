#!/usr/bin/env python3
"""
Trainer CLI - Integrates Teacher agent into terminal CLI
Provides safe phishing awareness training via interactive terminal sessions.
"""

import sys
import os
from typing import Optional

# Add project root to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(backend_dir)

# Add both project root and backend to path
if project_root not in sys.path:
    sys.path.insert(0, project_root)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Try importing from backend.trainer, fallback to direct import
try:
    from backend.trainer.teacher import (
        build_lesson_payload,
        is_harmful_request,
        format_lesson_for_terminal,
        format_quiz_for_terminal,
        evaluate_quiz_answer,
        get_available_topics,
        logger
    )
except ImportError:
    # Fallback: import directly from teacher module
    from teacher import (
        build_lesson_payload,
        is_harmful_request,
        format_lesson_for_terminal,
        format_quiz_for_terminal,
        evaluate_quiz_answer,
        get_available_topics,
        logger
    )

def run_teacher_session():
    """Run interactive teacher session in terminal"""
    print("\nPhisherman Teacher - Phishing Awareness Training")
    print("\nAvailable Topics:")
    topics = get_available_topics()
    for i, topic in enumerate(topics, 1):
        lesson = build_lesson_payload(topic)
        if lesson:
            print(f"{i}. {lesson['title']}")
    
    print("\nCommands:")
    print("  list                    - Show available topics")
    print("  teach <topic>           - Display lesson for topic")
    print("  quiz                    - Take mixed quiz from all topics")
    print("  help                    - Show this help")
    print("  exit / quit             - Return to main menu")
    
    # Check if LLM is available
    use_llm = bool(os.getenv("ASI1_API_KEY", ""))
    if use_llm:
        print("\nLLM paraphrasing enabled (ASI1_API_KEY found)")
    else:
        print("\nLLM paraphrasing not available (no ASI1_API_KEY)")
        print("Lessons will use static content.")
    print()
    
    while True:
        try:
            user_input = input("Teacher> ").strip()
            
            if not user_input:
                continue
            
            # Log command
            logger.info(f"Teacher command: {user_input}")
            
            # Safety check
            if is_harmful_request(user_input):
                logger.warning(f"Harmful request refused: {user_input}")
                print("\nSAFETY REFUSAL")
                print("I cannot generate phishing templates, links, or impersonation content.")
                print("I provide only defensive, educational lessons.")
                print("Safe commands: list, teach <topic>, quiz, help, exit")
                continue
            
            # Parse commands
            parts = user_input.lower().split()
            command = parts[0]
            
            if command in ['exit', 'quit', 'q']:
                print("\nReturning to main menu...")
                logger.info("Teacher session ended")
                break
            
            elif command == 'help':
                print("\nTeacher Commands")
                print("\nAvailable Topics:")
                for topic in topics:
                    lesson = build_lesson_payload(topic)
                    if lesson:
                        print(f"  {topic} - {lesson['title']}")
                print("\nCommands:")
                print("  list                    - Show available topics")
                print("  teach <topic>           - Display lesson for topic")
                print("  quiz                    - Take mixed quiz from all topics")
                print("  help                    - Show this help")
                print("  exit / quit             - Return to main menu")
            
            elif command == 'list':
                print("\nAvailable Topics:")
                for i, topic in enumerate(topics, 1):
                    lesson = build_lesson_payload(topic)
                    if lesson:
                        print(f"{i}. {lesson['title']}")
            
            elif command == 'teach':
                if len(parts) < 2:
                    print("\nUsage: teach <topic>")
                    print("Example: teach suspicious_link")
                    continue
                
                topic = parts[1]
                lesson = build_lesson_payload(topic)
                
                if not lesson:
                    print(f"\nTopic '{topic}' not found.")
                    print("Available topics:", ", ".join(topics))
                    continue
                
                # Display lesson immediately
                lesson_text = format_lesson_for_terminal(lesson, use_llm=use_llm)
                print(lesson_text)
                logger.info(f"Lesson displayed: {topic}")
            
            elif command == 'quiz':
                # Get mixed questions from all topics
                try:
                    from backend.trainer.teacher import get_all_quiz_questions
                except ImportError:
                    from teacher import get_all_quiz_questions
                all_questions = get_all_quiz_questions()
                
                if not all_questions:
                    print("\nNo quiz questions available.")
                    continue
                
                # Run quiz - 10 mixed questions
                question_num = 0
                score = 0
                
                while question_num < len(all_questions):
                    q = all_questions[question_num]
                    # Format quiz question
                    print(f"\nQuestion {question_num + 1}/10 - {q['topic_title']}")
                    print(f"{q['question']}")
                    print("\nOptions:")
                    for i, option in enumerate(q['options'], 1):
                        print(f"{i}. {option}")
                    print("\nEnter your answer (1-3) or 'back' to return:")
                    
                    # Get user answer
                    while True:
                        answer_input = input("Your answer: ").strip().lower()
                        
                        if answer_input in ['back', 'exit', 'quit']:
                            print("\nReturning to teacher menu...")
                            question_num = len(all_questions)  # Exit loop
                            break
                        
                        try:
                            answer_num = int(answer_input)
                            if 1 <= answer_num <= 3:
                                # Evaluate answer (user input is 1-based)
                                correct_index_0based = q['answer_index']
                                correct_index_1based = correct_index_0based + 1
                                is_correct = answer_num == correct_index_1based
                                
                                print("")
                                if is_correct:
                                    print("CORRECT!")
                                    score += 1
                                else:
                                    print("INCORRECT")
                                    print(f"The correct answer is: {correct_index_1based}. {q['options'][correct_index_0based]}")
                                
                                logger.info(f"Quiz Q{question_num + 1}: {q['topic']}, answer={answer_num}, correct={is_correct}")
                                
                                if question_num < len(all_questions) - 1:
                                    input("\nPress Enter to continue...")
                                else:
                                    print(f"\nQuiz Complete! Score: {score}/10")
                                
                                question_num += 1
                                break
                            else:
                                print("Please enter a number between 1 and 3")
                        except ValueError:
                            print("Please enter a number (1-3) or 'back'")
                    
                    if answer_input in ['back', 'exit', 'quit']:
                        break
            
            else:
                print(f"\nUnknown command: {command}")
                print("Type 'help' for available commands")
        
        except KeyboardInterrupt:
            print("\n\nReturning to main menu...")
            logger.info("Teacher session interrupted by user")
            break
        except Exception as e:
            logger.error(f"Error in teacher session: {e}", exc_info=True)
            print(f"\nError: {e}")
            print("Type 'help' for available commands or 'exit' to quit")

if __name__ == "__main__":
    run_teacher_session()

