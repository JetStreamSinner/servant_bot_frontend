import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from commands_handlers import root_handler


async def main():
    load_dotenv()
    bot_token = os.getenv("token")
    bot = Bot(token=bot_token)

    try:
        dispatcher = Dispatcher(bot=bot)
        dispatcher.register_message_handler(root_handler, commands={"start", "restart"})
        await dispatcher.start_polling()
    finally:
        await bot.close()


asyncio.run(main())
