import os
from config import Config
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_cors import CORS
from flask_praetorian import Praetorian
# import flask_praetorian
# from app.models import User


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
login = LoginManager()
cors = CORS()
guard = Praetorian()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    login.init_app(app)
    cors.init_app(app)
    with app.app_context():
        db.create_all()
    
    from app.models import User
    guard.init_app(app, User)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

from app import models