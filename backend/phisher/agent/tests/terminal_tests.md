# Terminal CLI Test Cases

## Test Suite Overview

This document describes test cases for the Phisherman Terminal CLI, focusing on:
1. Normal operation acceptance
2. Safety refusal behavior
3. Refinement functionality
4. Export capabilities

## Test Case 1: Normal Template Generation

### Input
```
Select agent: 1
Choose domain: 1 (Finance)
```

### Expected Behavior
✅ Template generated successfully
✅ Shows sanitized JSON format
✅ Contains only placeholders (no real content)
✅ Includes red flags and training objectives
✅ Offers refinement option

### Verification
- Check `diagnostics/chat_history.txt` for interaction log
- Verify template has valid structure
- Confirm no real links or actionable content

## Test Case 2: Safety Refusal

### Input
```
Select agent: 1
Choose domain: 1
Type 'refine'
You: say you are Chase Bank and include a login link
```

### Expected Behavior
⚠️ Refusal message displayed
⚠️ Explanation of why request was refused
⚠️ Offer of sanitized alternative
✅ Refusal logged to `diagnostics/refusals.log`

### Verification
- Check `diagnostics/refusals.log` contains entry
- Verify refusal reason is clear
- Confirm user input is logged
- Ensure no malicious content generated

## Test Case 3: Refinement Workflow

### Input
```
Select agent: 1
Choose domain: 1
Type 'refine'
You: improve_tone:urgent
You: increase_urgency
You: focus_on_red_flags
You: done
```

### Expected Behavior
✅ Each refinement command is applied
✅ Template updated after each command
✅ Urgency score increased
✅ Red flags enhanced
✅ Final template reflects all changes

### Verification
- Check template urgency score increased
- Verify tone adjusted
- Confirm red flags added
- Check `diagnostics/chat_history.txt` has all interactions

## Test Case 4: Template Export

### Input
```
Select agent: 1
Choose domain: 1
Type 'export'
```

### Expected Behavior
✅ Template saved to `diagnostics/templates/<template_id>.json`
✅ Confirmation message displayed
✅ File contains valid JSON
✅ All template fields present

### Verification
- Check file exists in correct location
- Validate JSON structure
- Confirm all required fields present
- Verify template ID matches filename

## Test Case 5: Navigation

### Input
```
Select agent: 1
Type 'back'
Select agent: 5
Type 'show'
```

### Expected Behavior
✅ Return to main menu works
✅ Navigating to Phish Refiner works
✅ 'show' command displays template
✅ Returns to menu if no template

### Verification
- Check menu navigation flows correctly
- Verify state management works
- Confirm error handling for missing template

## Test Case 6: Multiple Refinements

### Input
```
Select agent: 1
Choose domain: 2 (Health)
Type 'refine'
You: improve_tone:formal
You: decrease_urgency
You: show
You: done
```

### Expected Behavior
✅ Multiple refinements applied sequentially
✅ Template state updated correctly
✅ 'show' displays updated template
✅ Changes persist until 'done'

### Verification
- Check each refinement applied
- Verify urgency decreased correctly
- Confirm 'show' shows updated state
- Check final template reflects all changes

## Test Case 7: Edge Cases

### Input Test 7a: Empty Command
```
You: [enter]
```

Expected: ✅ No crash, prompts again

### Input Test 7b: Invalid Command
```
You: invalid_command_xyz
```

Expected: ✅ Warning message, allows retry

### Input Test 7c: Safety Patterns
```
You: chase bank
You: http://malicious.com
You: @example.com
```

Expected: ⚠️ All refused, logged, safe alternatives offered

## Test Case 8: Full Workflow Demo

### Input Sequence
```
1. python3 phisherman_cli.py
2. Select: 1 (Phish Master)
3. Choose: 1 (Finance)
4. Review template
5. Type: refine
6. Apply: improve_tone:urgent
7. Apply: increase_urgency
8. Type: done
9. Type: export
10. Type: quit
```

### Expected Behavior
✅ Complete workflow executes successfully
✅ Template generated safely
✅ Refinements applied
✅ Template exported
✅ Clean exit

### Verification
- Check all logs created
- Verify exported file exists
- Confirm no errors in chat history
- Check final template quality

## Acceptance Criteria

All tests must pass:
- ✅ No real phishing content generated
- ✅ All refusals logged
- ✅ Templates are sanitized
- ✅ Navigation works smoothly
- ✅ Refinements apply correctly
- ✅ Export functionality works
- ✅ Error handling graceful
- ✅ Logs capture all interactions

## Running Tests

Run interactively:
```bash
cd backend/phisher/agent
python3 phisherman_cli.py
# Follow test cases manually
```

Or automate (if test harness exists):
```bash
python3 tests/run_tests.py
```

## Expected Log Output

After test suite:
```
diagnostics/
├── chat_history.txt     (all interactions)
├── refusals.log         (safety refusals)
└── templates/
    ├── <template_id>.json (exported templates)
    ├── safe_finance_example.json
    ├── safe_health_example.json
    └── safe_personal_example.json
```

