from lib.furina import Furina, isPrivate
import requests
import io
import os

async def Url(msg, match, client):
    if not msg.reply_to_message:
        await msg.reply("Reply to a message.")
        return

    try:
        if msg.reply_to_message.media and msg.reply_to_message.media_type:
            file_path = await client.download_media(msg.reply_to_message.media)
            with open(file_path, 'rb') as f:
                response = requests.post('https://catbox.moe/user/api.php', data={'reqtype': 'fileupload'}, files={'fileToUpload': f})
            os.remove(file_path)
            if response.text.strip():
                await msg.reply(f"URL: {response.text.strip()}")
            else:
                await msg.reply("Failed to upload.")

        elif msg.reply_to_message.text:
            files = {'fileToUpload': ('message.txt', io.BytesIO(msg.reply_to_message.text.encode()), 'text/plain')}
            response = requests.post('https://catbox.moe/user/api.php', data={'reqtype': 'fileupload'}, files=files)
            if response.text.strip():
                await msg.reply(f"URL: {response.text.strip()}")
            else:
                await msg.reply("Failed to upload.")
        else:
            await msg.reply("No supported media.")

    except Exception as e:
        await msg.reply(f"Error: {e}")


Furina({
    "pattern": "url$",
    "fromMe": isPrivate,
    "desc": "Upload replied media",
    "type": "media"
}, Url)
