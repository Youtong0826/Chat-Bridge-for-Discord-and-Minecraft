from typing import (
    TypedDict,
    Union
)

class MessageData(TypedDict):
    body: dict[str, Union[str, int]]
    header: dict[str, Union[str, int]]

class Message:
    def __init__(self, data: MessageData) -> None:
        self.body = data.get("body")
        self.header = data.get("header")

    