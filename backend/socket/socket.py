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
    data = 'test'