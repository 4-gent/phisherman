# Socket-Based Quiz System

Real-time, socket-based quiz flow that consumes questions from the trainer backend and reports answers/scores live.

## Overview

The quiz system uses Socket.IO for bidirectional communication between the frontend and backend. Questions are delivered in real-time, answers are validated server-side, and scores are calculated using the rules: **+10 for correct, -10 for wrong**.

## Architecture

### Frontend
- **Location**: `frontend/src/quiz/`
- **Main Component**: `quiz.js` - React component handling quiz UI and socket events
- **Socket Module**: `socket.js` - Socket.IO client factory and reconnect handlers
- **Styles**: `styles.css` - Component-scoped styles (preserves global theme)

### Backend
- **Location**: `backend/trainer/quiz_socket.py`
- **Namespace**: `/quiz`
- **Integration**: Registered in `backend/sockets/socket.py`

## Environment Variables

### Backend
```bash
QUIZ_MAX_QUESTIONS=10  # Default: 10 questions per quiz
```

### Frontend
```javascript
// Optional: Override socket URL
window.__WS_URL__ = 'http://localhost:8080';

// Optional: Disable quiz feature
window.__ENABLE_QUIZ__ = false;

// Optional: Analytics hook
window.__quiz_onEvent = (eventName, data) => {
  console.log('Quiz event:', eventName, data);
};
```

## Starting the Server

### Prerequisites
```bash
# Install backend dependencies
pip install flask flask-socketio python-socketio

# Install frontend dependencies (socket.io-client already in package.json)
cd frontend && npm install
```

### Start Backend
```bash
cd backend
python main.py
# Server runs on http://localhost:8080 (default)
```

### Start Frontend
```bash
cd frontend
npm start
# Frontend runs on http://localhost:3000
```

The Socket.IO server automatically registers the `/quiz` namespace handlers on startup.

## Event Schema

### Client → Server Events

#### `quiz:join`
Join or resume a quiz session.
```javascript
socket.emit('quiz:join', {
  userId: 'user123',
  topic: 'suspicious_link',  // or 'abnormal_email', 'random_email_address'
  sessionId: 'optional-session-id'  // For resuming existing session
});
```

#### `quiz:answer`
Submit an answer for a question.
```javascript
socket.emit('quiz:answer', {
  sessionId: 'session-uuid',
  qid: 'q0',
  choiceIndex: 0  // 0-based index, or -1 for no answer/timeout
});
```

#### `quiz:next`
Request the next question.
```javascript
socket.emit('quiz:next', {
  sessionId: 'session-uuid'
});
```

#### `quiz:leave`
Leave the quiz session.
```javascript
socket.emit('quiz:leave', {
  sessionId: 'session-uuid'
});
```

### Server → Client Events

#### `quiz:init`
Quiz session initialized.
```javascript
{
  sessionId: 'session-uuid',
  userId: 'user123',
  topic: 'suspicious_link',
  totalQuestions: 10
}
```

#### `quiz:question`
Question delivered.
```javascript
{
  qid: 'q0',
  index: 0,
  text: 'What should you do before clicking a suspicious link?',
  options: ['hover', 'click', 'ignore'],
  answer_index: 0,  // For frontend validation only
  seconds: null  // Optional timer (null if no timer)
}
```

#### `quiz:score:update`
Score updated after answer submission.
```javascript
{
  qid: 'q0',
  correct: true,
  delta: 10,  // +10 or -10
  total: 10
}
```

#### `quiz:complete`
Quiz completed.
```javascript
{
  total: 80,
  correctCount: 9,
  wrongCount: 1,
  history: [
    { qid: 'q0', choice_index: 0, correct: true, delta: 10 },
    { qid: 'q1', choice_index: 1, correct: false, delta: -10 },
    // ...
  ]
}
```

#### `quiz:error`
Error occurred.
```javascript
{
  message: 'Invalid session'
}
```

## Topic Options

Available quiz topics (from `backend/trainer/teacher.py`):
- `suspicious_link` - Identifying Suspicious Links
- `abnormal_email` - Recognizing Abnormal Email Patterns
- `random_email_address` - Dealing with Suspicious Email Addresses

