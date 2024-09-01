import os
from pathlib import Path

from dotenv import load_dotenv

BASE_PATH = Path(__file__).resolve().parents[0]

load_dotenv(BASE_PATH / '.env')

TOKEN = os.getenv('BOT_TOKEN')

nazhor_adjectives = []  # lazy loading from file

base_food_api_url = os.getenv("FOOD_AI_API")
fart_directory = BASE_PATH / 'data/farts/'

reload_reaction = "🍌"
ALLOWED_CHATS = set()  # lazy loading from db

LOG_CHAT = 426004046
