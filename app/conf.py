from os import environ


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


config_by_name = dict(
    dev=DevelopmentConfig
)
