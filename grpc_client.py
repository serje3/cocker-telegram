import abc
import os
from typing import Generator, Any, AsyncGenerator
from ms.audio_grpc.proto import audio_service_pb2 as pb2
from ms.audio_grpc.proto import audio_service_pb2_grpc as pb2_grpc

import grpc


class GRPCClient(abc.ABC):
    SERVER_ADDRESS = os.getenv('AUDIO_GRPC_SERVER')

    async def __aenter__(self):
        self.channel = grpc.aio.insecure_channel(self.SERVER_ADDRESS, options=[
            ('grpc.max_receive_message_length', 50 * 1024 * 1024)  # 50 MB
        ])

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.channel.close()
        self.channel = None


class AudioGRPCClient(GRPCClient):
    async def _generate_audio(self, stream_func_name, text):
        if self.channel is None:
            raise ValueError('Channel is not opened')

        stub = pb2_grpc.AudioServiceStub(self.channel)
        async for response in getattr(stub, stream_func_name)(pb2.TextInputRequest(text=text)):
            yield response.audio_chunk

    def generate_fart_audio(self, text) -> AsyncGenerator[Any, Any]:
        return self._generate_audio("GenerateFartAudio", text)

    def generate_e_audio(self, text) -> AsyncGenerator[Any, Any]:
        return self._generate_audio("GenerateEAudio", text)
