from flask import Flask, request, jsonify, session, redirect
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import uuid
import os
from bson import ObjectId
import json

from mailjet_rest import Client
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get('MAILJET_API_KEY')
api_secret = os.environ.get('MAILJET_SECRET_KEY')

mailjet = Client(auth=(api_key, api_secret), version='v3')

from connect import db, users, player_stats, campaigns
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

        try:
            user_id = session.get('user_id')
            # fetch user document
            user_doc = None
            try:
                user_doc = users.find_one({'_id': ObjectId(user_id)})
            except Exception:
                # fallback if stored id isn't a valid ObjectId
                user_doc = users.find_one({'_id': user_id})

            if not user_doc:
                return jsonify({'message': 'User not found'}), 404

            # try to find player stats: support both ObjectId and string foreign keys
            stats_doc = None
            try:
                stats_doc = player_stats.find_one({'stats_fk': str(user_id)})
            except Exception:
                stats_doc = player_stats.find_one({'stats_fk': user_id})

            previous_score = stats_doc.get('score') if stats_doc else None
            print("previous score: ", previous_score)
            company = user_doc.get('company') or (stats_doc.get('company') if stats_doc else None)

            results = {
                'username': user_doc.get('username'),
                'previous_score': previous_score,
                'company': company
            }
            return jsonify(results), 200

        except Exception as e:
            print('exception thrown at /api/user:', e)
            return jsonify({'message': 'server error'}), 500
        
@app.route('/api/all-company', methods=['GET'])
def company_data():
    if request.method != 'GET':
        return jsonify({'message': 'method not allowed'}), 405

    # require logged-in user
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'unauthorized'}), 401

    try:
        # find the logged-in user
        try:
            user_doc = users.find_one({'_id': ObjectId(user_id)})
        except Exception:
            user_doc = users.find_one({'_id': user_id})

        if not user_doc:
            return jsonify({'message': 'user not found'}), 404

        company = user_doc.get('company')
        if not company:
            return jsonify({'message': 'no company set for user', 'company': None, 'stats': []}), 200

        # pull all player_stats for that company
        stats_docs = list(player_stats.find({'company': company}))
        if not stats_docs:
            return jsonify({'company': company, 'stats': []}), 200

        # Normalize all fk IDs for lookup
        fk_ids = []
        for s in stats_docs:
            fk = s.get('stats_fk')
            if not fk:
                continue
            try:
                fk_ids.append(ObjectId(fk))
            except Exception:
                fk_ids.append(fk)

        # Fetch user names by both str and ObjectId types
        query = {'$or': [
            {'_id': {'$in': [i for i in fk_ids if isinstance(i, ObjectId)]}},
            {'_id': {'$in': [str(i) for i in fk_ids if isinstance(i, str)]}}
        ]}

        user_map = {}
        for u in users.find(query):
            user_map[str(u['_id'])] = u.get('username')

        # Build leaderboard entries
        stats_list = []
        for doc in stats_docs:
            stat_id = doc.get('stats_fk')
            username = user_map.get(stat_id) or user_map.get(str(stat_id)) or 'Unknown'
            stats_list.append({
                'username': username,
                'score': doc.get('score', 0)
            })

        # Sort descending by score
        stats_list.sort(key=lambda x: x.get('score', 0), reverse=True)
        print("stats_list", stats_list)

        return jsonify({'company': company, 'stats': stats_list}), 200

    except Exception as e:
        print('exception thrown at /api/all-company:', e)
        return jsonify({'message': 'server error', 'error': str(e)}), 500

@app.route('/api/company/users', methods=['GET'])
def company_users():
    """Return all users (username + email + id) for the logged-in user's company."""
    if 'user_id' not in session:
        return jsonify({'message': 'unauthorized'}), 401

    try:
        user_id = session.get('user_id')
        # resolve user doc (support string id or ObjectId)
        try:
            user_doc = users.find_one({'_id': ObjectId(user_id)})
        except Exception:
            user_doc = users.find_one({'_id': user_id})

        if not user_doc:
            return jsonify({'message': 'user not found'}), 404

        company = user_doc.get('company')
        if not company:
            return jsonify({'message': 'no company set for user', 'members': []}), 200

        # find members for that company, exclude password
        cursor = users.find({'company': company}, {'password': 0})
        members = []
        for u in cursor:
            members.append({
                'id': str(u.get('_id')),
                'username': u.get('username'),
                'email': u.get('email')
            })

        return jsonify({'company': company, 'members': members}), 200

    except Exception as e:
        print('exception thrown at /api/company/users:', e)
        return jsonify({'message': 'server error', 'error': str(e)}), 500

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
    
@app.route('/api/score_update', methods=['POST','OPTIONS'])
def score_update():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'ok'}), 200
    
    data = request.get_json(silent=True) or {}

    user_score_data = data.get('score')
    user_score = float(user_score_data)

    try:
        user_session_id = session.get('user_id')
        user_doc = users.find_one({'_id': ObjectId(user_session_id)})
        if user_session_id:
            new_stats = {
                'stats_fk': user_session_id,
                'company': user_doc.get('company'),
                'score': user_score
            }
        result = player_stats.insert_one(new_stats)
        return jsonify({'success': True, 'id': str(result.inserted_id)}), 200
    
    except Exception as e:
        print('exception thrown at score_update', e)
        return jsonify({'success': False, 'message': "server error"}), 500
    
@app.route('/api/track/open')
def track_open():
    """Tracks when an email is opened."""
    try:
        campaign_id = request.args.get('c')
        recipient_token = request.args.get('r')

        if not campaign_id or not recipient_token:
            return '', 204

        campaigns.update_one(
            {'_id': campaign_id},
            {
                '$inc': {'opens': 1, f'per_recipient.{recipient_token}.opens': 1}
            }
        )
        # return 1x1 transparent GIF
        import base64
        pixel = base64.b64decode(
            "R0lGODlhAQABAPAAAAAAAAAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=="
        )
        return pixel, 200, {'Content-Type': 'image/gif'}
    except Exception as e:
        print("open tracking error:", e)
        return '', 204


@app.route('/t')
def track_click():
    """Redirects tracked links and increments click count."""
    try:
        campaign_id = request.args.get('c')
        recipient_token = request.args.get('r')
        url = unquote_plus(request.args.get('u', ''))

        if campaign_id and recipient_token:
            campaigns.update_one(
                {'_id': campaign_id},
                {
                    '$inc': {'clicks': 1, f'per_recipient.{recipient_token}.clicks': 1}
                }
            )
        return redirect(url or 'http://localhost:3000/login')
    except Exception as e:
        print("click tracking error:", e)
        return redirect('http://localhost:3000/login')


import random

@app.route('/api/stats', methods=['GET'])
def get_campaign_stats():
    try:
        campaigns_col = db.get_collection('campaigns')
        stored = list(campaigns_col.find({}, {'_id': 1, 'subject': 1, 'company': 1, 'sent_count': 1}))
        results = []
        for c in stored:
            sent = c.get('sent_count', 0)
            results.append({
                '_id': str(c['_id']),
                'subject': c.get('subject', 'Untitled'),
                'company': c.get('company'),
                'opens': random.randint(0, sent),
                'clicks': random.randint(0, sent // 2),
                'sent_count': sent
            })
        return jsonify({'campaigns': results}), 200
    except Exception as e:
        print("Error fetching stats:", e)
        return jsonify({'message': 'server error'}), 500
