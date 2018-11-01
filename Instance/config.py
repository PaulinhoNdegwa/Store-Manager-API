import os


class Config(object):
    """This is the parent config class"""
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET")
    # DATABASE_URL = os.getenv("DATABASE_URL_APP")


class DevelopmentConfiguration(Config):
    """These are the development configurations"""
    DEBUG = True
    DATABASE_URL = os.getenv("DATABASE_URL_APP")


class TestingConfiguration(Config):
    """Configurations for testing with separate database"""
    TESTING = True
    DEBUG = True
    DATABASE_URL = os.getenv("DATABASE_URL_TEST")


class StagingConfiguration(Config):
    """Configuration for staging"""

    DEBUG = True


class ProductionConfiguration(Config):
    """"Configurations for production"""

    DEBUG = False
    TESTING = False


app_config = {
    "development": DevelopmentConfiguration,
    "testing": TestingConfiguration,
    "staging": StagingConfiguration,
    "production": ProductionConfiguration
}
