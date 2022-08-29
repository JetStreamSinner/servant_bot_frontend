from typing import Dict, Any
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from commands_handlers import HandlerType


async def start_service(configuration: Dict[str, Any]):
    bot_token = configuration["token"]
    bot = Bot(token=bot_token)

    commands_handler_bind = configuration["handlers"]
    storage = MemoryStorage()
    dispatcher = Dispatcher(bot=bot, storage=storage)
    for binding in commands_handler_bind:
        match binding["handler_type"]:
            case HandlerType.MessageHandler:
                dispatcher.register_message_handler(binding["handler"], commands=binding["commands"])
            case HandlerType.CallbackQueryHandler:
                dispatcher.register_callback_query_handler(callback=binding["handler"])

    try:
        await dispatcher.start_polling()
    finally:
        await bot.close()
