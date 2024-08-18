import os
import random
from typing import Tuple

import aiohttp
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, PhotoSize, File, ReactionTypeEmoji

food_router = Router(name=__name__)

with open('./data/nazhor_adjectives.txt', 'r', encoding='utf-8') as f:
    nazhor_adjectives = f.read().split(', ')

base_food_api_url = os.getenv("FOOD_AI_API")


@food_router.message(F.photo.len() != 0, F.chat.id in [-1002070268098])
async def photo_handler(message: Message) -> None:
    print(message.chat)
    photo: PhotoSize = message.photo[-1]
    file: File = await message.bot.get_file(photo.file_id)
    print(file)
    is_food = await predict_is_food(file)

    if is_food:
        await message.react([ReactionTypeEmoji(emoji="🤔")])
        admins = await message.bot.get_chat_administrators(message.chat.id)
        mentions = []

        for admin in admins:
            user = admin.user
            if user.is_bot:
                continue
            mentions.append(f"[{user.full_name}](tg://user?id={user.id})")
        resp, status = await analyze_food(file.file_path, message.chat.id)
        if status == 200:
            await message.reply(resp['content'])
        else:
            await message.reply(
                f"{random.choice(nazhor_adjectives)} НАЖООООООР {' '.join(mentions if 'True' == os.getenv('ENABLE_MENTIONS', False) else [])}",
                parse_mode=ParseMode.MARKDOWN_V2)
        await message.react([])


async def analyze_food(file_path: str, chat_id: int) -> Tuple[dict, int] | Tuple[str, int]:
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{base_food_api_url}/analyze", json={
            "file_path": file_path,
            "chat_id": chat_id,
        }) as resp:
            print(resp.status, resp)
            if resp.status == 200:
                return await resp.json(), resp.status
            else:
                return await resp.text(), resp.status


async def predict_is_food(photo_file: File) -> bool:
    file_url = f'https://api.telegram.org/file/bot{os.getenv("BOT_TOKEN")}/{photo_file.file_path}'

    async with aiohttp.ClientSession() as tg_session:
        async with tg_session.get(file_url) as response:
            photo_bytes = await response.read()
            async with aiohttp.ClientSession() as food_api_session:
                form = aiohttp.FormData()
                form.add_field('file', photo_bytes, filename="image.jpg", content_type='image/jpeg')

                async with food_api_session.post(f'{base_food_api_url}/is-food', data=form) as response:
                    result = await response.json()
                    return result['is_food']
