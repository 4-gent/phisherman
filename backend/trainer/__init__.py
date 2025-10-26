"""
Trainer package - Provides teacher agent for phishing awareness training
"""

# Handle imports gracefully when running from backend directory
try:
    from backend.trainer.cli import run_teacher_session
except ImportError:
    try:
        from trainer.cli import run_teacher_session
    except ImportError:
        def run_teacher_session():
            print("Teacher session not available")

__all__ = ['run_teacher_session']

