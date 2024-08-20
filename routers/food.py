import os
import random
from typing import Tuple

import aiohttp
from aiogram import Router, F, Bot
from aiogram.enums import ChatType
from aiogram.types import Message, PhotoSize, File, ReactionTypeEmoji, MessageReactionUpdated

from config import reload_reaction, base_food_api_url, nazhor_adjectives, ALLOWED_CHATS
from db.models import Message as MessageMongo
from db.hooks import insert_message, retrieve_message, set_message_analyzed, is_message_analyzed, \
    set_message_not_analyzed

food_router = Router(name=__name__)

filter_by_chat_id = F.chat.id.in_(ALLOWED_CHATS)
filter_by_trigger_emoji_reaction = F.new_reaction.func(
    lambda new_reaction: bool(len(list(filter(lambda reaction: reaction.emoji == reload_reaction, new_reaction)))))


@food_router.message_reaction(filter_by_chat_id, filter_by_trigger_emoji_reaction)
async def reload_food_analyze_by_reaction(updated: MessageReactionUpdated):
    if await is_message_analyzed(updated.chat.id, updated.message_id):
        return

    message: MessageMongo = await retrieve_message(updated.chat.id, updated.message_id)

    if message is None:
        print("WTF?? message does not exist")
        return
    photo = message['photo'][-1] if len(message['photo']) != 0 else None

    if photo is None:
        print("message without photo")
        return

    await handle_food_analyze(updated.bot, updated.chat.id, updated.message_id, photo['file_id'],
                              skip_food_checking=True)


@food_router.message(F.photo.len() != 0, filter_by_chat_id)
async def photo_handler(message: Message) -> None:
    await insert_message(message)
    print(message.chat)
    photo: PhotoSize = message.photo[-1]
    await handle_food_analyze(message.bot, message.chat.id, message.message_id, photo.file_id)


async def handle_food_analyze(bot: Bot, chat_id: int, message_id: int, file_id: str, skip_food_checking=False) -> None:
    file: File = await bot.get_file(file_id)
    print(file)

    if skip_food_checking or await predict_is_food(file):
        if not (await set_message_analyzed(chat_id, message_id)):
            return
        await bot.set_message_reaction(chat_id, message_id, [ReactionTypeEmoji(emoji="🤔")])

        resp, status = await analyze_food(file.file_path, chat_id)
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
