from typing import List

from db.client import db

allowed_chats = db['allowed_chats']


async def get_allowed_chats() -> List[int]:
    cursor = allowed_chats.find()
    documents = await cursor.to_list(None)
    chats = [int(doc['chat_id']) for doc in documents]
    return chats


async def insert_allowed_chat(chat_id: int):
    if chat_id not in await get_allowed_chats():
        await allowed_chats.insert_one({'chat_id': chat_id})
