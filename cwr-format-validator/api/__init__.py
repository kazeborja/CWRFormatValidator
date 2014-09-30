from flask import Flask

__author__ = 'Borja'

api_app = Flask(__name__)
api_app.config['DEBUG'] = True

from api import endpoints