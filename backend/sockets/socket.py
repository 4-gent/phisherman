from flask import Flask, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from routes.routes import app

socketio = SocketIO(app, cors_allowed_origins='http://localhost:3000', manage_session=False)

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