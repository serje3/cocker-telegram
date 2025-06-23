import abc
from typing import Any

from pydub import AudioSegment


class AudioEncoder(abc.ABC):
    @abc.abstractmethod
    def encode(self, input_obj: Any) -> AudioSegment:
        pass