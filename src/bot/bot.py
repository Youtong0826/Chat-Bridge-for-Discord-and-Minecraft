from re import findall
from discord import Bot
from setting import Setting

class Bot(Bot):
    def __init__(self, description=None, *args, **options):
        super().__init__(description, *args, **options)
        
    @property
    def setting(self):
        return Setting()

    @staticmethod
    def is_emoji(content: str):
        return bool(findall("<:\w+:\d+>|<\w+:\w+:\d+>", content))