import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'ap3143pj2asdjf2134'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/tvFootball'


class TestingConfig(Config):
    TESTING = True
    travis = bool(os.environ.get('TRAVIS'))
    if travis:
        SQLALCHEMY_DATABASE_URI = ('postgresql://postgres@localhost/'
                                   'travis_ci_test')
    else:
        SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/tvFootball_test'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/tvFootball'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig

}
