import os


class Config():
    SECRET_KEY = os.urandom(32)
    FIRST_STARTUP = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)


class Production(Config):
    FLASK_DEBUG = 0
    

class Development(Config):
    FLASK_DEBUG = 1
