import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = True
TG_TOKEN = os.getenv('TG_TOKEN')
BASE_WEBHOOK_URL = os.getenv('NGROK_URL')
TG_WEBHOOK_PATH = '/telegram_webhook/'
TG_MY_TOKEN = TG_TOKEN.split(':')[1]

POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
