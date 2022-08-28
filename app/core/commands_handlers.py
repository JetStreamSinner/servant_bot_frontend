import enum
from aiogram import types

from keyboard_markups import create_main_markup, services_list_markup


class HandlerType(enum.Enum):
    MessageHandler = 0
    CallbackQueryHandler = 1


async def root_handler(message: types.Message):
    markup = create_main_markup()
    await message.reply(text="Root handler", reply_markup=markup)


async def about_handler(message: types.Message):
    await message.answer(text="About handler")


async def services_list_handler(message: types.Message):
    markup = services_list_markup()
    await message.answer(text="Service list handler", reply_markup=markup)


async def service_handler(query: types.CallbackQuery):
    await query.answer("Service id is {0}".format(query.data))


def get_commands_handler_bind():
    binding = [
        {
            "commands": ["start"],
            "handler": root_handler,
            "handler_type": HandlerType.MessageHandler
        },
        {
            "commands": ["about"],
            "handler": about_handler,
            "handler_type": HandlerType.MessageHandler
        },
        {
            "commands": ["services"],
            "handler": services_list_handler,
            "handler_type": HandlerType.MessageHandler
        },
        {
            "commands": [],
            "handler": service_handler,
            "handler_type": HandlerType.CallbackQueryHandler
        }
    ]
    return binding
