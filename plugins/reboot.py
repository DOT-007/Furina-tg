from lib.furina import Furina, isPrivate
import sys ,os ,asyncio ,platform , psutil 
from datetime import timedelta
import time

async def reboot_system(message, match, client):
    await message.reply("Rebooting the system...")
    os.execl(sys.executable, sys.executable, *sys.argv)

async def shutdown_system(message, match, client):
    await message.reply("Reboot now to prevent shutdown....")
    countdown = 5
    countdown_message = await message.reply("⚠️ **Warning!** Shutting down in 5 seconds... ⏳")

    for i in range(countdown, 0, -1):
        await countdown_message.edit(f"⚠️ **Warning!** {i} seconds remaining before shutting down... ⏳")
        await asyncio.sleep(1)

    await message.reply("The bot is shutting down now... Goodbye! 😢")
    await client.stop()
    sys.exit(0)

async def stats(msg, match, client):
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_str = str(timedelta(seconds=int(uptime_seconds)))
    await msg.reply(f"**⏳ Uptime:** {uptime_str}")

async def send_system_info(msg, match, client):
    uname = platform.uname()
    sys_info = (
        f"🖥 **System Information**\n"
        f"**System**: {uname.system}\n"
        f"**Node Name**: {uname.node}\n"
        f"**Release**: {uname.release}\n"
        f"**Version**: {uname.version}\n"
        f"**Machine**: {uname.machine}\n"
        f"**Processor**: {uname.processor}\n"
    )

    memory = psutil.virtual_memory()
    mem_info = (
        f"💾 **Memory Information**\n"
        f"**Total**: {memory.total / (1024 ** 3):.2f} GB\n"
        f"**Available**: {memory.available / (1024 ** 3):.2f} GB\n"
        f"**Used**: {memory.used / (1024 ** 3):.2f} GB\n"
        f"**Percentage**: {memory.percent}%\n"
    )

    await msg.reply(f"{sys_info}\n{mem_info}")

Furina({
    "pattern": "reboot$",
    "fromMe": True,
    "desc": "Reboot the system.",
    "type": "admin"
}, reboot_system)

Furina({
    "pattern": "shutdown$",
    "fromMe": True,
    "desc": "Shutdown the system.",
    "type": "admin"
}, shutdown_system)

Furina({
    "pattern": "sysinfo$",
    "fromMe": isPrivate,
    "desc": "Display system information.",
    "type": "utils"
}, send_system_info)

Furina({
    "pattern": "uptime$",
    "fromMe": isPrivate,
    "desc": "Display system stats.",
    "type": "utils"
}, stats)