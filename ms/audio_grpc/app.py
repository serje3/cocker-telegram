import asyncio
import multiprocessing
from concurrent import futures
from typing import Generator, AsyncIterator

import grpc

from fart_encoding import FartEncoder
from proto import audio_service_pb2 as pb2, audio_service_pb2_grpc as pb2_grpc
from utils import create_logger

logger = create_logger(__name__)


# Пример функции создания аудио
async def generate_audio_from_text(text) -> AsyncIterator[bytes]:
    encoder = FartEncoder()
    # return await encoder.encode_to_bytes(text)
    yield encoder.aencode_to_bytes(text)


class AudioService(pb2_grpc.AudioServiceServicer):
    async def GenerateFartAudio(self, request, context):
        text = request.text

        async for chunk in generate_audio_from_text(text):
            logger.info("Returning chunk: %s", f"{len(chunk) / 1024 / 1024}")
            yield pb2.AudioResponse(audio_chunk=chunk)


async def serve():
    print('worker count', multiprocessing.cpu_count())
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_AudioServiceServicer_to_server(AudioService(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    print("Server started")
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        pass
    finally:
        print("Shutting down")
        await server.stop(None)


if __name__ == '__main__':
    logger.info("Starting server")
    asyncio.run(serve())
