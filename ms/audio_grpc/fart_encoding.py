import abc
import io
import re
import time
from typing import Tuple, List, Generator

from pydub import AudioSegment, effects

from config import fart_directory
from utils import create_logger

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


class AudioEncoder(abc.ABC):
    @abc.abstractmethod
    def encode[T](self, input_obj: T) -> AudioSegment:
        pass


class FartEncoder(AudioEncoder):
    __FART_AUDIO_SEGMENTS: Tuple = tuple(AudioSegment.from_mp3(fart_directory / f'{i}.mp3') for i in range(1, 45))

    def __init__(self):
        self.audio = AudioSegment.empty()

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

    def encode(self, input_str: str) -> AudioSegment:
        encoded_text_nums = self._alphabet_values(input_str)
        result_audio_segment: AudioSegment | None = None
        for num in encoded_text_nums:
            if not result_audio_segment:
                result_audio_segment = self.__FART_AUDIO_SEGMENTS[num - 1]
                continue
            result_audio_segment += self.__FART_AUDIO_SEGMENTS[num - 1]

        print(result_audio_segment)

        if not result_audio_segment:
            print('not enough audio segments')
            return None

        normalized_audio_segment = effects.normalize(result_audio_segment)

        return normalized_audio_segment

    def encode_to_bytes(self, input_str: str, chunk_size=49 * 1024 * 1024) -> Generator[bytes, None, None]:
        start_time = time.time()
        encoded_audio_segment: AudioSegment = self.encode(input_str)

        if not encoded_audio_segment:
            return

        logger.info("Audio segment created with %s seconds", f"{time.time() - start_time}")

        with io.BytesIO() as audio_buffered_file:
            encoded_audio_segment.export(audio_buffered_file, format="mp3")

            audio_bytes: bytes = audio_buffered_file.read()

        logger.info("Size of this audio %s", f"{(len(audio_bytes) / 1024) / 1024} mb")

        for chunk_start in range(0, len(audio_bytes), chunk_size):
            yield audio_bytes[chunk_start: chunk_start + chunk_size]
