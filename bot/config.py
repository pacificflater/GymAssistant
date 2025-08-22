# config.py
import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME", "FastAPI App")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    BOT_API_TOKEN = os.getenv("BOT_API_TOKEN")
    BACKEND_URL = os.getenv("BACKEND_URL")
    ALLOWED_USERS = os.getenv("ALLOWED_USERS")

    @property
    def is_debug(self):
        return self.DEBUG


settings = Settings()