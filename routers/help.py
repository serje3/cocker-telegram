from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import reload_reaction

help_router = Router(name=__name__)


@help_router.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(f"""Это бот, который анализирует ваш нажор. 
    Всё что нужно это скинуть ему фотографию предполагаемого нажора.
    Бот был разработан именно для бесед, а не для лс, поэтому он будет определять сначала нажор это или нет. Если нет - ответа не будет
    Чтобы запустить вручную анализ нажора нужно на сообщение с предполагаемым фото нажора повесить реакцию {reload_reaction}
    Разработчик @serJAYY. Бот сейчас тестируется и пока не готов к работе с большим количеством пользователей.
    Что точно известно - если он и будет доступен, то с платной подпиской, т.к. каждый запрос тратит деньги
    Инженер тех-поддержки @devilcattik""")
