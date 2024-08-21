from typing import TypedDict, List

from typing_extensions import Required


class Photo(TypedDict):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: int


class Message(TypedDict, total=False):
    message_id: Required[int]
    chat_id: Required[int]
    message_text: str
    photo: Required[List[Photo]]


class Donate(TypedDict):
    name: str
    amount: int
    currency: str


class CustomInstruction(TypedDict, total=False):
    chat_id: Required[int]
    instruction: str
    enabled: Required[bool]
