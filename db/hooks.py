import os
from typing import List, Set

from aiogram.types import Message
from motor.motor_asyncio import AsyncIOMotorClient
from db.models import Message as MessageMongoModel

client = AsyncIOMotorClient(os.getenv('MONGO_CONNECTION_URL'), authSource='telegram')
db = client['telegram']
messages_collection = db['messages']
analyzed_messages_collection = db['analyzed_messages']
allowed_chats = db['allowed_chats']


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


async def set_message_analyzed(chat_id: int, message_id: int):
    if await is_message_analyzed(chat_id, message_id):
        return False
    document = {
        'message_id': message_id,
        'chat_id': chat_id,
    }
    result = await analyzed_messages_collection.insert_one(document)
    return result.acknowledged


async def set_message_not_analyzed(chat_id: int, message_id: int) -> bool:
    if await is_message_analyzed(chat_id, message_id):
        res = await analyzed_messages_collection.delete_one(
            {'chat_id': chat_id, 'message_id': message_id}
        )
        return res.acknowledged
    return False


async def is_message_analyzed(chat_id: int, message_id: int) -> MessageMongoModel:
    document = await analyzed_messages_collection.find_one({'chat_id': chat_id, 'message_id': message_id})
    return document is not None


async def get_allowed_chats() -> Set[int]:
    cursor = allowed_chats.find()
    documents = cursor.to_list(None)
    chats = {int(doc['chat_id']) for doc in documents}
    return chats


async def insert_allowed_chat(chat_id: int):
    if chat_id not in await get_allowed_chats():
        await allowed_chats.insert_one({'chat_id': chat_id})
