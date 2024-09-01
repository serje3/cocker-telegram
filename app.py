import asyncio
import logging
import sys
from os import getenv

from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import ALLOWED_CHATS, nazhor_adjectives  # MUST BE CALLED FIRST. There envs is loaded
from db.hooks.allowed_chats import get_allowed_chats
from db.hooks.message import insert_message
from routers.donate import donate_router
from routers.fart_encoding import fart_router
from routers.food.router import food_router, photo_handler as food_photo_handler
from routers.help import help_router
from routers.instructions import instructions_router
from routers.start import start_router
from utils import filter_only_allowed_chats, get_bot

dp = Dispatcher()
dp.include_routers(start_router,
                   help_router,
                   donate_router,
                   food_router,
                   instructions_router,
                   fart_router)


@dp.message(filter_only_allowed_chats)
async def on_message(message: Message):
    await insert_message(message)
    if message.photo is not None and len(message.photo) != 0:
        await food_photo_handler(message)


@dp.message(Command("cancel"))
async def cancel_command(message: Message, state: FSMContext) -> None:
    """
        Allow user to cancel any action
        """
    current_state = await state.get_state()
    if current_state is None:
        return

    print(f"Cancelling state {current_state}")
    await state.clear()
    await message.answer(
        "Отменено",
    )


async def main() -> None:
    with open('./data/nazhor_adjectives.txt', 'r', encoding='utf-8') as f:
        nazhor_adjectives.extend(f.read().split(', '))

    # Initialize Bot instance with default bot properties which will be passed to all API calls
    docs = await get_allowed_chats()
    ALLOWED_CHATS.update(docs)

    print("Allowed chats is", ALLOWED_CHATS)
    bot = get_bot()
    await bot.delete_webhook()

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.getLevelName(getenv('LOG_LEVEL', 'INFO')), stream=sys.stdout)
    asyncio.run(main())
