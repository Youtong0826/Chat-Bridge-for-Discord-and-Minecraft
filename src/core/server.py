import logging
import json

from asyncio import run_coroutine_threadsafe
from threading import Thread
from uuid import uuid4
from websocket_server import WebsocketServer, WebSocketHandler
from discord import Bot
from core.client import WebSocketClient
from core.setting import Setting

class WebSocketServerThreading:
    def __init__(self, bot: Bot, host: str = "127.0.0.1", port: int = 0, loglevel: logging = logging.WARN) -> None:
        self.server = WebsocketServer(host=host, port=port, loglevel=loglevel)
        self.client: WebSocketHandler = None
        self.setting = Setting()
        self.bot = bot
        
    def active(self):
        @self.server.on_new_client()
        def new_client(client: WebSocketClient, server: WebsocketServer):
            print(f"a new client connected. id: {client["id"]} address: {client["address"][0]}:{client["address"][1]}")
            self.client = client["handler"]
            server.send_message(client, json.dumps({
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
            message = json.loads(message)
            data: dict = message.get("body")
            header: dict = message.get("header")

            if header.get("eventName") == "PlayerMessage" and not data.get("receiver") and not data["message"].startswith("§9[Discord]"):
                channel = self.bot.get_channel(self.setting.dc_setting.get("channel"))
                future = run_coroutine_threadsafe(channel.send(f"[Minecraft] {data["sender"]}: {data["message"]}"), self.bot.loop)
        
        self.server.run_forever()
        
    def start(self):
        self.thread = Thread(target=self.active, name="websocket-server")
        self.thread.start()