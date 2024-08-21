from db.client import db

custom_instructions_collection = db['custom_instructions']


async def insert_instruction(chat_id: int, instruction: str):
    await custom_instructions_collection.find_one_and_replace({'chat_id': chat_id},
                                                              {'chat_id': chat_id, 'instruction': instruction},
                                                              upsert=True)


async def find_instruction(chat_id: int) -> str | None:
    doc = await custom_instructions_collection.find_one({'chat_id': chat_id})
    return doc['instruction'] if doc else None
