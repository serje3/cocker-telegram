from typing import Generator

import aiogram
import grpc
from aiogram import Router
from aiogram.types import MessageReactionUpdated, BufferedInputFile, Message

from db.hooks.message import retrieve_message, insert_message
from ms.audio_grpc.proto import audio_service_pb2 as pb2
from ms.audio_grpc.proto import audio_service_pb2_grpc as pb2_grpc
from utils import filter_by_trigger_emoji, filter_only_allowed_chats
from routers.food.router import photo_handler as food_photo_handler

fart_router = Router(name=__name__)


class AudioGRPCClient:
    SERVER_ADDRESS = 'localhost:50051'

    async def generate_audio(self, text) -> Generator[bytes, None, None]:
        async with grpc.aio.insecure_channel(self.SERVER_ADDRESS, options=[
            ('grpc.max_receive_message_length', 50 * 1024 * 1024)  # 50 MB
        ]) as channel:
            print('подключен')
            stub = pb2_grpc.AudioServiceStub(channel)
            async for response in stub.GenerateFartAudio(pb2.TextInputRequest(text=text)):
                yield response.audio_chunk


async def fart_encoding(text: str, chat_id: int, bot: aiogram.Bot, reply_to_message_id: int = None):
    client = AudioGRPCClient()
    async for audio_bytes in client.generate_audio(text):
        await bot.send_voice(chat_id, BufferedInputFile(audio_bytes, 'my_honest_reaction.mp3'),
                             reply_to_message_id=reply_to_message_id)


# 💩
@fart_router.message_reaction(filter_only_allowed_chats, filter_by_trigger_emoji("💩"))
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

    await fart_encoding(text, chat_id, updated.bot, reply_to_message_id=updated.message_id)


@fart_router.message(filter_only_allowed_chats)
async def on_message(message: Message):
    await insert_message(message)
    if message.photo is not None and len(message.photo) != 0:
        await food_photo_handler(message)
