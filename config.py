import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False
    TESTING = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'default': DevelopmentConfig
}
