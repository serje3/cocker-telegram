from db.client import db
from db.models import Message as MessageMongoModel

analyzed_messages_collection = db['analyzed_messages']


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
