import os
from flask import Flask
from flask_restx import Api


project_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
api = Api(app)

from app.module.controller import *