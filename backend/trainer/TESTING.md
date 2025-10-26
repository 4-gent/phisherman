# Testing the Teacher Agent

## Method 1: Through Main CLI (Recommended)

1. Start the main Phisherman CLI:
```bash
# From project root
cd backend/phisher/agent
python3 phisherman_cli.py
```

2. Select option `6` for Teacher

3. Test commands:
   - `list` - Show available topics
   - `teach suspicious_link` - View lesson on suspicious links
   - `teach abnormal_email` - View lesson on abnormal emails
   - `teach random_email_address` - View lesson on email addresses
   - `quiz` - Take mixed quiz (10 questions from all topics)
   - `help` - Show help
   - `exit` - Return to main menu

## Method 2: Run Teacher Directly

From project root:
```bash
python3 -m backend.trainer.cli
```

Or if you're already in backend directory:
```bash
# From backend directory
cd trainer
python3 cli.py
```

Or directly:
```bash
# From project root
python3 backend/trainer/cli.py
```

## Quick Test Script

Run this to verify everything works:

```bash
cd backend
python3 -c "from trainer import run_teacher_session; print('Teacher module imported successfully')"
```

## Expected Behavior

### When you run `teach suspicious_link`:
```
LESSON: Identifying Suspicious Links

Key Points:
  - Hover over links to check destination URLs
  - Watch for misspelled domain names
  - Avoid shortened URLs from unknown services
  - Verify links before clicking
```

### When you run `quiz`:
```
Question 1/10 - Identifying Suspicious Links
What should you do before clicking a suspicious link?

Options:
1. hover
2. click
3. ignore

Enter your answer (1-3) or 'back' to return:
Your answer: 1

CORRECT!

Press Enter to continue...
```

## Troubleshooting

**Import errors?**
- Make sure you're in the project root or backend directory
- Check that `backend/trainer/` exists with `__init__.py`, `cli.py`, and `teacher.py`

**Module not found?**
```bash
# Add project root to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Want to see logs?**
- Check `backend/logs/trainer_teacher.log` for all teacher interactions

