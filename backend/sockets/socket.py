from flask import Flask, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from routes.routes import app

socketio = SocketIO(
    app, 
    cors_allowed_origins='http://localhost:3000', 
    manage_session=False,
    async_mode='threading',
    logger=True,
    engineio_logger=True
)

@socketio.on('connect')
def handle_connect():
    print('website connected to backend socket: ', request.sid)
    emit('connected', {'sid': request.sid})

@socketio.on('join_training')
def on_join_training(data):
    room = (data or {}).get('room', 'global')
    join_room(room)
    emit('joined', {'room': room}, room=request.sid)

    test_payload = {
        'concept': 1,
        'status': 'done',
        'text': 'Test block of text for concept 1 - replace with real output when ready'
    }

    socketio.emit('concept_update', test_payload, room=room)

# Register quiz socket namespace handlers
try:
    from trainer.quiz_socket import register_quiz_socketio_handlers
    register_quiz_socketio_handlers(socketio)
    print('Quiz socket namespace handlers registered')
except ImportError:
    try:
        from backend.trainer.quiz_socket import register_quiz_socketio_handlers
        register_quiz_socketio_handlers(socketio)
        print('Quiz socket namespace handlers registered')
    except Exception as e:
        print(f'Warning: Could not register quiz socket handlers: {e}')
        import traceback
        traceback.print_exc()