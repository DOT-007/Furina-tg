import os
import re
import asyncio
import importlib.util
import sys
import traceback
from datetime import datetime
from functools import lru_cache
from pyrogram import Client, filters
from typing import Dict, Any, List, Optional, Union, Callable
from config import API_ID, API_HASH, PREFIX, VERSION, MODE, is_private_mode
from lib.furina import plugins, register_middleware, run_middleware
from lib.message import Message, ReplyMessage

COLORS = {
    "RESET": "\033[0m",
    "BLUE": "\033[94m",
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "CYAN": "\033[96m",
    "BOLD": "\033[1m",
}

pattern_cache = {}

class _Client:
    def __init__(self):
        if not API_ID or not API_HASH:
            print(f"{COLORS['RED']}[ERROR] API_ID and API_HASH must be there{COLORS['RESET']}")
            raise ValueError("API_ID and API_HASH must be there")
        
        print(f"{COLORS['GREEN']} Starting Furina...{COLORS['RESET']}")
        
        self.app = Client(
            "Furina",
            api_id=API_ID,
            api_hash=API_HASH,
            device_model="Furina",
            app_version="IRON-M4N 6.9",
            system_version="HydroOs 6.9.0",
        )

        self.app.on_message(filters.text | filters.media)(self.cmd_handler)
        self.store: Dict[str, Any] = {}

    async def start(self):
        try:
            await self.app.start()
            async def phone_code(_, __, phone_number):
                code = input(f"{COLORS['BLUE']}Enter the code sent to {phone_number}: {COLORS['RESET']}")
                return code
            
            async def password_handler(_, Pass):
                hint = Pass or "none"
                password = input(f"{COLORS['BLUE']}Enter your Two-Step Verification password (hint: {hint}): {COLORS['RESET']}")
                return password
            
            self.app.phone_code = phone_code
            self.app.password_handler = password_handler
            self.load_plugins()
            await self.startup_message()
            
            print(f"{COLORS['GREEN']}Furina started{COLORS['RESET']}")
        except Exception as e:
            print(f"{COLORS['RED']}[ERROR] Failed to start: {str(e)}{COLORS['RESET']}")
            print(f"{COLORS['RED']}[ERROR] {traceback.format_exc()}{COLORS['RESET']}")
            raise

    async def initialize(self):
        await self.start()

    def run(self):
        self.app.run()
    async def startup_message(self):
        try:
            me = await self.app.get_me()
            allcmds = len(plugins)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            startup_text = (
                f"** Furina connected **\n\n"
                f"**Version:** `{VERSION}`\n"
                f"**Mode:** `{MODE.upper()}`\n"
                f"**Total Commands:** `{allcmds}`\n"
                f"**Time:** `{now}`\n"
                f"**Username:** @{me.username}\n"
                f"**User ID:** `{me.id}`"
            )

            print(f"{COLORS['BLUE']}[STARTUP] Furina v{VERSION} Started{COLORS['RESET']}")
            print(f"{COLORS['BLUE']}[STARTUP] Mode: {MODE.upper()}{COLORS['RESET']}")
            print(f"{COLORS['BLUE']}[STARTUP] Commands: {allcmds}{COLORS['RESET']}")
            print(f"{COLORS['BLUE']}[STARTUP] Username: @{me.username}{COLORS['RESET']}")
            print(f"{COLORS['BLUE']}[STARTUP] User ID: {me.id}{COLORS['RESET']}")

            await self.app.send_message(me.id, startup_text)
        except Exception as e:
            print(f"{COLORS['RED']}[ERROR] Failed to send startup message: {str(e)}{COLORS['RESET']}")

    def load_plugins(self):
        sys.path.insert(0, os.getcwd())
        plugin_dir = os.path.join(os.getcwd(), "plugins")
        if not os.path.exists(plugin_dir):
            print(f"{COLORS['RED']}[ERROR] Directory not found: {plugin_dir}{COLORS['RESET']}")
            try:
                os.makedirs(plugin_dir)
            except Exception as e:
                print(f"{COLORS['RED']}[ERROR] Failed: {str(e)}{COLORS['RESET']}")
            return

        plugin_files = [f for f in os.listdir(plugin_dir) if f.endswith('.py') and f != "__init__.py"]
        if not plugin_files:
            print(f"{COLORS['RED']}[ERROR] No plugins found{COLORS['RESET']}")
            return

        print(f"{COLORS['BLUE']}Found {len(plugin_files)} Files{COLORS['RESET']}")

        for plugin in plugins:
            cfg = plugin["config"]
            pattern = cfg.get("pattern", "")
            if pattern and pattern not in pattern_cache:
                try:
                    pattern_cache[pattern] = re.compile(pattern)
                except Exception as e:
                    print(f"{COLORS['RED']}[ERROR] Failed to get pattern {pattern}: {str(e)}{COLORS['RESET']}")

        for filename in plugin_files:
            module_name = filename[:-3]
            file_path = os.path.join(plugin_dir, filename)

            try:
                if module_name in sys.modules:
                    continue
                    
                print(f"{COLORS['BLUE']}Installing {module_name}...{COLORS['RESET']}")
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec is None:
                    print(f"{COLORS['RED']}[ERROR] Failed to load {module_name}{COLORS['RESET']}")
                    continue

                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
               
            except Exception as e:
                print(f"{COLORS['RED']}[ERROR] Failed to load plugin {module_name}: {str(e)}{COLORS['RESET']}")

        sys.path.pop(0)
        print(f"{COLORS['GREEN']}Total plugins: {len(plugins)}{COLORS['RESET']}")

    async def cmd_handler(self, client, msg):
        text = msg.text or msg.caption or ""
        if not text:
            return
            
        sender_is_me = msg.from_user and msg.from_user.is_self
        
        if msg.from_user:
            username = msg.from_user.username or msg.from_user.id
            chat_name = msg.chat.title if hasattr(msg.chat, "title") and msg.chat.title else f"Chat {msg.chat.id}"
            direction = "↓ INCOMING" if not sender_is_me else "↑ OUTGOING"
            print(f"{COLORS['BLUE']}[MSG] {direction} | {username} in {chat_name}: {text[:50]}{'...' if len(text) > 50 else ''}{COLORS['RESET']}")
            
        curvemsg = Message(msg, client)

        try:
            if await run_middleware(curvemsg, client) is False:
                return

            for plugin in plugins:
                cfg = plugin["config"]
                pattern = cfg.get("pattern", "")
                from_me = cfg.get("fromMe", True)
                no_prefix = cfg.get("noprefix", False)
                pfx = cfg.get("prefix", PREFIX)

                if is_private_mode() and from_me and not sender_is_me:
                    continue

                if from_me and not sender_is_me:
                    continue

                if not no_prefix:
                    if not text.startswith(pfx):
                        continue
                    cmd_text = text[len(pfx):]
                else:
                    cmd_text = text

                if pattern:
                    compiled_pattern = pattern_cache.get(pattern)
                    if not compiled_pattern:
                        compiled_pattern = re.compile(pattern)
                        pattern_cache[pattern] = compiled_pattern
                    match = compiled_pattern.match(cmd_text)
                    if match:
                        match_text = ""
                        if match.groups():
                            match_text = match.group(1)
                        else:
                            pattern_end = match.end()
                            if pattern_end < len(cmd_text):
                                match_text = cmd_text[pattern_end:].strip()
                        try:
                            await plugin["handler"](curvemsg, match_text, client)
                        except Exception as e:
                            await curvemsg.reply(f"**Error**:\n `{str(e)}`")
                            print(f"{COLORS['RED']}[ERROR] Command {cfg.get('desc', 'unknown')} failed: {str(e)}{COLORS['RESET']}")
                            print(f"{COLORS['RED']}[ERROR] {traceback.format_exc()}{COLORS['RESET']}")
                        break
        except Exception as e:
            print(f"{COLORS['RED']}[ERROR] Command handler failed: {str(e)}{COLORS['RESET']}")
            print(f"{COLORS['RED']}[ERROR] {traceback.format_exc()}{COLORS['RESET']}")
