import asyncio
from lib.client import _Client

async def idle():
    print("Bot is running. Press Ctrl+C to stop.")
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("Shutting down...")

async def main():
    print("Starting Furina...")
    client = _Client()
    await client.initialize()
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
