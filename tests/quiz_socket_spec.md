# Quiz Socket Test Specification

Manual test plan and expected event order for the socket-based quiz system.

## Prerequisites

1. Backend server running on `http://localhost:8080`
2. Frontend running on `http://localhost:3000`
3. Browser console open (F12)
4. Socket.IO inspector or network tab enabled

## Test Case 1: Basic Quiz Flow

### Steps
1. Navigate to `http://localhost:3000/quiz?topic=suspicious_link`
2. Observe browser console for socket connection
3. Answer all 10 questions
4. Verify final score calculation

### Expected Event Order
```
1. Client → Server: connect (to /quiz namespace)
2. Server → Client: connected
3. Client → Server: quiz:join { userId, topic }
4. Server → Client: quiz:init { sessionId, totalQuestions: 10 }
5. Server → Client: quiz:question { qid: 'q0', text, options, ... }
6. User selects option
7. Client → Server: quiz:answer { sessionId, qid, choiceIndex }
8. Server → Client: quiz:score:update { delta: 10/-10, total }
9. Client → Server: quiz:next { sessionId }
10. Server → Client: quiz:question { qid: 'q1', ... }
... (repeat steps 6-10 for remaining questions)
11. Server → Client: quiz:complete { total, correctCount, wrongCount, history }
```

### Validation
- [ ] Socket connects successfully
- [ ] Session ID is received
- [ ] Questions appear in order
- [ ] Score updates after each answer (+10 or -10)
- [ ] Correct answers show ✓, wrong show ✗
- [ ] Final score matches calculation (sum of deltas)
- [ ] No console errors

## Test Case 2: Answer Validation

### Steps
1. Start quiz
2. Submit correct answer (choiceIndex matches answer_index)
3. Submit wrong answer (choiceIndex ≠ answer_index)
4. Verify scoring

### Expected Behavior
- Correct answer: `delta: 10`, `correct: true`
- Wrong answer: `delta: -10`, `correct: false`
- Score badge updates in real-time

### Validation
- [ ] Correct answers award +10
- [ ] Wrong answers deduct -10
- [ ] Visual feedback (✓/✗) appears correctly
- [ ] Score badge reflects running total

## Test Case 3: Session Resume

### Steps
1. Start quiz, answer 3 questions
2. Refresh page (simulate disconnect)
3. Verify session resumes from question 4

### Expected Behavior
- On reconnect, client sends `quiz:join` with `sessionId`
- Server resumes session from last question
- Score and history preserved

### Validation
- [ ] Session ID stored (check localStorage/sessionStorage)
- [ ] On reconnect, session resumes correctly
- [ ] Score and progress maintained
- [ ] Questions continue from where left off

## Test Case 4: Keyboard Navigation

### Steps
1. Start quiz
2. Use arrow keys to navigate options
3. Press Enter to submit
4. Use number keys (1-3) to select options

### Expected Behavior
- Arrow keys cycle through options
- Enter submits selected answer
- Number keys directly select option

### Validation
- [ ] Arrow keys work
- [ ] Enter submits answer
- [ ] Number keys select options
- [ ] Focus indicators visible

## Test Case 5: Error Handling

### Steps
1. Start quiz
2. Disconnect network (simulate)
3. Reconnect
4. Submit answer during disconnection

### Expected Behavior
- Reconnection handler attempts to reconnect
- Session resumes on reconnect
- Answers submitted during disconnect are queued or ignored

### Validation
- [ ] Reconnection attempts occur
- [ ] Session resumes after reconnect
- [ ] No duplicate answers processed
- [ ] Error messages displayed appropriately

## Test Case 6: Invalid Inputs

### Steps
1. Start quiz
2. Try to submit answer with invalid `choiceIndex`
3. Try to submit answer for already-answered question
4. Try to join with invalid topic

### Expected Behavior
- Invalid choiceIndex: Error message, answer ignored
- Duplicate answer: Ignored (idempotency)
- Invalid topic: Fallback to mixed questions

### Validation
- [ ] Invalid inputs rejected gracefully
- [ ] Duplicate answers prevented
- [ ] Error messages informative
- [ ] No crashes or exceptions

## Test Case 7: Multiple Topics

