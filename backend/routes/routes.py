from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import uuid
import os
from bson import ObjectId
import json

from connect import db, users
from mail.sender.sender import email_send
from phisher.agent.phisherman_cli import orchestrate_flow

app = Flask(__name__)

app.secret_key = 'im-phishing-it'

app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False

CORS(app, origins=['http://localhost:3000'], supports_credentials=True)

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return 'we in that hoe'

@app.route('/register', methods=['POST'])
def register():
    if request.method == "POST":
        try:
            data = request.get_json()
            # Minimal register implementation: create a user with a hashed password
            username = data.get('username')
            password = data.get('password')
            company = data.get('company').lower()
            email = data.get('email')

            if not username or not password:
                return jsonify({'success': False, 'message': 'username and password required'}), 400

            # avoid duplicate usernames
            existing = users.find_one({'username': username})
            if existing:
                return jsonify({'success': False, 'message': 'username already exists'}), 409

            pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = {
                'username': username,
                'password': pw_hash,
                'company': company,
                'email': email,
                'isAdmin': False
            }
            result = users.insert_one(new_user)
            return jsonify({'success': True, 'id': str(result.inserted_id)}), 200
        except Exception as e:
            print("exception thrown at register: ", e)
            return jsonify({'success': False, 'message': 'server error'}), 500

@app.route('/login', methods=['POST'])
def login():
    if request.method == "POST":
        try:
            data = request.get_json()
            print(data)
            username = data.get('username')
            password = data.get('password')

            user = users.find_one({'username': username})
            if not user:
                return jsonify({'success': False, 'message': 'invalid credentials'}), 401

            stored_pw = user.get('password')
            password_ok = False

            # Try bcrypt verification if a hash is stored
            try:
                password_ok = bcrypt.check_password_hash(stored_pw, password)
            except Exception:
                # fallback to plain text compare (if DB contains plain passwords)
                password_ok = (stored_pw == password)

            if not password_ok:
                return jsonify({'success': False, 'message': 'invalid credentials'}), 401

            # successful login: set session and return success
            if user.get('isAdmin') == False:
                session['user_id'] = str(user.get('_id'))
                return jsonify({'success': True, 'username': username}), 200
            elif user.get('isAdmin') == True:
                session['user_id'] = str(user.get('_id'))
                return jsonify({'success': True, 'username': username}), 201
            else:
                print("Error at login")
                return jsonify({'success': False}), 400 
        except Exception as e:
            print("exception thrown at login: ", e)
            return jsonify({'success': False, 'message': 'server error'}), 500

@app.route('/api/user', methods=['GET'])
def user_data():
    if request.method == 'GET':
        if 'user_id' not in session:
            print('user_id is not in the session')
            return jsonify({'message': 'unauthorized'}), 401
        if request.method == 'GET':
            data = users.find_one({'_id': ObjectId(session['user_id'])})
            if(data):
                data['_id'] = str(data['_id'])
                return jsonify(data)
            else:
                return jsonify({'message': 'User not found'}), 404

@app.route('/api/email', methods=['POST', 'OPTIONS'])
def email_send_route():
    if request.method == 'POST' or request.method == 'OPTIONS':
        print("Sending test email")
        email_send()
        return jsonify({'message': "something"}), 200
    
@app.route('/api/campaign', methods=['POST', 'OPTIONS'])
def email_template_route():
# handle CORS preflight quickly and with a valid response
    if request.method == 'OPTIONS':
        return jsonify({'message': 'ok'}), 200

    try:
        # get_json may return None for invalid/missing JSON; default to empty dict
        data = request.get_json(silent=True) or {}
        template = data.get('template') if isinstance(data, dict) else None

        print('Template: ', template)

        if not template:
            return jsonify({'success': False, 'message': 'template required'}), 400

        if template:
            email_template = orchestrate_flow(template)
            email_result = json.dumps(email_template)
            print("plain result: ", email_result)
            print("data type: ", type(data))
            print("parsed for html body: ", email_template['html_body'])
            email_send()
            

        return jsonify({'success': True, 'message': 'input received', 'template': template}), 200

    except Exception as e:
        print("exception thrown at campaign: ", e)
        return jsonify({'success': False, 'message': 'server error'}), 500
    
@app.route('/api/completion', methods=['POST', 'OPTIONS'])
def training_completion():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'ok'}), 200
    
    try:
        data = request.get_json(silent=True) or {}
        training = data.get('training')
        if training is False:
            return jsonify({'success': False, 'message': 'training incomplete'}), 400    
        if training is True:
            print("training complete")
            return jsonify({'success': True, 'message': 'training completed'}), 200
        return jsonify({'success': False, 'message': 'invalid payload at training'}), 400
    except Exception as e:
        print("exception thrown at training: ", e)
        return jsonify({'success': False, 'message': 'server error'}), 500