from lib.furina import Furina, isPrivate
import time

async def Ping(msg, match, client):
    start = time.time()
    ping_msg = await msg.reply("**Pinging...**")
    end = time.time()
    ms = round((end - start) * 1000, 2)
    await ping_msg.edit(f"**Pong!** `{ms}ms`")

Furina({
    "pattern": "ping$",
    "fromMe": isPrivate,
    "desc": "Test bot responsiveness",
    "type": "utils"
}, Ping)