### Steps
1. Test `suspicious_link` topic
2. Test `abnormal_email` topic
3. Test `random_email_address` topic
4. Test invalid topic (fallback)

### Expected Behavior
- Each topic loads appropriate questions
- Invalid topic uses mixed questions
- Score calculation consistent across topics

### Validation
- [ ] All topics work correctly
- [ ] Questions match topic
- [ ] Scoring rules consistent
- [ ] Invalid topic handled gracefully

## Test Case 8: Timer Functionality (If Implemented)

### Steps
1. Start quiz with timer enabled
2. Let timer expire
3. Verify auto-submit

### Expected Behavior
- Timer counts down if `seconds` provided
- On expiry, answer submitted as -1 (no answer)
- Score deducted 10 points

### Validation
- [ ] Timer displays correctly
- [ ] Auto-submit on expiry
- [ ] No answer treated as wrong (-10)

## Test Case 9: Analytics Hooks

### Steps
1. Set `window.__quiz_onEvent` callback
2. Complete quiz
3. Verify events logged

### Expected Behavior
- Callback called for: init, question, answer, score, complete
- Data passed correctly to callback

### Validation
- [ ] All events trigger callback
- [ ] Data format correct
- [ ] No errors in callback execution

## Test Case 10: UI Theme Preservation

### Steps
1. Navigate to quiz page
2. Compare with other pages
3. Verify styling consistency

### Expected Behavior
- Global theme preserved
- No visual regressions
- Existing CSS variables respected

### Validation
- [ ] Colors match theme
- [ ] Fonts consistent
- [ ] Spacing follows design system
- [ ] No layout shifts

## Test Case 11: Multiple Users

### Steps
1. Open quiz in two browser windows
2. Complete quiz in both
3. Verify independent sessions

### Expected Behavior
- Each window has separate session
- Scores independent
- No cross-session interference

### Validation
- [ ] Separate session IDs
- [ ] Independent scoring
- [ ] No data leakage between sessions

## Test Case 12: Session Expiry

### Steps
1. Start quiz session
2. Wait 2+ hours (or modify TTL in code)
3. Try to resume session

### Expected Behavior
- Session expires after TTL
- Resume attempt creates new session
- Old session data discarded

### Validation
- [ ] Expired sessions cleaned up
- [ ] New session created on resume
- [ ] No stale data accessed

## Event Validation Checklist

### quiz:init
- [ ] Contains `sessionId` (UUID format)
- [ ] Contains `userId`
- [ ] Contains `topic`
- [ ] Contains `totalQuestions` (default 10)

### quiz:question
- [ ] Contains `qid` (unique per question)
- [ ] Contains `index` (0-based)
- [ ] Contains `text` (string)
- [ ] Contains `options` (array of strings, length 3)
- [ ] Contains `answer_index` (0-2)
- [ ] Optionally contains `seconds` (number or null)

### quiz:score:update
- [ ] Contains `qid` (matches answered question)
- [ ] Contains `correct` (boolean)
- [ ] Contains `delta` (+10 or -10)
- [ ] Contains `total` (running sum)

### quiz:complete
- [ ] Contains `total` (final score)
- [ ] Contains `correctCount` (number)
- [ ] Contains `wrongCount` (number)
- [ ] Contains `history` (array of answer objects)

## Performance Checks

- [ ] Questions load within 100ms
- [ ] Score updates instantly (< 50ms)
- [ ] No memory leaks (check browser DevTools)
- [ ] Session cleanup working (check backend logs)

## Browser Compatibility

Test in:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

## Production Readiness Checklist

- [ ] CORS configured for production domain
- [ ] Environment variables set correctly
- [ ] Logging working (backend + diagnostics)
- [ ] Error handling robust
- [ ] No hardcoded URLs
- [ ] Security validations in place
- [ ] Rate limiting considered
- [ ] Session storage strategy appropriate
- [ ] Analytics hooks documented
- [ ] Tests pass all cases above

## Reporting Issues

When reporting issues, include:
1. Browser and version
2. Console errors/warnings
3. Network tab (Socket.IO messages)
4. Steps to reproduce
5. Expected vs actual behavior
6. Session ID (if applicable)

