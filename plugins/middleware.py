"""
Middleware functions run before command handlers

import time
from lib.furina import register_middleware
from lib.logger import log_msg
from config import LOG_LEVEL

@register_middleware
async def log_middleware(msg, client):
    if not msg.is_self:
        if msg.sender and msg.sender.username:
            sender = f"@{msg.sender.username}"
        elif msg.sender:
            sender = f"User {msg.sender.id}"
        else:
            sender = "Unknown"
        chat_name = msg.chat.title if hasattr(msg.chat, "title") and msg.chat.title else f"Chat {msg.chat.id}"
        log_level = "INFO" if LOG_LEVEL == "INFO" else "DEBUG"
        log_msg(f"Message from {sender} in {chat_name}: {msg.text[:50]}{'...' if len(msg.text) > 50 else ''}", 
                lvl=log_level, 
                tag="MIDDLEWARE")

    return True

@register_middleware
async def performance_middleware(msg, client):
#execute time test
    msg._cmd_start_time = time.time()
    return True
"""