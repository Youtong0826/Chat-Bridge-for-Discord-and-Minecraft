import logging

from threading import Thread
from uuid import uuid4
from asyncio import run_coroutine_threadsafe

from json import (
    loads, 
    dumps
)

from websocket_server import (
    WebsocketServer, 
    WebSocketHandler
)

from server.client import WebSocketClient
from bot import Bot

class WebSocketServerThreading:
    def __init__(self, bot: Bot, host: str = "127.0.0.1", port: int = 0, loglevel: logging = logging.WARN) -> None:
        self.server = WebsocketServer(host=host, port=port, loglevel=loglevel)
        self.client: WebSocketHandler = None
        self.bot = bot
        
    def active(self):
        @self.server.on_new_client()
        def new_client(client: WebSocketClient, server: WebsocketServer):
            print(f"a new client connected. id: {client["id"]} address: {client["address"][0]}:{client["address"][1]}")
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
        def message_received(client: WebSocketClient, server: WebsocketServer, message: dict):
            message = loads(message)
            data: dict = message.get("body")
            header: dict = message.get("header")
            print(message)
            if header.get("eventName") == "PlayerMessage" and data["type"] == "chat":
                channel = self.bot.get_channel(self.bot.setting.discord.get("channel"))
                run_coroutine_threadsafe(channel.send(self.bot.setting.discord["message"].format(user=data["sender"], msg=data["message"])), self.bot.loop)
        
        self.server.run_forever()
        
    def start(self):
        self.thread = Thread(target=self.active, name="websocket-server")
        self.thread.start()