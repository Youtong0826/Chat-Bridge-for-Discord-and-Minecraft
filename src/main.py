import logging
import json

from uuid import uuid4
from os import getenv
from dotenv import load_dotenv
from discord import (
    Bot,
    Message,
    Intents
)

from core.server import WebSocketServerThreading
from core.setting import Setting

load_dotenv()

bot = Bot(intents=Intents.all())
setting = Setting()
websocket = WebSocketServerThreading(bot, setting.ws_setting["host"], setting.ws_setting["port"], logging.INFO)
@bot.event
async def on_ready():
    print(">> Bot is online <<")

@bot.event
async def on_message(msg: Message):
    if msg.author.bot: return
    
    if msg.channel.id == setting.dc_setting.get("channel"):
        websocket.client.send_message(json.dumps({  
	        "header": {
	        	"version": 1,
                "requestId": str(uuid4()),
	        	"messageType": "commandRequest",
                "messagePurpose": "commandRequest"
	        },
            "body": {
	        	"origin": {
	        		"type": "player"
	        	},
	        	"commandLine": 'tellraw @a {"rawtext":[{"text": "%s"}]}' % f"§9[Discord] §e{msg.author.name}§r: {msg.content}",
	        	"version": 1
	        },
        }))
    
if __name__ == "__main__":
    websocket.start()
    bot.run(getenv("TOKEN"))
