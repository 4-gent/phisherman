#!/usr/bin/env python3
"""
Trainer CLI - Integrates Teacher agent into terminal CLI
Provides safe phishing awareness training via interactive terminal sessions.
"""

import sys
import os
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.trainer.teacher import (
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
    print("\n" + "="*70)
    print("🎓 Phisherman Teacher - Phishing Awareness Training")
    print("="*70)
    print("\n📚 Available Topics:")
    print("-"*70)
    topics = get_available_topics()
    for i, topic in enumerate(topics, 1):
        lesson = build_lesson_payload(topic)
        if lesson:
            print(f"{i}. {lesson['display'] if 'display' in lesson else lesson['title']}")
            print(f"   {lesson['title']}")
    print("-"*70)
    
    print("\n💡 Commands:")
    print("   • list                    - Show available topics")
    print("   • teach <topic>           - Display lesson for topic")
    print("   • quiz                    - Take mixed quiz from all topics")
    print("   • help                    - Show this help")
    print("   • exit / quit             - Return to main menu")
    print("="*70)
    
    # Check if LLM is available
    use_llm = bool(os.getenv("ASI1_API_KEY", ""))
    if use_llm:
        print("\n✨ LLM paraphrasing enabled (ASI1_API_KEY found)")
    else:
        print("\nℹ️  LLM paraphrasing not available (no ASI1_API_KEY)")
        print("   Lessons will use static content.")
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
                print("\n⚠️  SAFETY REFUSAL")
                print("   I cannot generate phishing templates, links, or impersonation content.")
                print("   I provide only defensive, educational lessons.")
                print("   Safe commands: list, teach <topic>, quiz, help, exit")
                continue
            
            # Parse commands
            parts = user_input.lower().split()
            command = parts[0]
            
            if command in ['exit', 'quit', 'q']:
                print("\n👋 Returning to main menu...")
                logger.info("Teacher session ended")
                break
            
            elif command == 'help':
                print("\n" + "="*70)
                print("📖 Teacher Commands")
                print("="*70)
                print("\n📚 Available Topics:")
                for topic in topics:
                    lesson = build_lesson_payload(topic)
                    if lesson:
                        print(f"   • {topic} - {lesson['title']}")
                print("\n💡 Commands:")
                print("   • list                    - Show available topics")
                print("   • teach <topic>           - Display lesson for topic")
                print("   • quiz                    - Take mixed quiz from all topics")
                print("   • help                    - Show this help")
                print("   • exit / quit             - Return to main menu")
                print("="*70)
            
            elif command == 'list':
                print("\n📚 Available Topics:")
                print("-"*70)
                for i, topic in enumerate(topics, 1):
                    lesson = build_lesson_payload(topic)
                    if lesson:
                        print(f"{i}. {lesson['title']}")
                        print(f"   {topic}")
                print("-"*70)
            
            elif command == 'teach':
                if len(parts) < 2:
                    print("\n❌ Usage: teach <topic>")
                    print("   Example: teach suspicious_link")
                    continue
                
                topic = parts[1]
                lesson = build_lesson_payload(topic)
                
                if not lesson:
                    print(f"\n❌ Topic '{topic}' not found.")
                    print("   Available topics:", ", ".join(topics))
                    continue
                
                # Display lesson immediately
                lesson_text = format_lesson_for_terminal(lesson, use_llm=use_llm)
                print(lesson_text)
                logger.info(f"Lesson displayed: {topic}")
            
            elif command == 'quiz':
                # Get mixed questions from all topics
                from backend.trainer.teacher import get_all_quiz_questions
                all_questions = get_all_quiz_questions()
                
                if not all_questions:
                    print("\n❌ No quiz questions available.")
                    continue
                
                # Run quiz - 10 mixed questions
                question_num = 0
                score = 0
                
                while question_num < len(all_questions):
                    q = all_questions[question_num]
                    # Format quiz question
                    print("\n" + "="*70)
                    print(f"📝 QUIZ (Question {question_num + 1}/10) - {q['topic_title']}")
                    print("="*70)
                    print(f"\n❓ {q['question']}")
                    print("\n📋 Options:")
                    for i, option in enumerate(q['options'], 1):
                        print(f"   {i}. {option}")
                    print("\n" + "-"*70)
                    print("Enter your answer (1-3) or 'back' to return:")
                    print("="*70)
                    
                    # Get user answer
                    while True:
                        answer_input = input("Your answer: ").strip().lower()
                        
                        if answer_input in ['back', 'exit', 'quit']:
                            print("\n📚 Returning to teacher menu...")
                            question_num = len(all_questions)  # Exit loop
                            break
                        
                        try:
                            answer_num = int(answer_input)
                            if 1 <= answer_num <= 3:
                                # Evaluate answer (user input is 1-based)
                                correct_index_0based = q['answer_index']
                                correct_index_1based = correct_index_0based + 1
                                is_correct = answer_num == correct_index_1based
                                
                                print("\n" + "="*70)
                                if is_correct:
                                    print("✅ CORRECT!")
                                    score += 1
                                else:
                                    print("❌ INCORRECT")
                                    print(f"\nThe correct answer is: {correct_index_1based}. {q['options'][correct_index_0based]}")
                                print("="*70)
                                
                                logger.info(f"Quiz Q{question_num + 1}: {q['topic']}, answer={answer_num}, correct={is_correct}")
                                
                                if question_num < len(all_questions) - 1:
                                    input("\nPress Enter to continue to next question...")
                                else:
                                    print(f"\n🎉 Quiz Complete! Score: {score}/10")
                                
                                question_num += 1
                                break
                            else:
                                print("❌ Please enter a number between 1 and 3")
                        except ValueError:
                            print("❌ Please enter a number (1-3) or 'back'")
                    
                    if answer_input in ['back', 'exit', 'quit']:
                        break
            
            else:
                print(f"\n❌ Unknown command: {command}")
                print("   Type 'help' for available commands")
        
        except KeyboardInterrupt:
            print("\n\n👋 Returning to main menu...")
            logger.info("Teacher session interrupted by user")
            break
        except Exception as e:
            logger.error(f"Error in teacher session: {e}", exc_info=True)
            print(f"\n❌ Error: {e}")
            print("   Type 'help' for available commands or 'exit' to quit")

if __name__ == "__main__":
    run_teacher_session()

