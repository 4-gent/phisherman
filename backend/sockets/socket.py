# ...existing code...
from flask import request
from flask_socketio import SocketIO, emit, join_room
from routes.routes import app
from phisher.agent.phisherman_cli import refine_template, orchestrate_flow

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

# helper worker used by multiple handlers
def _refine_worker(tpl, instruction, client_sid, event_type='prompt_response'):
    """
    Run refinement (or other processing) in background and emit back result.
    event_type allows using different response event names ('prompt_response' or 'chat_response').
    """
    try:
        # call the safe refiner; replace/extend with orchestrate_flow if desired
        refined = refine_template(tpl, instruction)
        payload = {'success': True, 'result': refined, 'instruction': instruction}
        socketio.emit(event_type, payload, room=client_sid)
    except Exception as e:
        print(f'_refine_worker failed: {e}')
        socketio.emit(event_type, {'success': False, 'error': str(e)}, room=client_sid)

@socketio.on('prompt_inject')
def handle_prompt_inject(data):
    sid = request.sid
    print('prompt_inject received from', sid, 'data keys:', list((data or {}).keys()))
    template = data.get('template') if isinstance(data, dict) else data

    def worker(tpl, client_sid):
        try:
            result = tpl
            socketio.emit('prompt_response', {'success': True, 'result': result}, room=client_sid)
        except Exception as e:
            print('prompt processing failed: ', e)
            socketio.emit('prompt_response', {'success': False, 'error': str(e)}, room=client_sid)

    socketio.start_background_task(worker, template, sid)

@socketio.on('prompt_refine')
def handle_prompt_refine(data):
    sid = request.sid
    print('prompt_refine received from', sid, 'keys:', list((data or {}).keys()))
    instruction = (data or {}).get('instruction')
    template = (data or {}).get('template')

    if not template or not instruction:
        emit('prompt_response', {'success': False, 'error': 'template and instruction required'}, room=sid)
        return

    # background refine, reply via prompt_response
    socketio.start_background_task(_refine_worker, template, instruction, sid, 'prompt_response')

@socketio.on('chat_message')
def handle_chat_message(data):
    """
    Expect data: { template: {...}, message: "user input" }
    Returns: emits 'chat_response' with the refined/updated template or chat reply.
    """
    sid = request.sid
    print('chat_message from', sid, 'keys:', list((data or {}).keys()))
    template = (data or {}).get('template')
    message = (data or {}).get('message')

    if not template or not message:
        emit('chat_response', {'success': False, 'error': 'template and message required'}, room=sid)
        return

    # use the same refiner worker but emit as 'chat_response'
    socketio.start_background_task(_refine_worker, template, message, sid, 'chat_response')
    

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
