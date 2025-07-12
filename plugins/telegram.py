from lib.furina import Furina, isPrivate

async def tgme(msg, match, client):
    try:
        target_user = None
        if msg.reply_to_message:
            target_user = msg.reply_to_message.sender
        else:
            args = msg.get_args()
            if args:
                try:
                    user_input = args[0].replace("@", "")
                    if user_input.isdigit():
                        target_user = await client.get_users(int(user_input))
                    else:
                        target_user = await client.get_users(user_input)
                except Exception:
                    await msg.reply("User not found.")
                    return
            else:
                target_user = await client.get_me()
        if target_user and target_user.username:
            await msg.reply(f"https://{target_user.username}.t.me")
        else:
            await msg.reply("User doesn't have a username.")

    except Exception as e:
        await msg.reply(f"Error: {e}")


async def invite(msg, match, client):
    try:
        chat = msg.chat
        if hasattr(chat, 'invite_link') and chat.invite_link:
            await msg.reply(f"Invite Link: {chat.invite_link}")
        else:
            try:
                invite_link = await client.export_chat_invite_link(chat.id)
                await msg.reply(f"Invite Link: {invite_link}")
            except Exception:
                await msg.reply("Cannot generate invite link for this chat.")

    except Exception as e:
        await msg.reply(f"Error getting invite link: {e}")


async def Id(msg, match, client):
    try:
        if msg.reply_to_message:
            target = msg.reply_to_message.sender
            reply_text = f"User ID: `{target.id}`\nChat ID: `{msg.chat.id}`\nMessage ID: `{msg.reply_to_message.id}`"
        else:
            reply_text = f"Chat ID: `{msg.chat.id}`\nYour ID: `{msg.sender.id}`"

        await msg.reply(reply_text)

    except Exception as e:
        await msg.reply(f"Error getting IDs: {e}")


async def chatinfo(msg, match, client):
    try:
        chat_info = f"Title: {msg.chat.title or 'N/A'}"
        chat_info += f"\ID: {msg.chat.id}"
        chat_info += f"\Type: {msg.chat.type.value if hasattr(msg.chat.type, 'value') else msg.chat.type}"
        if hasattr(msg.chat, 'username') and msg.chat.username:
            chat_info += f"\nUsername: @{msg.chat.username}"
        if hasattr(msg.chat, 'members_count'):
            chat_info += f"\nMembers Count: {msg.chat.members_count}"
        if hasattr(msg.chat, 'description') and msg.chat.description:
            chat_info += f"\nDescription: {msg.chat.description}"
        try:
            if msg.chat.photo:
                await client.send_photo(
                    msg.msg.chat.id,
                    photo=msg.chat.photo.big_file_id,
                    caption=chat_info,
                    reply_to_message_id=msg.id
                )
            else:
                await msg.reply(chat_info)
        except Exception:
            await msg.reply(chat_info)

    except Exception as e:
        await msg.reply(f"Error getting msg.chat info: {e}")


async def dlt(msg, match, client):
    if not msg.reply_to_message:
        await msg.reply("Reply to a message to delete it.")
        return

    try:
        await client.delete_messages(msg.chat.id, msg.reply_to_message.id)
        await msg.delete()
    except Exception as e:
        await msg.reply(f"Failed: {e}")


async def Me(msg, match, client):
    try:
        me = await client.get_me()
        user_info = f"Name: {me.first_name or 'N/A'}"
        if me.last_name:
            user_info += f" {me.last_name}"
        user_info += f"\nUsername: @{me.username}" if me.username else "\nUsername: None"
        user_info += f"\nUser ID: {me.id}"
        user_info += f"\nIs Bot: {'Yes' if me.is_bot else 'No'}"
        user_info += f"\nIs Premium: {'Yes' if me.is_premium else 'No'}"
        user_info += f"\nIs Verified: {'Yes' if me.is_verified else 'No'}"
        try:
            photos = await client.get_chat_photos("me", limit=1)
            if photos:
                photo = photos[0]
                await client.send_photo(
                    msg.chat.id,
                    photo=photo.file_id,
                    caption=user_info,
                    reply_to_message_id=msg.id
                )
            else:
                await msg.reply(user_info)
        except Exception:
            await msg.reply(user_info)

    except Exception as e:
        await msg.reply(f"Error: {e}")


