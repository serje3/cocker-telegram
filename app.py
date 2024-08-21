import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import ALLOWED_CHATS, TOKEN  # MUST BE CALLED. There envs is loaded
from db.hooks import get_allowed_chats
from routers.donate import donate_router
from routers.food.router import food_router
from routers.help import help_router
from routers.start import start_router

dp = Dispatcher()
dp.include_router(start_router)
dp.include_router(help_router)
dp.include_router(donate_router)
dp.include_router(food_router)


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    docs = await get_allowed_chats()
    ALLOWED_CHATS.update(docs)

    print("Allowed chats is", ALLOWED_CHATS)

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook()

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.getLevelName(getenv('LOG_LEVEL', 'INFO')), stream=sys.stdout)
    asyncio.run(main())
