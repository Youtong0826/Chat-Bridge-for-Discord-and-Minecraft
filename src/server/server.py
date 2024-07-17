import logging
from threading import Thread
from uuid import uuid4
from asyncio import run_coroutine_threadsafe

from json import (
    loads, 
    dumps
)

from websocket_server import (
    WebsocketServer as WebSocketServer, 
    WebSocketHandler
)

from server.message import Message
from server.client import WebSocketClient
from bot import Bot

logger = logging.getLogger("Minecraft")

class BridgeWebSocketServer(WebSocketServer):
    def __init__(self, host: str = "127.0.0.1", port: int = 0, loglevel: logging = logging.WARNING, key=None, cert=None):
        super().__init__(host, port, loglevel, key, cert)
        logger.setLevel(loglevel)

    def _message_received_(self, handler, msg):
        return super()._message_received_(handler, Message(loads(msg)))

class BridgeThread:
    def __init__(self, bot: Bot, host: str = "127.0.0.1", port: int = 0, loglevel: logging = logging.WARN) -> None:
        self.server = BridgeWebSocketServer(host=host, port=port, loglevel=loglevel)
        self.client: WebSocketHandler = None
        self.bot = bot
        
    def __bool__(self) -> bool:
        return self.is_ready()

    def is_ready(self):
        return bool(self.client)

    def active(self):
        @self.server.on_new_client()
        def new_client(client: WebSocketClient, server: BridgeWebSocketServer):
            logger.info(f"a new client connected. id: {client["id"]} address: {client["address"][0]}:{client["address"][1]}")
            self.client = client["handler"]
            server.send_message(client, dumps({
                "header": {
                    "version": 1,                     
                    "requestId": str(uuid4()),           
                    "messageType": "commandRequest",  
                    "messagePurpose": "subscribe" 
                },
                "body": {
                    "eventName": "PlayerMessage"
                }
            }, indent=4))

        @self.server.on_message_received()
        def message_received(client: WebSocketClient, server: BridgeWebSocketServer, message: Message):
            if not message.header or not message.body:
                return
    
            if message.header.get("eventName") == "PlayerMessage" and message.body.get("type") == "chat":
                logger.info(f'received a message: "{message.body["message"]}" by user {message.body["sender"]}')
                channel = self.bot.get_channel(self.bot.setting.discord.get("channel"))
                run_coroutine_threadsafe(
                    channel.send(
                        self.bot.setting.discord["message"].format(
                            user=message.body["sender"], 
                            msg=message.body["message"]
                    )), 
                    self.bot.loop
                )
        
        self.server.run_forever()
        
    def start(self):
        self.thread = Thread(target=self.active, name="bridge")
        self.thread.start()
