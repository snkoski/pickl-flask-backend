from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from config import Config

app = Flask(__name__)
db = SQLAlchemy(app)

from app import models