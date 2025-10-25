# initial starting file {everyting will be callable as a library}
from flask import request
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import time
import requests
import os

load_dotenv()

from routes.routes import app

if __name__ == '__main__':
    app.run(debug=True, port=8080)