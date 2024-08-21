from aiogram import Router
from aiogram.types import Message, PhotoSize, MessageReactionUpdated
from aiogram.utils.chat_action import ChatActionSender

from db.hooks.analyzed_messages import is_message_analyzed
from db.hooks.message import retrieve_message, insert_message
from db.models import Message as MessageMongo
from routers.food.utils import filter_only_allowed_chats, filter_by_trigger_emoji_reaction, handle_food_analyze, \
    filter_only_with_photos

food_router = Router(name=__name__)


@food_router.message_reaction(filter_only_allowed_chats, filter_by_trigger_emoji_reaction)
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

    async with ChatActionSender.typing(bot=updated.bot, chat_id=updated.chat.id):
        await handle_food_analyze(updated.bot, updated.chat.id, updated.message_id, photo['file_id'],
                                  skip_food_checking=True)


@food_router.message(filter_only_allowed_chats, filter_only_with_photos)
async def photo_handler(message: Message) -> None:
    await insert_message(message)
    photo: PhotoSize = message.photo[-1]
    print(f"Photo sended from: {message.from_user.username}")
    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        await handle_food_analyze(message.bot, message.chat.id, message.message_id, photo.file_id)
