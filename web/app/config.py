import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    FB_APP_ID = os.environ.get("FB_APP_ID", None)
    if not FB_APP_ID:
        raise Exception("FB_APP_ID environment variable must be specified.")

    FB_APP_SECRET = os.environ.get("FB_APP_SECRET", None)
    if not FB_APP_SECRET:
        raise Exception("FB_APP_SECRET environment variable must be specified.")

    FB_MAX_EVENT_RESULTS = 100

    CSV_COLUMN_ORDER = ["name", "link", "street_address", "city", "state",\
            "start_date", "end_date", "description"]

    OUTPUT_TIMESTAMP_FORMAT = "%A, %B %d %Y %I:%M %p %z"

    ARG_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,

    "default": DevelopmentConfig
}
