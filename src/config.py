import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = True
TG_TOKEN = os.getenv('TG_TOKEN')
BASE_WEBHOOK_URL = os.getenv('NGROK_URL')
TG_WEBHOOK_PATH = '/telegram_webhook/'
TG_MY_TOKEN = TG_TOKEN.split(':')[1]
