import io
import re
from typing import List, Tuple

import aiogram
from aiogram import Router
from aiogram.types import MessageReactionUpdated, BufferedInputFile
from pydub import AudioSegment, effects

from config import fart_directory
from db.hooks.message import retrieve_message
from utils import filter_by_trigger_emoji, filter_only_allowed_chats

fart_router = Router(name=__name__)

fart_alphabet = {
    'а': 1,
    'б': 2,
    'в': 3,
    'г': 4,
    'д': 5,
    'е': 6,
    'ё': 7,
    'ж': 8,
    'з': 9,
    'и': 10,
    'й': 11,
    'к': 12,
    'л': 13,
    'м': 14,
    'н': 15,
    'о': 16,
    'п': 17,
    'р': 18,
    'с': 19,
    'т': 20,
    'у': 21,
    'ф': 22,
    'х': 23,
    'ц': 24,
    'ч': 25,
    'ш': 26,
    ' ': 27,  # Пробел
    'щ': 28,
    'ъ': 29,
    'ы': 30,
    'ь': 31,
    'э': 32,
    'ю': 33,
    'я': 34,
    '0': 35,
    '1': 36,
    '2': 37,
    '3': 38,
    '4': 39,
    '5': 40,
    '6': 41,
    '7': 42,
    '8': 43,
    '9': 44,
    '.': 27
}

fart_audio_segments: Tuple = tuple(AudioSegment.from_mp3(fart_directory / f'{i}.mp3') for i in range(1, 45))


# Функция предобработки строки
def preprocess_string(input_string):
    # Приведение к нижнему регистру
    input_string = input_string.lower()
    # Удаление спецсимволов (оставляем только русские буквы, пробелы и цифры)
    input_string = re.sub(r'[^а-я0-9 .ё]', '', input_string)
    # Преобразование строки в список символов
    char_list = list(input_string)
    return char_list


def alphabet_values(input_str) -> List[int]:
    char_list = preprocess_string(input_str)
    print('preprocessed', ''.join(char_list))
    return [fart_alphabet[char] for char in char_list]


async def fart_encoding(text: str, chat_id: int, bot: aiogram.Bot, reply_to_message_id: int = None):
    encoded_text_nums = alphabet_values(text[:300]) # temporary
    result_audio_segment: AudioSegment | None = None
    for num in encoded_text_nums:
        if not result_audio_segment:
            result_audio_segment = fart_audio_segments[num - 1]
            continue
        result_audio_segment += fart_audio_segments[num - 1]

    print(result_audio_segment)

    if not result_audio_segment:
        print('not enough audio segments')
        return

    normalized_audio_segment = effects.normalize(result_audio_segment)

    with io.BytesIO() as audio_buffered_file:
        normalized_audio_segment.export(audio_buffered_file, format="mp3")

        audio_bytes: bytes = audio_buffered_file.read()

        audio_size_in_mb = (len(audio_bytes) / 1024) / 1024

        print((len(audio_bytes) / 1024) / 1024, 'mb')

        if audio_size_in_mb >= 50:
            audio_bytes = audio_bytes[:49 * 1024 * 1024]

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
