import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_babel import Babel
from flask import request
from flask_moment import Moment
from elasticsearch import Elasticsearch

db = SQLAlchemy()
migrate = Migrate()
encrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None
    db.init_app(app)
    migrate.init_app(app, db)
    encrypt.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    from project.users.routes import users
    from project.messages.routes import messages
    from project.contacts.routes import contacts
    app.register_blueprint(users)
    app.register_blueprint(messages)
    app.register_blueprint(contacts)
    if not app.debug and not app.testing:
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/clone160by2.log', maxBytes=10240,backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('clone160by2 startup')

    return app