async def save(msg, match, client):
    if not msg.reply_to_message:
        await msg.reply("Reply to a message to save.")
        return
    try:
        await client.forward_messages(chat_id="me", from_chat_id=msg.chat.id, message_ids=msg.reply_to_message.id)
    except Exception as e:
        await msg.reply(f"Error: {e}")


async def Purge(msg, match, client):
    if not msg.reply_to_message:
        await msg.reply("Reply to a message to start purging from.")
        return
    try:
        messages_to_delete = []
        async for message in client.get_chat_history(msg.chat.id, limit=200):
            if msg.reply_to_message.id <= message.id <= msg.id:
                messages_to_delete.append(message.id)
            if message.id < msg.reply_to_message.id:
                break

        if not messages_to_delete:
            await msg.reply("No messages found to purge.")
            return

        for i in range(0, len(messages_to_delete), 100):
            batch = messages_to_delete[i:i+100]
            await client.delete_messages(msg.chat.id, batch)

    except Exception as e:
        await msg.reply(f"Error: {e}")


async def Whois(msg, match, client):
    t_usr = None
    if msg.reply_to_message:
        t_usr = msg.reply_to_message.sender
    else:
        args = msg.get_args()
        if args:
            try:
                input_ = args[0].replace("@", "")
                if input_.isdigit():
                    t_usr = await client.get_users(int(input_))
                else:
                    t_usr = await client.get_users(input_)
            except Exception as e:
                await msg.reply(f"User not found: {e}")
                return
        else:
            t_usr = msg.sender
    if not t_usr:
        await msg.reply("No user found to get info for.")
        return

    user_info = f"Name: {t_usr.first_name or 'N/A'}"
    if t_usr.last_name:
        user_info += f" {t_usr.last_name}"
    user_info += f"\nUsername: @{t_usr.username}" if t_usr.username else "\nUsername: None"
    user_info += f"\nUser ID: {t_usr.id}"
    user_info += f"\nIs Bot: {'Yes' if t_usr.is_bot else 'No'}"
    user_info += f"\nIs Premium: {'Yes' if t_usr.is_premium else 'No'}"
    user_info += f"\nIs Verified: {'Yes' if t_usr.is_verified else 'No'}"
    user_info += f"\nIs Scam: {'Yes' if t_usr.is_scam else 'No'}"
    user_info += f"\nIs Fake: {'Yes' if t_usr.is_fake else 'No'}"

    try:
        photos = []
        async for photo in client.get_chat_photos(t_usr.id, limit=1):
            photos.append(photo)

        if photos:
            photo = photos[0]
            await client.send_photo(
                msg.chat.id,
                photo=photo.file_id,
                caption=user_info,
                reply_to_message_id=msg.id
            )
        else:
            await msg.reply(user_info)
    except Exception:
        await msg.reply(user_info)

Furina({
    "pattern": r"whois(?:\s+(.+))?$",
    "fromMe": isPrivate,
    "desc": "Get user information",
    "type": "telegram"
}, Whois)

Furina({
    "pattern": r"purge$",
    "fromMe": isPrivate,
    "desc": "Delete all messages between replied message and command (inclusive)",
    "type": "telegram"
}, Purge)

Furina({
    "pattern": "save$",
    "fromMe": isPrivate,
    "desc": "Forward replied message to saved messages",
    "type": "media"
}, save)

Furina({
    "pattern": "me$",
    "fromMe": isPrivate,
    "desc": "Get your own user information",
    "type": "telegram"
}, Me)

Furina({
    "pattern": "dlt$",
    "fromMe": isPrivate,
    "desc": "Delete replied message",
    "type": "telegram"
}, dlt)

Furina({
    "pattern": "dlt$",
    "fromMe": isPrivate,
    "desc": "Delete replied message",
    "type": "telegram"
}, dlt)

Furina({
    "pattern": r"tgme(?:\s+(.+))?$",
    "fromMe": isPrivate,
    "desc": "Get telegram URL for user",
    "type": "telegram"
}, tgme)

Furina({
    "pattern": "invite$",
    "fromMe": isPrivate,
    "desc": "Get chat invite link",
    "type": "telegram"
}, invite)

Furina({
    "pattern": "id$",
    "fromMe": isPrivate,
    "desc": "Get IDs",
    "type": "telegram"
}, Id)

Furina({
    "pattern": "info",
    "fromMe": isPrivate,
    "desc": "Get current chat information",
    "type": "telegram"
}, chatinfo)
