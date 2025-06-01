from lib.furina import Furina, plugins
from config import PREFIX, VERSION
from datetime import datetime

async def menu_handler(msg, match, client):
    plugins_by_type = {}
    plugin_count = 0

    for p in plugins:
        cfg = p["config"]
        cmd_type = cfg.get("type", "misc").lower()
        if cmd_type not in plugins_by_type:
            plugins_by_type[cmd_type] = []
        pattern = cfg.get("pattern", "")
        if pattern:
            # Clean up pattern for display
            display_pattern = pattern
            if "$" in display_pattern:
                display_pattern = display_pattern.split("$")[0]
            if "(" in display_pattern:
                display_pattern = display_pattern.split("(")[0]
            plugins_by_type[cmd_type].append(display_pattern)
            plugin_count += 1

    me = await client.get_me()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    menu_text = (f"╔═══❖•ೋ°❖°ೋ•❖═══❖•ೋ°❖°ೋ•❖═══╗\n"
                 f"ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ𝓣𝓾𝓻𝓲𝓷𝓪 ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\n"
                 f"╚═══❖•ೋ°❖°ೋ•❖═══❖•ೋ°❖°ೋ•❖═══╝\n\n"
                 f"Bot: @{me.username}\n"
                 f"Version: `{VERSION}`\n"
                 f"Time: `{current_time}`\n"
                 f"Mode: Userbot\n"
                 f"Plugins: {plugin_count}\n\n"
                 )

    for cmd_type, cmd_list in sorted(plugins_by_type.items()):
        menu_text += f"┏━━━ {cmd_type.upper()} ━━━┓\n"
        for cmd in sorted(set(cmd_list)):
            menu_text += f"┃ {cmd}\n"
        menu_text += "┗━━━━━━━━━━━━━━┛\n\n"
    await msg.reply(menu_text)

Furina({
    "pattern": "menu$",
    "fromMe": True,
    "desc": "Display bot menu and plugins",
    "type": "utils"
}, menu_handler)

async def help_handler(msg, match, client):
    args = msg.get_args()
    if not args:
        help_text = ("╔═══❖•ೋ°❖°ೋ•❖═══❖•ೋ°❖°ೋ•❖═══╗\n"
                     "ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ𝓣𝓾𝓻𝓲𝓷𝓪 ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\n"
                     "╚═══❖•ೋ°❖°ೋ•❖═══❖•ೋ°❖°ೋ•❖═══╝\n\n"
                     )
        for p in sorted(plugins, key=lambda x: x["config"].get("pattern", "")):
            cfg = p["config"]
            prefix = "" if cfg.get("noprefix", False) else cfg.get("prefix", PREFIX)
            pattern = cfg.get("pattern", "")
            desc = cfg.get("desc", " ")
            if pattern:
                display_pattern = pattern
                if "$" in display_pattern:
                    display_pattern = display_pattern.split("$")[0]
                if "(" in display_pattern:
                    display_pattern = display_pattern.split("(")[0]
                help_text += f"𝄞ㅤ`{prefix}{display_pattern}`\n"
                help_text += f"ㅤㅤ└─𒆜 ㅤ{desc}\n\n"
        await msg.reply(help_text)
    else:
        query = args[0].lower()
        found = False
        for p in plugins:
            cfg = p["config"]
            pattern = cfg.get("pattern", "").lower()
            if query in pattern:
                prefix = "" if cfg.get("noprefix", False) else cfg.get("prefix", PREFIX)
                desc = cfg.get("desc", "No description")
                cmd_type = cfg.get("type", "misc")
                clean_pattern = pattern
                if "$" in clean_pattern:
                    clean_pattern = clean_pattern.split("$")[0]
                if "(" in clean_pattern:
                    clean_pattern = clean_pattern.split("(")[0]
                help_text = (f"╔═══❖•ೋ°❖°ೋ•❖═══❖•ೋ°❖°ೋ•❖═══╗\n"
                             f" ㅤㅤㅤㅤㅤㅤㅤ{clean_pattern.upper()} ㅤㅤㅤㅤㅤㅤㅤ\n"
                             f"╚═══❖•ೋ°❖°ೋ•❖═══❖•ೋ°❖°ೋ•❖═══╝\n\n"
                             f"ムㅤᴄᴏᴍᴍᴀɴᴅ    `{prefix}{clean_pattern}`\n"
                             f"ムㅤᴛʏᴘᴇ ᴄᴍᴅ      {cmd_type}\n"
                             f"ムㅤɪɴғᴏ               {desc}\n"
                             f"ムㅤᴍᴏᴅᴇ             {'ᴘʀɪᴠᴀᴛᴇ' if cfg.get('fromMe', True) else 'ᴘᴜʙʟɪᴄ'}\n"
                             )
                await msg.reply(help_text)
                found = True
                break
        if not found:
            await msg.reply(f"╔═══❖•ೋ°❖°ೋ•❖═══❖•ೋ°❖°ೋ•❖═══╗\n"
                            "ㅤㅤㅤㅤㅤㅤㅤㅤ ㅤ 𝓠𝓾𝓮𝓻𝔂 𝓝𝓸𝓽  𝓕𝓸𝓾𝓷𝓭ㅤㅤㅤㅤㅤ       ㅤㅤ\n"
                            "╚═══❖•ೋ°❖°ೋ•❖═══❖•ೋ°❖°ೋ•❖═══╝\n\n"
                            f"𝗘𝗡𝗢𝗖𝗠𝗗    𝙉𝙤 𝙘𝙤𝙢𝙢𝙖𝙣𝙙𝙨 𝙢𝙖𝙩𝙘𝙝𝙚𝙙 𝙩𝙤 𝙘𝙖𝙡𝙡 𝙩𝙮𝙥𝙚 𝙤𝙛`{query}` 𝙞𝙣 𝙥𝙡𝙪𝙜𝙞𝙣𝙨 𝙡𝙞𝙨𝙩"
                            )

Furina({
    "pattern": "help(?: |)([^$]*)?$",
    "fromMe": True,
    "desc": "Displays available commands",
    "type": "utils"
}, help_handler)