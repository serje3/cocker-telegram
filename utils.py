import json

import aiohttp
from aiogram import F

from config import ALLOWED_CHATS


async def fetch(url, headers=None, data=None, method="POST"):
    if data is not None:
        data = json.dumps(data)

    print("INTERNAL REQUEST:", method, url, data)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.request(
                    method=method, url=url, data=data, headers=headers
            ) as resp:
                return await resp.json()
        except Exception as e:
            return f"An error occurred: {e}"


filter_only_allowed_chats = F.chat.id.in_(ALLOWED_CHATS)
filter_only_with_photos = F.photo.len() != 0


def filter_by_trigger_emoji(reaction_str: str) -> bool:
    return F.new_reaction.func(
        lambda new_reaction: bool(len(list(filter(lambda reaction: reaction.emoji == reaction_str, new_reaction)))))