## Scoring Rules

- **Correct answer**: +10 points
- **Wrong answer**: -10 points
- **No answer/timeout**: -10 points
- **Total score**: Sum of all deltas

## Usage in Frontend

### Basic Usage
```javascript
import SocketQuiz from './quiz/quiz';

function MyQuizPage() {
  return (
    <div id="quiz-root">
      <SocketQuiz 
        userId="user123" 
        topic="suspicious_link"
        onComplete={(results) => {
          console.log('Quiz complete:', results);
        }}
      />
    </div>
  );
}
```

### With URL Parameters
Navigate to `/quiz?topic=suspicious_link` to set the topic.

### Feature Flag
The quiz respects `window.__ENABLE_QUIZ__` - set to `false` to disable.

## Session Management

- Sessions are stored in-memory with a 2-hour TTL
- On reconnect, send `quiz:join` with `sessionId` to resume
- Sessions are logged to `diagnostics/quiz_sessions.log` (no PII)

## Accessibility

- Keyboard navigation: Arrow keys to select options, Enter to submit
- Screen reader friendly: ARIA labels and semantic HTML
- Focus management: Clear focus indicators

## CORS Configuration

The Socket.IO server is configured to allow connections from `http://localhost:3000`. For production:

```python
# In backend/sockets/socket.py
socketio = SocketIO(app, cors_allowed_origins=[
    'http://localhost:3000',
    'https://your-production-domain.com'
], manage_session=False)
```

## Production Considerations

### Sticky Sessions
If using multiple backend instances, ensure Socket.IO sessions are sticky (use session affinity/load balancer sticky sessions).

### Rate Limiting
Consider adding rate limiting for `quiz:answer` events (current: 1 per question via duplicate check).

### Error Handling
- Frontend: Error state displayed to user
- Backend: Errors logged to `logs/quiz_socket.log`
- Reconnection: Automatic reconnection with session resume

### Security
- Validate all inputs server-side
- Sanitize question text and options
- Cap options array length
- Throttle answer submissions (already implemented)

## Diagnostics

### Logs
- **Backend**: `backend/logs/quiz_socket.log`
- **Sessions**: `diagnostics/quiz_sessions.log` (JSONL format)

### Session Log Format
```json
{"timestamp": "2024-01-01T12:00:00Z", "session_id": "uuid", "event": "join", "data": {"topic": "suspicious_link"}}
```

## Troubleshooting

### Quiz not connecting
1. Check backend server is running on port 8080
2. Verify Socket.IO namespace `/quiz` is registered (check console logs)
3. Check CORS configuration matches frontend origin

### Questions not appearing
1. Verify topic is valid (check `backend/trainer/teacher.py`)
2. Check browser console for errors
3. Verify session was initialized (`quiz:init` event received)

### Score not updating
1. Check `quiz:answer` events are being sent
2. Verify sessionId matches
3. Check backend logs for scoring errors

### Session not resuming
1. Verify sessionId is stored and sent on reconnect
2. Check session hasn't expired (2-hour TTL)
3. Look for errors in browser console

## Example Payloads

### Complete Flow
```javascript
// 1. Join quiz
socket.emit('quiz:join', { userId: 'user1', topic: 'suspicious_link' });

// 2. Receive init
// socket.on('quiz:init', ...) => { sessionId: 'abc123', totalQuestions: 10 }

// 3. Receive question
// socket.on('quiz:question', ...) => { qid: 'q0', text: '...', options: [...] }

// 4. Submit answer
socket.emit('quiz:answer', { sessionId: 'abc123', qid: 'q0', choiceIndex: 0 });

// 5. Receive score update
// socket.on('quiz:score:update', ...) => { delta: 10, total: 10 }

// 6. Request next question
socket.emit('quiz:next', { sessionId: 'abc123' });

// 7. Receive complete
// socket.on('quiz:complete', ...) => { total: 80, correctCount: 9, ... }
```

## Integration with Existing UI

The socket quiz component preserves the existing UI theme:
- Uses global CSS variables and font families
- Preserves existing button classes where applicable
- No breaking changes to other routes or components
- Mounts to `#quiz-root` container (or specified container)

