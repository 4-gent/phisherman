from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import uuid
import os
from bson import ObjectId

from connect import db, users
from mail.sender.sender import email_send

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

        return jsonify({'success': True, 'message': 'input received', 'template': template}), 200

    except Exception as e:
        print("exception thrown at campaign: ", e)
        return jsonify({'success': False, 'message': 'server error'}), 500