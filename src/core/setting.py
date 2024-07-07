import json

def read_setting(name: str) -> dict:
    with open(f"{name}.json", "r") as f:
        return json.loads(f.read())

class Setting:

    @property
    def ws_setting(self):
      return read_setting("server")
  
    @property
    def dc_setting(self):
        return read_setting("discord")