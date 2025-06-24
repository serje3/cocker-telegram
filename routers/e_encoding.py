import aiogram
from aiogram import Router
from aiogram.types import BufferedInputFile, MessageReactionUpdated

from db.hooks.message import retrieve_message
from grpc_client import AudioGRPCClient
from utils import filter_only_allowed_chats, filter_by_trigger_emoji

e_router = Router(name=__name__)


async def e_encoding(text: str, chat_id: int, bot: aiogram.Bot, reply_to_message_id: int = None):
    async with AudioGRPCClient() as client:
        async for audio_bytes in client.generate_e_audio(text):
            await bot.send_voice(chat_id, BufferedInputFile(audio_bytes, 'my_honest_reaction.mp3'),
                                 reply_to_message_id=reply_to_message_id)


@e_router.message_reaction(filter_only_allowed_chats, filter_by_trigger_emoji("💊"))
async def message_reaction(updated: MessageReactionUpdated):
    message_mongo = await retrieve_message(updated.chat.id, updated.message_id)
    if not message_mongo:
        print("no message for fart encoding")
        return
    text = message_mongo['message_text']
    chat_id = message_mongo['chat_id']

    if not text or len(text) == 0:
        print('текст пустой')
        return
    print('длина текста', len(text))

    await e_encoding(text, chat_id, updated.bot, reply_to_message_id=updated.message_id)
