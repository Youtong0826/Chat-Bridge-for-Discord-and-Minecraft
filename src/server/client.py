from typing import Tuple, TypedDict
from websocket_server import WebSocketHandler

class WebSocketClient(TypedDict):
    id: int
    handler: WebSocketHandler
    address: Tuple[str, int]
    