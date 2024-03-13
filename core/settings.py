import json
from os import getenv
from dotenv import load_dotenv

load_dotenv()

URL_SEARCH = getenv('URL_SEARCH')
TOKEN = getenv('TELEGRAM_BOT_TOKEN')

DATABASE = getenv('PATH_DATABASE')



