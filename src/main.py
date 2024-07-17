import logging
from os import getenv
from dotenv import load_dotenv

from discord import Intents
from bot import Bot

load_dotenv()

logger = logging.getLogger("Discord")
logger.setLevel(logging.INFO)

bot = Bot(intents=Intents.all())

@bot.event
async def on_ready():
    logger.info(">> Bot is online <<")

if __name__ == "__main__":
    bot.load_extension("bot.message")
    bot.run(getenv("TOKEN"))
    
