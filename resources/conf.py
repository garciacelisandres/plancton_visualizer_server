from os import environ

from dotenv import load_dotenv
load_dotenv(dotenv_path="../.env")


class Config:
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB = {
        "URL": environ.get("DATABASE_URL"),
        "DATABASE": environ.get("DATABASE_NAME")
    }
    DOWNLOAD = {
        "SAVE_PATH": environ.get("DOWNLOAD_SAVE_PATH"),
        "LINK_ELEMENT_ID": environ.get("DOWNLOAD_LINK_ELEMENT_ID"),
        "DOWNLOAD_URL": environ.get("DOWNLOAD_URL")
    }
    LOAD = {
        "DESTINATION_DIR": environ.get("LOAD_DESTINATION_DIR")
    }


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    APP_ENV = 'testing'
    WTF_CSRF_ENABLED = False
    MONGODB = {
        "URL": environ.get("DATABASE_URL"),
        "DATABASE": environ.get("TEST_DATABASE_NAME")
    }


class ProductionConfig(Config):
    FLASK_ENV = "production"
    MONGODB = {
        "URL": environ.get("DATABASE_URL"),
        "DATABASE": environ.get("DATABASE_NAME")
    }
    DOWNLOAD = {
        "SAVE_PATH": environ.get("DOWNLOAD_SAVE_PATH"),
        "LINK_ELEMENT_ID": environ.get("DOWNLOAD_LINK_ELEMENT_ID"),
        "DOWNLOAD_URL": environ.get("DOWNLOAD_URL")
    }
    LOAD = {
        "DESTINATION_DIR": environ.get("LOAD_DESTINATION_DIR")
    }


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
