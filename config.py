import os
import logging
from dotenv import load_dotenv

load_dotenv("config.env")

VERSION = "1.0.0"
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH")
PREFIX = os.environ.get("PREFIX", "!")
SESSION = os.environ.get("SESSION")
MODE = os.environ.get("MODE", "private").lower()

if not API_ID:
    raise ValueError("API_ID must be a valid integer.")
if not API_HASH:
    raise ValueError("API_HASH is required.")
if MODE not in ["private", "public"]:
    raise ValueError("MODE must be either 'private' or 'public'")

def is_private_mode():
    return MODE == "private"

print("Config:")
print(f"- VERSION: {VERSION}")
print(f"- MODE: {MODE.upper()}")
print(f"- PREFIX: {PREFIX}")
