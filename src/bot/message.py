import logging
from json import dumps
from uuid import uuid4

from discord import (
    Cog,
    Message,
)

from server import WebSocketServerThreading
from bot import Bot

class MessageEvents(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        
        self.websocket = WebSocketServerThreading(
            bot, 
            bot.setting.server["host"], 
            bot.setting.server["port"], 
            loglevel=logging.INFO
        )
        
        self.websocket.start()
        
    @Cog.listener()
    async def on_message(self, msg: Message):
        if msg.author.bot: return

        if msg.channel.id == self.bot.setting.discord.get("channel"):
            self.websocket.client.send_message(dumps({  
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
                    "commandLine": 'tellraw @a {"rawtext":[{"text": "%s"}]}' % self.bot.setting.minecraft["message"].format(
                        user=msg.author.global_name if msg.author.global_name else msg.author.name, 
                        msg=msg.content
                    ),
                    "version": 1
	            },
            }))
            
def setup(bot: Bot):
    bot.add_cog(MessageEvents(bot))