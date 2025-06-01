from lib.furina import Furina, isPrivate
import requests

async def waifu_handler(msg, match, client):
    api_url = "https://ironman.koyeb.app/ironman/waifu"
    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()
        if data.get("status") and "ironman" in data and "url" in data["ironman"]:
            img_url = data["ironman"]["url"]
            await client.send_photo(
                msg.chat.id,
                photo=img_url,
                caption="Here's your waifu!"
            )
        else:
            await msg.reply("Failed to get waifu image. Try again later.")
    except Exception as e:
        await msg.reply(f"Error: {e}")

Furina({
    "pattern": "waifu$",
    "fromMe": isPrivate,
    "desc": "Send a random waifu image.",
    "type": "fun"
}, waifu_handler)