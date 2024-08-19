import asyncio
import logging
import sys

from dotenv import load_dotenv

from config import reload_reaction

load_dotenv()

from os import getenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from routers.food import food_router

TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()
dp.include_router(food_router)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    print(message.chat)
    await message.answer(f"Я тут я тут мужичок")


@dp.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(f"""Это бот, который анализирует ваш нажор. 
    Всё что нужно это скинуть ему фотографию предполагаемого нажора.
    Бот был разработан именно для бесед, а не для лс, поэтому он будет определять сначала нажор это или нет. Если нет - ответа не будет
    Чтобы запустить вручную анализ нажора нужно на сообщение с предполагаемым фото нажора повесить реакцию {reload_reaction}
    Разработчик @serJAYY. Бот сейчас тестируется и пока не готов к работе с большим количеством пользователей.
    Что точно известно - если он и будет доступен, то с платной подпиской, т.к. каждый запрос тратит деньги
    Инженер тех-поддержки @devilcattik""")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook()
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.getLevelName(getenv('LOG_LEVEL', 'INFO')), stream=sys.stdout)
    asyncio.run(main())
