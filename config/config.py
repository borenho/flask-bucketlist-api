"""
This file contains the general settings that we want all environments to have by default
"""

import os

class Config(object):
    """
    Parent config class
    """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    """
    Development mode configurations
    """
    DEBUG = True


class TestingConfig(Config):
    """
    Testing mode configurations, with a separate database
    """
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_db'


class ProductionConfig(Config):
    """
    Production mode configurations
    """
    TESTING =  False
    DEBUG = False


# Export them all in one dict, for them to be imported in other files
app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
