from db.client import db
from db.models import CustomInstruction

custom_instructions_collection = db['custom_instructions']


async def insert_instruction(chat_id: int, instruction: str):
    await custom_instructions_collection.find_one_and_replace({'chat_id': chat_id},
                                                              {'chat_id': chat_id, 'instruction': instruction,
                                                               'enabled': True},
                                                              upsert=True)


async def find_instruction(chat_id: int) -> CustomInstruction | None:
    return await custom_instructions_collection.find_one({'chat_id': chat_id})


async def enable_instruction(chat_id: int) -> None:
    await custom_instructions_collection.find_one_and_update({'chat_id': chat_id}, {"$set": {'enabled': True}})


async def disable_instruction(chat_id: int) -> None:
    await custom_instructions_collection.find_one_and_update({'chat_id': chat_id}, {"$set": {'enabled': False}})
