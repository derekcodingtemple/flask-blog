# Initialize Flask app
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'warning'

    moment.init_app(app)

    from app.blueprints.account import account
    app.register_blueprint(account, url_prefix='/account')

    from app.blueprints.users import users
    app.register_blueprint(users, url_prefix='/users')

    with app.app_context():
        from app import routes

    return app

from app import models