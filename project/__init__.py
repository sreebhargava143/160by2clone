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
    migrate.init_app(app)
    encrypt.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    from project.users.routes import users
    from project.messages.routes import messages
    from project.contacts.routes import contacts
    app.register_blueprint(users)
    app.register_blueprint(messages)
    app.register_blueprint(contacts)

    return app
