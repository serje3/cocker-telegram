import multiprocessing
from concurrent import futures
from typing import Generator

import grpc

from fart_encoding import FartEncoder
from proto import audio_service_pb2 as pb2, audio_service_pb2_grpc as pb2_grpc
from utils import create_logger

logger = create_logger(__name__)


# Пример функции создания аудио
def generate_audio_from_text(text) -> Generator[bytes, None, None]:
    encoder = FartEncoder()
    return encoder.encode_to_bytes(text)


class AudioService(pb2_grpc.AudioServiceServicer):
    def GenerateFartAudio(self, request, context):
        text = request.text

        for chunk in generate_audio_from_text(text):
            logger.info("Returning chunk: %s", f"{len(chunk) / 1024 / 1024}")
            yield pb2.AudioResponse(audio_chunk=chunk)


def serve():
    # Используем ProcessPoolExecutor вместо ThreadPoolExecutor для параллельной обработки
    print('worker count', multiprocessing.cpu_count())
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_AudioServiceServicer_to_server(AudioService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logger.info("Starting server")
    serve()
