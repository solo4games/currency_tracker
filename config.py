import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASS: str = os.getenv("DB_PASS", "password")
    DB_NAME: str = os.getenv("DB_NAME", "postgres")

    DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    API_KEY = os.getenv("EXCHANGERATE_API_KEY", "")
    API_BASE_URL = "https://api.exchangerate-api.com/v4/latest"
    REQUEST_INTERVAL_MINUTES = int(os.getenv("REQUEST_INTERVAL", "5"))


    LOG_DIR = Path("logs")
    LOG_FILE = LOG_DIR / "errors.log"
    LOG_LEVEL = logging.INFO

    @classmethod
    def setup_logging(cls) -> None:
        cls.LOG_DIR.mkdir(exist_ok=True)

        error_handler = RotatingFileHandler(
            cls.LOG_FILE,
            maxBytes=10_485_760,
            backupCount=5,
            encoding="utf-8"
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))


        logger = logging.getLogger()
        logger.setLevel(cls.LOG_LEVEL)
        logger.addHandler(error_handler)


        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%H:%M:%S"
        ))
        logger.addHandler(console_handler)