from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()
import asyncio
import logging
import sys

from os import getenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery

from routers.food import food_router
from config import reload_reaction, ALLOWED_CHATS, LOG_CHAT

from db.hooks import get_allowed_chats, insert_allowed_chat, client

TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()
dp.include_router(food_router)


async def request_access(message: Message):
    is_private = message.chat.type == 'private'
    text = f"""{message.chat.username if is_private else message.chat.title} запрашивает доступ к боту ID:{message.chat.id}"""

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Дать доступ",
        callback_data="chat_give_access")
    )
    await message.bot.send_message(LOG_CHAT, text,
                                   reply_markup=builder.as_markup())


@dp.callback_query(F.data == "chat_give_access")
async def chat_give_access(callback: CallbackQuery):
    chat_id_to_give = int(callback.message.text.split("ID:")[-1])
    await insert_allowed_chat(chat_id_to_give)


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
    if message.chat.id not in ALLOWED_CHATS:
        is_private = message.chat.type == 'private'
        await message.answer(
            f"Я пока не доступен для тебя, но я уже оповестил своего dungeon master о {'тебе' if is_private else 'вас'} и {'твоих' if is_private else 'ваших'} странных намерениях")


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

    ALLOWED_CHATS.update(await get_allowed_chats())

    print("Allowed chats is", ALLOWED_CHATS)

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook()

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.getLevelName(getenv('LOG_LEVEL', 'INFO')), stream=sys.stdout)
    asyncio.run(main())
