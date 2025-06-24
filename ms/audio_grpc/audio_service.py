from typing import AsyncIterator

from ms.audio_grpc.e_encoding import EEncoder
from ms.audio_grpc.fart_encoding import FartEncoder
from utils import create_logger
from proto import audio_service_pb2 as pb2, audio_service_pb2_grpc as pb2_grpc

logger = create_logger(__name__)


class AudioService(pb2_grpc.AudioServiceServicer):
    async def GenerateFartAudio(self, request, context):
        text = request.text

        async for chunk in FartEncoder().aencode_to_bytes(text):
            logger.info("Returning chunk: %s", f"{len(chunk) / 1024 / 1024}")
            yield pb2.AudioResponse(audio_chunk=chunk)

    async def GenerateEAudio(self, request, context):
        text = request.text

        async for chunk in EEncoder().aencode_to_bytes(text):
            logger.info("Returning chunk: %s", f"{len(chunk) / 1024 / 1024}")
            yield pb2.AudioResponse(audio_chunk=chunk)
