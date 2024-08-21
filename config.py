import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

with open('./data/nazhor_adjectives.txt', 'r', encoding='utf-8') as f:
    nazhor_adjectives = f.read().split(', ')

base_food_api_url = os.getenv("FOOD_AI_API")

reload_reaction = "🍌"
ALLOWED_CHATS = set()

LOG_CHAT = 426004046
