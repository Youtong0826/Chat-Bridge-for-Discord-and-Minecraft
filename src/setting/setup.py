import json
from typing import TypedDict

from dataclasses import (
    dataclass, 
    field
)

def read_setting(name: str) -> dict:
    with open(f"setting.json", "r", encoding="utf-8") as f:
        return json.loads(f.read())[name]

class ServerDict(TypedDict):
    host: str
    port: int

class DiscordDict(TypedDict):
    channel: int
    message: str
    
class MinecraftDict(TypedDict):
    message: str

@dataclass
class Setting:
    server: ServerDict = field(default_factory=lambda: read_setting("server"))
    discord: DiscordDict = field(default_factory=lambda: read_setting("discord"))
    minecraft: MinecraftDict = field(default_factory=lambda: read_setting("minecraft"))