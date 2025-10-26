# Phisherman Terminal CLI - User Guide

## 🎓 Overview

The Phisherman Terminal CLI is an educational cybersecurity tool for generating sanitized phishing training templates. **NO real phishing content is produced** - only safe, educational materials.

## ⚠️ Safety Notice

- **Educational use only** - NO real phishing emails generated
- **Sanitized outputs** - Only placeholders and descriptions
- **Safety logging** - All refusals logged for audit
- **Non-actionable** - Content cannot be used for actual phishing

## 🚀 Quick Start

```bash
cd backend/phisher/agent
python3 phisherman_cli.py
```

## 📋 Commands

### Navigation
- `1-5` or agent name - Select an agent
- `help` - Show available commands
- `back` - Return to main menu
- `quit` / `exit` - Exit application

### Template Commands
- `show` - Display current template
- `refine` - Open refinement chat
- `export` - Save template to file

### Refinement Commands
- `improve_tone:<style>` - Change tone (formal/casual/urgent)
- `increase_urgency` - Raise urgency level
- `decrease_urgency` - Lower urgency level
- `focus_on_red_flags` - Highlight red flags
- `done` - Complete refinement

## 💬 Example Workflow

```
1. Select agent: 1 (Phish Master)
2. Choose domain: 1 (Finance)
3. Review generated template
4. Type 'refine' to improve
5. Apply refinements: improve_tone:urgent
6. Type 'done' when satisfied
7. Type 'export' to save
```

## 📁 File Locations

### Exported Templates
```
diagnostics/templates/<template_id>.json
```

### Logs
```
diagnostics/chat_history.txt      - Chat interactions
diagnostics/refusals.log          - Safety refusals
diagnostics/hosted_calls.txt      - API call metadata (if applicable)
```

### Example Templates
```
diagnostics/templates/safe_finance_example.json
diagnostics/templates/safe_health_example.json
diagnostics/templates/safe_personal_example.json
```

## 🎯 Template Format

All templates follow this sanitized structure:

```json
{
  "template_id": "FINacbd1234",
  "scenario_title": "Financial Account Verification Exercise",
  "sanitized_description": "Educational description...",
  "placeholders": {
    "subject": "[FINANCIAL_INSTITUTION_NAME] Account Verification",
    "preheader": "Action required to secure your account",
    "body_notes": "Tone and content description"
  },
  "red_flags": ["Lists red flags..."],
  "training_objectives": ["Lists objectives..."],
  "urgency_score": 8,
  "safety_notes": ["Safety disclaimers..."]
}
```

## ⚠️ Safety Features

### Automatic Refusal
The system will refuse requests for:
- Real bank names or institution names
- Actual links or URLs
- Sendable email content
- Real sender addresses
- Clickable buttons or actions

### Refusal Logging
All refusals are logged to `diagnostics/refusals.log` with:
- Timestamp
- Reason for refusal
- User input
- Type of refusal

## 📚 Documentation

- **Refiner Behavior:** `docs/refiner_behaviour.md`
- **Test Cases:** `tests/terminal_tests.md`
- **Agent Integration:** `diagnostics/integration_readme.md`

## 🧪 Testing

Run test cases from `tests/terminal_tests.md`:
```bash
python3 phisherman_cli.py
# Follow test scenarios interactively
```

## 🔒 Responsible Use

This tool is designed for:
- ✅ Cybersecurity awareness training
- ✅ Educational demonstrations
- ✅ Security team training
- ✅ Phishing simulation exercises (safe)

**Never use for:**
- ❌ Actual phishing attacks
- ❌ Fraudulent activities
- ❌ Unauthorized access attempts
- ❌ Malicious purposes

## 📞 Support

For questions or issues:
1. Check `docs/refiner_behaviour.md` for refiner commands
2. Review `tests/terminal_tests.md` for examples
3. Check logs in `diagnostics/` directory

## 🎓 Training Resources

The generated templates are intended to help users:
- Recognize phishing tactics
- Identify red flags
- Understand social engineering
- Practice detection skills

All content is designed to be educational and non-actionable.

