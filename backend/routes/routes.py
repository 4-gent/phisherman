from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import uuid
import os
from bson import ObjectId
import json

from connect import db, users
from phisher.agent.phisherman_cli import orchestrate_flow

# Optional email import (for quiz to work without mailjet)
try:
    from mail.sender.sender import email_send
except ImportError:
    def email_send():
        print("Email sending not available (mailjet_rest not installed)")

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

@app.route('/api/prompt/send', methods=['POST', 'OPTIONS'])
def email_send_route():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'ok'}), 200

    try:
        data = request.get_json(silent=True) or {}
        prompt = data.get('prompt') or data.get('message')

        # try to coerce prompt from a JSON string into a dict
        if isinstance(prompt, str):
            try:
                prompt_parsed = json.loads(prompt)
                prompt = prompt_parsed
            except Exception:
                # not JSON — return a helpful error (or change this to accept plain text)
                return jsonify({
                    'success': False,
                    'message': 'prompt must be a JSON object or a JSON-string containing the template fields',
                    'received_type': 'string',
                    'echo': prompt
                }), 400

        if not prompt or not isinstance(prompt, dict):
            return jsonify({'success': False, 'message': 'prompt required and must be an object'}), 400

        # optional: get company from session user
        company = ''
        try:
            user_data = users.find_one({'_id': ObjectId(session.get('user_id'))}) if session.get('user_id') else None
            if user_data:
                company = user_data.get('company', '')
                print(company)
        except Exception as e:
            print('warning: failed to lookup user/company:', e)

        # validate required template fields
        required = ['subject', 'preheader', 'html_body']
        missing = [k for k in required if not prompt.get(k)]
        if missing:
            return jsonify({'success': False, 'message': f'missing template fields: {missing}'}), 400

        subject = prompt.get('subject')
        preheader = prompt.get('preheader')
        html_body = prompt.get('html_body')

        # send email (mailjet helper)
        email_send(html_body, subject, preheader, company)
        return jsonify({'success': True, 'message': 'campaign sent'}), 200

    except Exception as e:
        print('exception thrown at prompt_send: ', e)
        return jsonify({'success': False, 'message': 'Server error', 'error': str(e)}), 500
    
@app.route('/api/campaign', methods=['POST', 'OPTIONS'])
def email_template_route():
# handle CORS preflight quickly and with a valid response
    if request.method == 'OPTIONS':
        return jsonify({'message': 'ok'}), 200

    try:
        # get_json may return None for invalid/missing JSON; default to empty dict
        data = request.get_json(silent=True) or {}
        template = data.get('template') if isinstance(data, dict) else None

        user_data = users.find_one({'_id': ObjectId(session['user_id'])})
        company = ''
        if user_data:
            company = str(user_data['company'])
            print("company", company)

        if not template:
            return jsonify({'success': False, 'message': 'template required'}), 400

        if template:
            email_template = orchestrate_flow(template)
            return jsonify({'template': email_template}), 200

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