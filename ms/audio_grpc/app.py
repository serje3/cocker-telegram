import asyncio
import multiprocessing
from concurrent import futures
from typing import AsyncIterator

import grpc

from fart_encoding import FartEncoder
from ms.audio_grpc.audio_service import AudioService
from ms.audio_grpc.proto.audio_service_pb2_grpc import add_AudioServiceServicer_to_server
from utils import create_logger

logger = create_logger(__name__)



async def serve():
    logger.info('worker count ' + str(multiprocessing.cpu_count()))
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    add_AudioServiceServicer_to_server(AudioService(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    logger.info("Server started")
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        pass
    finally:
        logger.info("Shutting down")
        await server.stop(None)


if __name__ == '__main__':
    logger.info("Starting server")
    asyncio.run(serve())
