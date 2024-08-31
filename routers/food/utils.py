import asyncio.exceptions
import os
import random
from typing import Tuple

import aiohttp
from aiogram import F, Bot
from aiogram.enums import ChatType
from aiogram.types import File, ReactionTypeEmoji
from aiogram.utils.chat_action import ChatActionSender

from config import reload_reaction, nazhor_adjectives, base_food_api_url
from db.hooks.analyzed_messages import set_message_analyzed, set_message_not_analyzed
from db.hooks.custom_instructions import find_instruction
from utils import filter_by_trigger_emoji

filter_by_trigger_emoji_reaction = filter_by_trigger_emoji(reload_reaction)


async def handle_food_analyze(bot: Bot, chat_id: int, message_id: int, file_id: str, skip_food_checking=False) -> None:
    file: File = await bot.get_file(file_id)
    print(file)

    if skip_food_checking or await predict_is_food(file):
        if not (await set_message_analyzed(chat_id, message_id)):
            return
        await bot.set_message_reaction(chat_id, message_id, [ReactionTypeEmoji(emoji="🤔")])

        try:
            async with ChatActionSender.typing(bot=bot, chat_id=chat_id):
                resp, status = await analyze_food(file.file_path, chat_id)
        except asyncio.exceptions.TimeoutError as e:
            status = None
            print('TIMEOUT CALLED: ' + str(e))
        if status == 200:
            await bot.send_message(chat_id, resp['content'], reply_to_message_id=message_id)
        else:
            await bot.send_message(chat_id, f"{random.choice(nazhor_adjectives)} НАЖООООООР",
                                   reply_to_message_id=message_id)
            await set_message_not_analyzed(chat_id, message_id)
        await bot.set_message_reaction(chat_id, message_id, [])
    else:
        print('no food')
        chat = await bot.get_chat(chat_id)
        if chat.type == ChatType.PRIVATE:
            await bot.send_message(chat_id,
                                   f"Это не похоже на нажор. Если я не прав киньте на картиночку реакцию {reload_reaction}")


async def analyze_food(file_path: str, chat_id: int) -> Tuple[dict, int] | Tuple[str, int]:
    opt_kwargs = {}

    if instruction_doc := await find_instruction(chat_id):
        if instruction_doc['enabled']:
            opt_kwargs['instructions'] = instruction_doc['instruction']

    if base_food_api_url is None:
        print("WARNING base_food_api_url is None")
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{base_food_api_url}/analyze", json={
            "file_path": file_path,
            "chat_id": chat_id,
            **opt_kwargs
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
