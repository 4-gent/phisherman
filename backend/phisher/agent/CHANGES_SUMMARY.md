# Phisherman Terminal CLI - Changes Summary

## 🎯 Overview

Created a production-ready, safe terminal CLI for generating sanitized phishing training templates. The system enforces strict safety constraints and generates ONLY educational, non-actionable content.

## ✨ Key Improvements

### 1. **Safety-First Design**
- ✅ NO real phishing content generated
- ✅ Only sanitized placeholders and descriptions
- ✅ Automatic refusal of unsafe requests
- ✅ All refusals logged for audit
- ✅ Explicit safety notices throughout

### 2. **Sanitized Template Format**
All templates now follow safe JSON structure:
```json
{
  "template_id": "FINacbd1234",
  "scenario_title": "Financial Account Verification Exercise",
  "sanitized_description": "Educational description only",
  "placeholders": { "subject": "[PLACEHOLDER]", ... },
  "red_flags": ["Educational red flags"],
  "training_objectives": ["Training goals"],
  "urgency_score": 8,
  "safety_notes": ["Safety disclaimers"]
}
```

### 3. **Enhanced Navigation**
- Clear numbered agent selection
- Back command to return to menu
- Help command with examples
- Show command to display template
- Export command to save templates

### 4. **Refinement System**
- Targeted refinement commands
- Tone adjustment (formal/casual/urgent)
- Urgency modification
- Red flag enhancement
- Real-time template updates

### 5. **Comprehensive Logging**
- Chat history logged
- Safety refusals logged
- Template exports tracked
- Audit trail maintained

## 📁 Files Created

### Core Application
- `phisherman_cli.py` - Main terminal CLI application

### Example Templates
- `diagnostics/templates/safe_finance_example.json`
- `diagnostics/templates/safe_health_example.json`
- `diagnostics/templates/safe_personal_example.json`

### Documentation
- `README_TERMINAL.md` - User guide
- `docs/refiner_behaviour.md` - Refiner documentation
- `tests/terminal_tests.md` - Test cases
- `CHANGES_SUMMARY.md` - This file

### Tools
- `demo_script.sh` - 60-second demo script
- `tools/view_template.html` - Template viewer

## 🚀 Quick Start

```bash
cd backend/phisher/agent
python3 phisherman_cli.py
```

## 📋 Demo Script (60 seconds)

```bash
./demo_script.sh
```

Demonstrates:
1. Generate finance template
2. Refine tone to urgent
3. Increase urgency
4. Export template
5. Show logs

## ⚠️ Safety Features

### Automatic Refusal
The system refuses requests for:
- Real bank names ("Chase Bank")
- Actual links ("http://...")
- Sendable email content
- Real addresses ("@example.com")
- Actionable instructions

### Refusal Response
```
⚠️ SAFETY REFUSAL: Attempted to request real phishing content
   For security reasons, I cannot generate real phishing content.
   Instead, here's what I can provide:
   - Sanitized scenario descriptions
   - Red flag identification training
   - Placeholder templates
   - Educational safety notes
```

## 🧪 Test Cases

See `tests/terminal_tests.md` for:
- Template generation acceptance
- Safety refusal behavior
- Refinement workflow
- Export functionality
- Edge case handling

## 📊 Workflow

```
User → Phish Master → Choose Domain → Generate Template
                                              ↓
                                    Show Sanitized Template
                                              ↓
                            Option: Refine → Phish Refiner
                                              ↓
                            Apply Refinements → Done
                                              ↓
                            Option: Export → Save JSON
```

## 🎓 Educational Focus

All outputs include:
- ✅ Scenario titles (not real subjects)
- ✅ Sanitized descriptions
- ✅ Placeholders (not real content)
- ✅ Red flags for training
- ✅ Training objectives
- ✅ Safety notes

**NO outputs include:**
- ❌ Real email content
- ❌ Actual links
- ❌ Real sender addresses
- ❌ Clickable buttons
- ❌ Actionable instructions

## 📝 Files Generated

When using the CLI:
```
diagnostics/
├── chat_history.txt          # All interactions
├── refusals.log              # Safety refusals
├── templates/
│   ├── safe_finance_example.json  # Example
│   ├── safe_health_example.json   # Example
│   ├── safe_personal_example.json # Example
│   └── <template_id>.json         # Generated
```

## 🔍 Example Output

```
📄 TEMPLATE
======================================================================
🆔 Template ID: FINacbd1234
📝 Scenario: Financial Account Verification Exercise

📖 Description:
   This template demonstrates common tactics used in financial 
   phishing: urgent account verification requests, payment 
   information requests, and security alerts.

📋 Placeholders:
   • subject: [FINANCIAL_INSTITUTION_NAME] Account Verification
   • preheader: Action required to secure your account
   • body_notes: Professional tone requesting verification...

🚩 Red Flags:
   • Requests immediate action
   • Asks for account verification
   • Contains urgency language
   • May request sensitive information
   • Email sender may be spoofed

🎯 Training Objectives:
   • Identify urgency manipulation tactics
   • Recognize account verification scams
   • Understand social engineering
   • Practice detecting red flags

⚠️ Urgency Score: 8/10

✅ Safety Notes:
   • This is an educational template only
   • Contains NO real links or actionable content
   • Intended for cybersecurity awareness training
   • Should NEVER be used for actual phishing
======================================================================
```

## 🎯 Compliance

✅ No real phishing content
✅ All content sanitized
✅ Safety enforced
✅ Logging for audit
✅ Educational focus
✅ Clear disclaimers

## 🚀 Next Steps

1. Run `python3 phisherman_cli.py`
2. Follow demo script for judges
3. Review exported templates
4. Check logs for audit trail
5. Use templates for training

