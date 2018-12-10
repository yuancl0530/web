class Config(object):
    DEBUG = False


class ProductionConfig(Config):
    DATA_URI = 'mysql://'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True