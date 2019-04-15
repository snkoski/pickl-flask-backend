from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
import os
from config import Config
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow


# app = Flask(__name__)
# app.config.from_object(Config)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# from app import models, routes

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main.bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

from app import models