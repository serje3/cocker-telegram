import io

from aiofiles import os, tempfile
from pydub import AudioSegment

from config import e_sound
from ms.audio_grpc.base import AudioEncoder
from utils import create_logger
from ms.audio_grpc.utils_ffmpeg import concatenate_audios_ffmpeg

logger = create_logger(__name__)

# Загружаем базовый звук (буква "э")
base = AudioSegment.from_file(e_sound)

# Алфавит + пробел
alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя "


def generate_pitch_map():
    base_index = alphabet.index("э")
    total = len(alphabet)
    pitch_map = {}

    for i, ch in enumerate(alphabet):
        # шаг pitch в пределах 0.7–1.3
        relative = (i - base_index) / (total - 1)
        pitch = 1.0 + relative * 0.6  # ±0.3
        pitch_map[ch] = pitch

    return pitch_map


pitch_map = generate_pitch_map()


# Функция смены pitch (изменяет скорость)
def change_pitch(sound, pitch=1.0):
    new_frame_rate = int(sound.frame_rate * pitch)
    pitched = sound._spawn(sound.raw_data, overrides={'frame_rate': new_frame_rate})
    return pitched.set_frame_rate(sound.frame_rate)


class EEncoder(AudioEncoder):

    async def encode(self, input_str: str) -> bytes:
        segments = []

        for ch in input_str.lower():
            if ch not in pitch_map:
                continue  # пропустить неизвестные символы

            pitch = pitch_map[ch]
            seg = change_pitch(base, pitch)
            segments.append(seg)

        result = sum(segments)

        # Возврат в виде байтов
        buffer = io.BytesIO()
        result.export(buffer, format="ogg")
        return buffer.getvalue()
