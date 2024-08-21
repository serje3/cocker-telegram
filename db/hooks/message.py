from aiogram.types import Message

from db.client import db
from db.models import Message as MessageMongoModel

messages_collection = db['messages']


async def insert_message(message: Message) -> bool:
    if (await retrieve_message(message.chat.id, message.message_id)) is not None:
        return False
    document = {
        'message_id': message.message_id,
        'chat_id': message.chat.id,
        'message_text': message.text,
        'photo': [photo.model_dump() for photo in message.photo]
    }
    result = await messages_collection.insert_one(document)
    return result.acknowledged


async def retrieve_message(chat_id: int, message_id: int) -> MessageMongoModel:
    document = await messages_collection.find_one({'chat_id': chat_id, 'message_id': message_id})
    return document
