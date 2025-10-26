# Phish Refiner Behavior Documentation

## Overview

The Phish Refiner is an interactive agent that helps refine and improve phishing training templates in a safe, educational manner. It operates on sanitized templates only and does not generate real phishing content.

## Refinement Commands

### Tone Adjustment
**Command:** `improve_tone:<style>`

**Styles:**
- `formal` - Professional, business-like tone
- `casual` - Conversational, friendly tone
- `urgent` - Time-sensitive, pressing tone

**Example:**
```
You: improve_tone:urgent
Phish Refiner: ✅ Tone adjusted to urgent. Template updated.
```

### Urgency Modification
**Command:** `increase_urgency` or `decrease_urgency`

**Behavior:**
- Increases or decreases the urgency score by 1
- Modifies subject line accordingly
- Updates template description

**Example:**
```
You: increase_urgency
Phish Refiner: ✅ Urgency increased. Score: 9/10
```

### Red Flag Enhancement
**Command:** `focus_on_red_flags`

**Behavior:**
- Adds educational note about red flags
- Enhances training objectives
- Improves visibility of warning signs

**Example:**
```
You: focus_on_red_flags
Phish Refiner: ✅ Red flags highlighted for training.
```

## Sample Refinement Session

```
Phish Refiner: Hello! I'm ready to refine your template.
              What would you like me to improve?

You: improve_tone:formal
✅ Refinement applied! Template updated.

You: increase_urgency
✅ Refinement applied! Template updated.

You: focus_on_red_flags
✅ Refinement applied! Template updated.

You: done
✅ Refinement complete!
```

## Safety Enforcement

The refiner will refuse any request that could generate real phishing content:

**Refused Requests:**
- "Say you are Chase Bank" → Refused, offers sanitized alternative
- "Include a login link" → Refused, offers placeholder
- "Send this email" → Refused, explains educational purpose

**Allowed Requests:**
- Tone adjustments
- Urgency modifications
- Red flag enhancements
- Training objective updates

## Response Format

All refinements return:
- Confirmation message
- Updated template ID
- Modified urgency score (if applicable)
- List of changes made

## Export

Type `export` to save the refined template to:
`diagnostics/templates/<template_id>.json`

The exported JSON includes:
- Template ID
- Scenario title
- Sanitized description
- Placeholders
- Red flags
- Training objectives
- Urgency score
- Safety notes

