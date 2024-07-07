from uuid import uuid4
import logging
import json

from websocket_server import WebsocketServer, WebSocketHandler
from client import WebSocketClient

server = WebsocketServer(port=9001, loglevel=logging.INFO)

@server.on_new_client()
def new_client(client: WebSocketClient, server: WebsocketServer):
    print(f"a new client connected. id: {client["id"]} address: {client["address"][0]}:{client["address"][1]}")
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

@server.on_message_received()
def message_received(client: WebSocketClient, server: WebsocketServer, message: dict):
    print(message)

server.run_forever()    
