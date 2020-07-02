# Initialize Flask app
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
import logging, os
from logging.handlers import SMTPHandler, RotatingFileHandler

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
    login_manager.login_view = 'account.login'
    login_manager.login_message_category = 'warning'

    moment.init_app(app)

    from app.blueprints.account import account
    app.register_blueprint(account, url_prefix='/account')

    from app.blueprints.users import users
    app.register_blueprint(users, url_prefix='/users')

    with app.app_context():
        from app import routes

        from app.blueprints.errors import errors
        app.register_blueprint(errors, url_prefix='/error')

    # Email Error Logging
    if not app.debug:
        server = app.config.get('MAIL_SERVER')
        username = app.config.get('MAIL_USERNAME')
        port = app.config.get('MAIL_PORT')
        password = app.config.get('MAIL_PASSWORD')
        use_tls = app.config.get('MAIL_USE_TLS')
        admins = app.config.get('ADMINS')

        if server:
            auth = None
            if username or password:
                auth = (username, password)
            secure = None
            if use_tls:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(server, port),
                fromaddr=f'noreply@{server}',
                toaddrs=admins,
                subject='Flask Blog Failure',
                credentials=auth,
                secure=secure
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            'logs/flask-blog.log',
            maxBytes=10240,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s [%(pathname)s:%(lineno)d]"))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Flask_Blog startup')
    return app

from app import models
