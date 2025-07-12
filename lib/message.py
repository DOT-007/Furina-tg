import time


class ReplyMessage:

    def __init__(self, reply_msg):
        self.id = reply_msg.id
        self.text = reply_msg.text or reply_msg.caption or ""
        self.sender = reply_msg.from_user or reply_msg.sender_chat
        self._raw = reply_msg
        self.media = None
        self.media_type = None
        self.forward_origin = getattr(reply_msg, 'forward_origin', None)
        self.is_forwarded = self.forward_origin is not None
        if reply_msg.photo:
            self.media = reply_msg.photo
            self.media_type = "photo"
        elif reply_msg.video:
            self.media = reply_msg.video
            self.media_type = "video"
        elif reply_msg.audio:
            self.media = reply_msg.audio
            self.media_type = "audio"
        elif reply_msg.voice:
            self.media = reply_msg.voice
            self.media_type = "voice"
        elif reply_msg.document:
            self.media = reply_msg.document
            self.media_type = "document"
        elif reply_msg.sticker:
            self.media = reply_msg.sticker
            self.media_type = "sticker"
        elif reply_msg.animation:
            self.media = reply_msg.animation
            self.media_type = "animation"

    @property
    def file_id(self):
        if not self.media:
            return None

        if self.media_type == "photo":
            return self.media.file_id
        return self.media.file_id if hasattr(self.media, "file_id") else None

    def __str__(self):
        return self.text


class Message:

    def __init__(self, msg, client):
        self._msg = msg
        self._client = client
        self.client = client
        self.id = msg.id
        self.chat = msg.chat
        self.text = msg.text or msg.caption or ""
        self.sender = msg.from_user
        self.is_self = msg.from_user and msg.from_user.is_self
        self.timestamp = msg.date
        self.mentioned = msg.mentioned
        self.scheduled = msg.scheduled
        self.from_scheduled = msg.from_scheduled
        self.media = None
        self.media_type = None

        if msg.photo:
            self.media = msg.photo
            self.media_type = "photo"
        elif msg.video:
            self.media = msg.video
            self.media_type = "video"
        elif msg.audio:
            self.media = msg.audio
            self.media_type = "audio"
        elif msg.voice:
            self.media = msg.voice
            self.media_type = "voice"
        elif msg.document:
            self.media = msg.document
            self.media_type = "document"
        elif msg.sticker:
            self.media = msg.sticker
            self.media_type = "sticker"
        elif msg.animation:
            self.media = msg.animation
            self.media_type = "animation"

        self.forward_origin = getattr(msg, 'forward_origin', None)
        self.is_forwarded = self.forward_origin is not None

        self.reply_to_message = None
        if msg.reply_to_message:
            self.reply_to_message = ReplyMessage(msg.reply_to_message)

    async def reply(self, text, **kwargs):
        return await self._msg.reply(text, **kwargs)

    async def edit(self, text, **kwargs):
        if hasattr(self._msg, "edit_text"):
            return await self._msg.edit_text(text, **kwargs)
        elif hasattr(self._msg, "edit"):
            return await self._msg.edit(text, **kwargs)
        return None

    async def delete(self):
        return await self._msg.delete()

    async def react(self, emoji="✅"):
        return await self._msg.react(emoji)

    async def send(self, content, meta=None, reply=False, mode="text"):
        meta = meta or {}
        chat_id = self.chat.id
        if reply and self.id:
            meta["reply_to_message_id"] = self.id

        if mode == "text":
            return await self._client.send_message(chat_id, content, **meta)
        elif mode == "photo" or mode == "image":
            return await self._client.send_photo(chat_id, content, **meta)
        elif mode == "video":
            return await self._client.send_video(chat_id, content, **meta)
        elif mode == "audio":
            return await self._client.send_audio(chat_id, content, **meta)
        elif mode == "voice":
            return await self._client.send_voice(chat_id, content, **meta)
        elif mode == "sticker":
            return await self._client.send_sticker(chat_id, content, **meta)
        elif mode == "document":
            return await self._client.send_document(chat_id, content, **meta)
        elif mode == "animation" or mode == "gif":
            return await self._client.send_animation(chat_id, content, **meta)

    async def forward(self, chat_id):
        return await self._msg.forward(chat_id)

    async def copy(self, chat_id, **kwargs):
        return await self._msg.copy(chat_id, **kwargs)

    def get_args(self):
        parts = self.text.split(" ")
        return parts[1:] if len(parts) > 1 else []

    def get_quoted_text(self):
        return self.reply_to_message.text if self.reply_to_message else None

    async def progress_callback(self,
                                current,
                                total,
                                message,
                                start_time=None,
                                info=""):
        if not start_time:
            start_time = time.time()

        if round(current / total * 100, 1) % 10 == 0:
            now = time.time()
            diff = now - start_time
            if diff > 1:
                speed = current / diff
                if speed > 0:
                    eta = (total - current) / speed
                    await message.edit(
                        f"{info}\n"
                        f"{current * 100 / total:.1f}% "
                        f"({humanbytes(current)}/{humanbytes(total)}) "
                        f"@ {humanbytes(speed)}/s | ETA: {time_formatter(eta)}"
                    )

    def __str__(self):
        return self.text


def humanbytes(size):
    if not size:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units) - 1:
        size /= 1024.0
        i += 1
    return f"{size:.2f} {units[i]}"


def time_formatter(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)

    if hours:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"
