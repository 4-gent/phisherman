from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import uuid
import os
from bson import ObjectId

from connect import db, users

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
            print(data)
            # Minimal register implementation: create a user with a hashed password
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return jsonify({'success': False, 'message': 'username and password required'}), 400

            # avoid duplicate usernames
            existing = users.find_one({'username': username})
            if existing:
                return jsonify({'success': False, 'message': 'username already exists'}), 409

            pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = {
                'username': username,
                'password': pw_hash
            }
            result = users.insert_one(new_user)
            return jsonify({'success': True, 'id': str(result.inserted_id)}), 201
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

            if not username or not password:
                return jsonify({'success': False, 'message': 'username and password required'}), 400

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
            session['user_id'] = str(user.get('_id'))
            return jsonify({'success': True, 'username': username}), 200
        except Exception as e:
            print("exception thrown at login: ", e)
            return jsonify({'success': False, 'message': 'server error'}), 500