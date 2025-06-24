import os
import re
from typing import List

from aiofiles import tempfile

from config import fart_directory
from ms.audio_grpc.base import AudioEncoder
from utils import create_logger
from ms.audio_grpc.utils_ffmpeg import concatenate_audios_ffmpeg

logger = create_logger(__name__)

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


class FartEncoder(AudioEncoder):

    # Функция предобработки строки
    def _preprocess_string(self, input_string):
        # Приведение к нижнему регистру
        input_string = input_string.lower()
        # Удаление спецсимволов (оставляем только русские буквы, пробелы и цифры)
        input_string = re.sub(r'[^а-я0-9 .ё]', '', input_string)
        # Преобразование строки в список символов
        char_list = list(input_string)
        return char_list

    def _alphabet_values(self, input_str: str) -> List[int]:
        char_list = self._preprocess_string(input_str)
        logger.info('preprocessed %s', ''.join(char_list))
        return [fart_alphabet[char] for char in char_list]

    async def encode(self, input_str: str) -> bytes:
        logger.info("starting encoding")
        encoded_text_nums = self._alphabet_values(input_str)
        file_pathes = list(map(lambda num: fart_directory / f"{num}.mp3", encoded_text_nums))
        logger.info("Starting ffmpeg process with %s symbols", len(encoded_text_nums))

        async with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', suffix='.txt') as temp_file:
            temp_filename = temp_file.name
            for file in file_pathes:
                await temp_file.write(f"file '{file}'\n")
        logger.info("created temp file with name %s", temp_filename)
        audio_bytes = b''

        try:
            audio_bytes = await concatenate_audios_ffmpeg(temp_filename)
        except Exception as e:
            logger.error(e)
        finally:
            os.remove(temp_filename)
            logger.info("removed temp file with name %s", temp_filename)

        logger.info("encoded audio %d", len(audio_bytes) != 0)

        return audio_bytes
