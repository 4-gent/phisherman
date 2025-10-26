# initial starting file {everyting will be callable as a library}
from flask import request
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import time
import requests
import os

from routes.routes import app
from config import config
from sockets.socket import socketio

if __name__ == '__main__':
    socketio.run(
        app,
        debug=config.FLASK_DEBUG,
        host=config.HOST,
        port=config.PORT
    )