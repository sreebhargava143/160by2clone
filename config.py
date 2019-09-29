import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    LANGUAGES = os.environ.get('LANGUAGES')
    MESSAGE_API_KEY = os.environ.get('MESSAGE_API_KEY')
    MESSAGE_SECRET_KEY = os.environ.get('MESSAGE_SECRET_KEY')
    MESSAGE_USE_TYPE = os.environ.get('MESSAGE_USE_TYPE')
    SENDER_ID = "160by2"
    MESSAGE_URL = os.environ.get('MESSAGE_URL')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    MESSAGES_PER_PAGE = 5
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')