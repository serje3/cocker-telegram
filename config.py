import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_PATH = Path(__file__). resolve().parents[0]

TOKEN = os.getenv('BOT_TOKEN')

with open('./data/nazhor_adjectives.txt', 'r', encoding='utf-8') as f:
    nazhor_adjectives = f.read().split(', ')

base_food_api_url = os.getenv("FOOD_AI_API")
fart_directory = BASE_PATH / 'data/farts/'

reload_reaction = "🍌"
ALLOWED_CHATS = set()

LOG_CHAT = 426004046
