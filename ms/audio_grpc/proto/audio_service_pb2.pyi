from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TextInputRequest(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...

class AudioResponse(_message.Message):
    __slots__ = ("audio_chunk",)
    AUDIO_CHUNK_FIELD_NUMBER: _ClassVar[int]
    audio_chunk: bytes
    def __init__(self, audio_chunk: _Optional[bytes] = ...) -> None: ...
