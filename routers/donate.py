from typing import List

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from db.hooks import find_top_donates
from db.models import Donate

donate_router = Router(name=__name__)


@donate_router.message(Command("top_donates"))
async def top_donates(message: Message) -> None:
    """Команда для ахуенных людей"""

    donates: List[Donate] = await find_top_donates()

    top = "\n" + "\n".join([f"{i + 1}. {donates[i]['name']} - {donates[i]['amount']}{donates[i]['currency']}" for i in
                            range(len(donates))])

    await message.answer(f"""Топ донатчики вообще самые пиздатые ахуенные люди:{top}""")


@donate_router.message(Command("donate"))
async def donate(message: Message) -> None:
    await message.answer("Все деньги пойдут на поддержку бота потому шо он содержанка (каждый запрос стоит деняк)")
    await message.answer("https://pay.cloudtips.ru/p/47dd3faa")
