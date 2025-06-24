import abc
import time
from typing import Any, AsyncIterator

from utils import create_logger

logger = create_logger(__name__)


class AudioEncoder(abc.ABC):
    @abc.abstractmethod
    async def encode(self, input_str: str) -> bytes:
        pass

    async def aencode_to_bytes(self, input_str: str, chunk_size=49 * 1024 * 1024) -> AsyncIterator[bytes]:

        start_time = time.time()
        audio_bytes: bytes = await self.encode(input_str)
        if not audio_bytes or len(audio_bytes) == 0:
            return

        logger.info("Audio segment created with %s seconds", f"{time.time() - start_time}")

        logger.info("Size of this audio %s", f"{(len(audio_bytes) / 1024) / 1024} mb")

        for chunk_start in range(0, len(audio_bytes), chunk_size):
            yield audio_bytes[chunk_start: chunk_start + chunk_size]
