from aiogram import Router, F
from aiogram.client.session import aiohttp
from aiogram.types import MessageReactionUpdated
from aiogram.utils.chat_action import ChatActionSender

from config import base_food_api_url
from db.hooks.analyzed_messages import is_message_analyzed
from db.hooks.message import retrieve_message
from utils import filter_by_trigger_emoji, fetch
from db.models import Message as MessageMongo

words_router = Router(name=__name__)

filter_by_trigger_emoji_reaction = filter_by_trigger_emoji("💅")


@words_router.message_reaction(F.chat.id.in_([-1002070268098]), filter_by_trigger_emoji_reaction)
async def words_erection(updated: MessageReactionUpdated):
    message: MessageMongo = await retrieve_message(updated.chat.id, updated.message_id)
    if message is None or message.get('message_text', None) is None:
        print("WTF?? message does not exist for word reaction")
        return
    async with ChatActionSender.typing(bot=updated.bot, chat_id=updated.chat.id):
        response = await fetch(f"{base_food_api_url}/predict/words",
                               headers={'Content-Type': 'application/json'},
                               data={"content": message['message_text']})
        print(response)
        try:
            content = response['content']
        except KeyError:
            print('Чето пошло не так')
            await updated.bot.send_message(updated.chat.id, 'иди нахуй💅')
            return
        words = content.split(' ')
        text = ' '.join(words[:-2])
        await updated.bot.send_message(updated.chat.id, text, reply_to_message_id=updated.message_id)
