from lib.furina import Furina, isPrivate
from pyrogram.types import ChatPermissions

async def is_admin(msg, client):
    try:
        user = await client.get_chat_member(msg.chat.id, msg.sender.id)
        return user.status in ("creator", "administrator")
    except Exception:
        return False


async def ban(msg, match, client):
    if not await is_admin(msg, client):
        return await msg.reply("You need to be admin.")

    if not msg.reply_to_message:
        return await msg.reply("Reply to a user to ban them.")

    try:
        await client.ban_chat_member(msg.chat.id, msg.reply_to_message.sender.id)
        await msg.reply(f"Banned {msg.reply_to_message.sender.first_name}")
    except Exception as e:
        await msg.reply(f"Failed: {e}")


async def unban(msg, match, client):
    if not await is_admin(msg, client):
        return await msg.reply("You need to be admin.")

    if not msg.reply_to_message:
        return await msg.reply("Reply to a user to unban them.")

    try:
        await client.unban_chat_member(msg.chat.id, msg.reply_to_message.sender.id)
        await msg.reply(f"Unbanned {msg.reply_to_message.sender.first_name}")
    except Exception as e:
        await msg.reply(f"Failed to unban user: {e}")


async def kick(msg, match, client):
    if not await is_admin(msg, client):
        return await msg.reply("You need to be admin.")

    if not msg.reply_to_message:
        return await msg.reply("Reply to a user to kick them.")

    try:
        await client.ban_chat_member(msg.chat.id, msg.reply_to_message.sender.id)
        await client.unban_chat_member(msg.chat.id, msg.reply_to_message.sender.id)
        await msg.reply(f"Kicked {msg.reply_to_message.sender.first_name}")
    except Exception as e:
        await msg.reply(f"Failed to kick user: {e}")


async def mute(msg, match, client):
    if not await is_admin(msg, client):
        return await msg.reply("You need to be admin.")

    if not msg.reply_to_message:
        return await msg.reply("Reply to a user to mute them.")

    try:
        await client.restrict_chat_member(
            msg.chat.id,
            msg.reply_to_message.sender.id,
            ChatPermissions()
        )
        await msg.reply(f"Muted {msg.reply_to_message.sender.first_name}")
    except Exception as e:
        await msg.reply(f"Failed to mute user: {e}")


async def unmute(msg, match, client):
    if not await is_admin(msg, client):
        return await msg.reply("You need to be admin.")

    if not msg.reply_to_message:
        return await msg.reply("Reply to a user to unmute them.")

    try:
        await client.restrict_chat_member(
            msg.chat.id,
            msg.reply_to_message.sender.id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True,
            )
        )
        await msg.reply(f"Unmuted {msg.reply_to_message.sender.first_name}")
    except Exception as e:
        await msg.reply(f"Failed to unmute user: {e}")


Furina({"pattern": "ban$", "fromMe": isPrivate, "desc": "Ban replied user", "type": "admin"}, ban)
Furina({"pattern": "unban$", "fromMe": isPrivate, "desc": "Unban replied user", "type": "admin"}, unban)
Furina({"pattern": "kick$", "fromMe": isPrivate, "desc": "Kick replied user", "type": "admin"}, kick)
Furina({"pattern": "mute$", "fromMe": isPrivate, "desc": "Mute replied user", "type": "admin"}, mute)
Furina({"pattern": "unmute$", "fromMe": isPrivate, "desc": "Unmute replied user", "type": "admin"}, unmute)
