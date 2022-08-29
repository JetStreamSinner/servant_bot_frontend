import logging

import os

import asyncio
from dotenv import load_dotenv
from bot_service import start_service
from commands_handlers import get_commands_handler_bind


async def main():
    load_dotenv()
    logging.basicConfig(level=logging.DEBUG)
    service_config = {
        "token": os.getenv("token"),
        "handlers": get_commands_handler_bind()
    }
    await start_service(configuration=service_config)

asyncio.run(main())
