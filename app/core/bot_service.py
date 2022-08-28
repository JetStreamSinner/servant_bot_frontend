from typing import Dict, Any
from aiogram import Bot, Dispatcher


async def start_service(configuration: Dict[str, Any]):
    bot_token = configuration["token"]
    bot = Bot(token=bot_token)

    commands_handler_bind = configuration["handlers"]
    dispatcher = Dispatcher(bot=bot)
    for binding in commands_handler_bind:
        dispatcher.register_message_handler(binding["handler"], commands=binding["commands"])

    try:
        await dispatcher.start_polling()
    finally:
        await bot.close()
