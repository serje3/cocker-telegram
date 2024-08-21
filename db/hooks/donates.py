from typing import List

from db.client import db
from db.models import Donate

donates = db['donates']


async def find_top_donates(limit: int = 10) -> List[Donate]:
    cursor = donates.find().sort('amount', -1) \
        .limit(limit)
    docs: List[Donate] = await cursor.to_list(None)
    return docs
