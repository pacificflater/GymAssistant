# config.py
import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME", "FastAPI App")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    API_KEY = os.getenv("API_KEY")
    FOLDER_ID = os.getenv("FOLDER_ID")
    API_VERSION = os.getenv("API_VERSION", "v1")

    @property
    def is_debug(self):
        return self.DEBUG


settings = Settings()