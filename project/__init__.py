from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_babel import Babel
from flask import request
from flask_moment import Moment

# @babel.localeselector
# def get_locale():
#     return request.accept_languages.best_match(app.config['LANGUAGES'])

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
encrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
moment = Moment(app)
# babel = Babel(app)

from project.users.routes import users
from project.messages.routes import messages
from project.contacts.routes import contacts

app.register_blueprint(users)
app.register_blueprint(messages)
app.register_blueprint(contacts)
