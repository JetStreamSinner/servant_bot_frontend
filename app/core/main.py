import asyncio

import requests
from aiogram import Bot, Dispatcher, types


async def root_handler(event: types.Message):
    proxy_service_url = "http://127.0.0.1:8000"
    service_list_router = "/services_list"
    target_url = proxy_service_url + service_list_router
    services_list_request = requests.get(target_url)
    services = services_list_request.json()
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=3)
    keyboard_markup.row(*[types.KeyboardButton(service["service_name"]) for service in services])
    await event.reply("Services list", reply_markup=keyboard_markup)


async def main():
    bot_token = "5784798752:AAH2WBi463u3EZsGvMnqnO6WfZ3UKA1rlaM"
    bot = Bot(token=bot_token)

    try:
        dispatcher = Dispatcher(bot=bot)
        dispatcher.register_message_handler(root_handler, commands={"start", "restart"})
        await dispatcher.start_polling()
    finally:
        await bot.close()


asyncio.run(main())
