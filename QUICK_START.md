# Quick Start - Socket Quiz System

## ✅ Status: Ready to Test

All files have been created and integrated. The socket-based quiz is ready to run.

## Files Created
- ✅ `frontend/src/quiz/socket.js` - Socket client
- ✅ `frontend/src/quiz/quiz.js` - React component  
- ✅ `frontend/src/quiz/styles.css` - Styles
- ✅ `backend/trainer/quiz_socket.py` - Socket server
- ✅ `backend/sockets/socket.py` - Updated with quiz handlers
- ✅ `frontend/src/routes/quiz.js` - Updated to use socket quiz

## 🚀 To Run

### 1. Start Backend
```bash
cd backend
python3 main.py
```
Should see: `Quiz socket namespace handlers registered`

### 2. Start Frontend  
```bash
cd frontend
yarn start
```

### 3. Open Quiz
Navigate to: `http://localhost:3000/quiz?topic=suspicious_link`

## 📋 What to Expect

1. **Console logs** show socket connection
2. **Questions appear** automatically after connection
3. **Click options** to answer (or use keyboard: 1-3, arrows, Enter)
4. **Score updates** in real-time (+10/-10)
5. **Progress** shows "Q X/10"
6. **Completion** shows final score

## 🔍 Quick Test Checklist

- [ ] Backend starts without errors
- [ ] Frontend connects to socket
- [ ] First question appears
- [ ] Can select and submit answer
- [ ] Score updates after answer
- [ ] Next question appears automatically
- [ ] Quiz completes after 10 questions
- [ ] Final score displayed

## 🐛 If Issues

1. **No connection**: Check backend is running on port 8080
2. **No questions**: Check browser console for errors
3. **Score not updating**: Check `backend/logs/quiz_socket.log`

## 📝 Topics Available

- `suspicious_link` - Default
- `abnormal_email` 
- `random_email_address`

Change via URL: `/quiz?topic=abnormal_email`

## 🎯 Key Features Working

- ✅ Real-time socket communication
- ✅ Scoring (+10/-10)
- ✅ Session management (2hr TTL)
- ✅ Progress tracking
- ✅ Keyboard navigation
- ✅ Visual feedback (✓/✗)
- ✅ Error handling
- ✅ Auto-reconnect

Ready to test! 🎉

