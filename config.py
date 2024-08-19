import os


with open('./data/nazhor_adjectives.txt', 'r', encoding='utf-8') as f:
    nazhor_adjectives = f.read().split(', ')

base_food_api_url = os.getenv("FOOD_AI_API")

reload_reaction = "🍌"
ALLOWED_CHATS = (-1002070268098, -1002222522139)
