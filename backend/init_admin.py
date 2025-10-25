from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import uuid
import os
from bson import ObjectId

from connect import db, users

app = Flask(__name__)

app.secret_key = "im-adminning-it"

bcrypt = Bcrypt(app)

pw_hash = bcrypt.generate_password_hash("sjsuadminpw").decode('utf-8')

try:
    new_admin = {
        'username': "sjsu_admin",
        'password': pw_hash,
        'company': "san jose state university",
        'email': 'marlon.burog@sjsu.edu',
        'isAdmin': True
    }
    result = users.insert_one(new_admin)
    print(result)
except Exception as e:
    print(e)