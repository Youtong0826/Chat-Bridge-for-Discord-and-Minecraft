# Chat Bridge for Discord and Minecraft
不用任何插件，不用任何模組，不用任何 Add-on，只要原版世界就可以讓人們在 Discord 與 Minecraft 之間聊天 ! 

(僅限基岩版)

### 使用條件:
* Minecraft BE
* Python >= 3.8

### 使用方法:

#### 設定:

使用以下指令來下載所需套件
``` 
pip install -r requirements.txt 
```

在最外層創建 `.env` 檔案並寫入你的 Discord 機器人 Token
```
TOKEN = "Your Discord Bot Token"
```

接著可以到 `setting.json` 設定各項內容
```js
{
    "server": { // 主機位址
        "host": "127.0.0.1",
        "port": 9000
    },
    "discord": {
        "channel": 1259342904309321831, // dicsord 的頻道 id
        "message": "**[Minecraft]**  **` {user} `** : {msg}" // discord 端的訊息的樣板 {user} 是名字 {msg} 則是訊息
    },
    "minecraft": {
        "message": "§9[Discord] §e{user}§r: {msg}" // Minecraft 端的訊息樣板，同上
    }
}
```

最後進去 Minecraft 設定 -> `一般` -> `網路設定` -> `需要有加密的 WebSockets` 關掉 

#### 啟用:
設定完畢後執行 `src/main.py`，任何可以啟動 python 檔案的方法都行 
舉例:
```shell
cd D:\GitHub\Chat-Bridge-for-Discord-and-Minecraft
python src/main.py
```
成功的話會出現這些訊息
```shell
INFO:websocket_server.websocket_server:Listening on port 9000 for clients..
INFO:websocket_server.websocket_server:Starting BridgeWebSocketServer on main thread.
INFO:Discord:>> Bot is online <<
```

接著回到 Minecraft 世界，輸入指令 `/wsserver host:port` 或是 `/connect host:port` (e.g `/wsserver 127.0.0.1:9000`) 這樣就成功啦 !

備註: 需開啟作弊或是創造模式

#### 預覽:
![alt text](assets/chat1.png)

![alt text](assets/chat2.png)
