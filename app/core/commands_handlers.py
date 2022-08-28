from aiogram import types

from keyboard_markups import create_main_markup, services_list_markup


async def root_handler(message: types.Message):
    markup = create_main_markup()
    await message.reply(text="Root handler", reply_markup=markup)


async def about_handler(message: types.Message):
    await message.answer(text="About handler")


async def services_list_handler(message: types.Message):
    markup = services_list_markup()
    await message.answer(text="Service list handler", reply_markup=markup)


def get_commands_handler_bind():
    binding = [
        {
            "commands": ["start"],
            "handler": root_handler
        },
        {
            "commands": ["about"],
            "handler": about_handler
        },
        {
            "commands": ["services"],
            "handler": services_list_handler
        }
    ]
    return binding
