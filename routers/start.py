from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import ALLOWED_CHATS, LOG_CHAT
from db.hooks.allowed_chats import get_allowed_chats, insert_allowed_chat

start_router = Router(name=__name__)

cache_sent_request = set()


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
    cache_sent_request.add(message.chat.id)


@start_router.callback_query(F.data == "chat_give_access")
async def chat_give_access(callback: CallbackQuery):
    chat_id_to_give = int(callback.message.text.split("ID:")[-1])
    await insert_allowed_chat(chat_id_to_give)
    await callback.answer(f"Доступ выдан {chat_id_to_give}")
    ALLOWED_CHATS.clear()
    ALLOWED_CHATS.update(await get_allowed_chats())
    await callback.bot.send_message(chat_id_to_give, "Вам дали потыкать меня")


@start_router.message(CommandStart())
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
        if message.chat.id not in cache_sent_request:
            await request_access(message)
        is_private = message.chat.type == 'private'
        await message.answer(
            f"Я пока не доступен для тебя, но я уже оповестил своего dungeon master о {'тебе' if is_private else 'вас'} и {'твоих' if is_private else 'ваших'} странных намерениях")


@start_router.message(Command("reload_allowed"), F.chat.id == LOG_CHAT)
async def reload_allowed(message: Message) -> None:
    ALLOWED_CHATS.clear()
    ALLOWED_CHATS.update(await get_allowed_chats())
