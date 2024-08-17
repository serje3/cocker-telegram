import os
import random

import aiohttp
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, PhotoSize, File

food_router = Router(name=__name__)

with open('./data/nazhor_adjectives.txt', 'r', encoding='utf-8') as f:
    nazhor_adjectives = f.read().split(', ')


@food_router.message(F.photo.len() != 0)
async def photo_handler(message: Message) -> None:
    photo: PhotoSize = message.photo[-1]
    print(message.photo)
    file: File = await message.bot.get_file(photo.file_id)
    print(file)
    is_food = await predict_is_food(file)

    if is_food:
        admins = await message.bot.get_chat_administrators(message.chat.id)
        mentions = []

        for admin in admins:
            user = admin.user
            if user.is_bot:
                continue
            mentions.append(f"[{user.full_name}](tg://user?id={user.id})")

        await message.reply(
            f"{random.choice(nazhor_adjectives)} НАЖООООООР {' '.join(mentions if 'True' == os.getenv('ENABLE_MENTIONS', False) else [])}",
            parse_mode=ParseMode.MARKDOWN_V2)


async def predict_is_food(photo_file: File) -> bool:
    file_url = f'https://api.telegram.org/file/bot{os.getenv("BOT_TOKEN")}/{photo_file.file_path}'

    async with aiohttp.ClientSession() as tg_session:
        async with tg_session.get(file_url) as response:
            photo_bytes = await response.read()
            async with aiohttp.ClientSession() as food_api_session:
                form = aiohttp.FormData()
                form.add_field('file', photo_bytes, filename="image.jpg", content_type='image/jpeg')

                async with food_api_session.post(f'{os.getenv("FOOD_AI_API")}/is-food', data=form) as response:
                    result = await response.json()
                    return result['is_food']
