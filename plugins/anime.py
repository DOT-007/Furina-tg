from lib.furina import Furina, isPrivate
import requests
import random

async def Waifu(msg, match, client):
    try:
        res = requests.get("https://ironman.koyeb.app/ironman/waifu", timeout=10)
        data = res.json()
        if data.get("status") and "ironman" in data and "url" in data["ironman"]:
            img_url = data["ironman"]["url"]
            await client.send_photo(msg.chat.id, photo=img_url, caption="Here's your waifu!")
        else:
            await msg.reply("Failed to get image.")
    except Exception as e:
        await msg.reply(f"Error: {e}")


async def Aquote(msg, match, client):
    try:
        res = requests.get("https://ironman.koyeb.app/aquote", timeout=10)
        quotes = res.json()
        if isinstance(quotes, list) and quotes:
            quote = random.choice(quotes)
            await msg.reply(f"\"{quote['english']}\"\n\n" f"-{quote['character']} ({quote['anime']})")
        else:
            await msg.reply("No quotes found.")
    except Exception as e:
        await msg.reply(f"Error: {e}")


async def Neko(msg, match, client):
    try:
        res = requests.get("https://ironman.koyeb.app/ironman/neko", timeout=10)
        data = res.json()
        if data.get("status") and "ironman" in data and "url" in data["ironman"]:
            img_url = data["ironman"]["url"]
            await client.send_photo(msg.chat.id, photo=img_url, caption="Here's your neko!" )
        else:
            await msg.reply("Failed to get image.")
    except Exception as e:
        await msg.reply(f"Error: {e}")

Furina({
    "pattern": "waifu$",
    "fromMe": isPrivate,
    "desc": "Send a random waifu image.",
    "type": "anime"
}, Waifu)

Furina({
    "pattern": "neko$",
    "fromMe": isPrivate,
    "desc": "Send a random neko image.",
    "type": "anime"
}, Neko)

Furina({
    "pattern": "aquote$",
    "fromMe": isPrivate,
    "desc": "Send a random anime quote.",
    "type": "anime"
}, Aquote)
