"""Application configuration centralization."""
import os


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change_this_secret")
    BASE_PATH = os.environ.get("BASE_PATH", "/smallqr")
    PORT = int(os.environ.get("PORT", 8002))
    COUNTER_FILE = os.environ.get("COUNTER_FILE", "qr_counter.txt")
    MAX_INPUT_LENGTH = int(os.environ.get("MAX_INPUT_LENGTH", 5000))
    DEFAULT_ERROR_LEVEL = "L"
    ALLOWED_ERROR_LEVELS = {"L", "M", "Q", "H"}
    # Use secure cookies by default in production; can be overridden via SECURE_COOKIES env
    _env = os.environ.get("FLASK_ENV", "production").lower()
    SECURE_COOKIES = os.environ.get("SECURE_COOKIES")
    if SECURE_COOKIES is None:
        SECURE_COOKIES = (_env == "production")
    else:
        SECURE_COOKIES = str(SECURE_COOKIES).strip() in {"1", "true", "yes", "on"}


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False


def get_config() -> type:
    env = os.environ.get("FLASK_ENV", "production").lower()
    if env == "development":
        return DevelopmentConfig
    return ProductionConfig
