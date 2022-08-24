from aiogram import types
from keyboard_markups import create_main_markup


async def root_handler(event: types.Message):
    main_menu_markup = create_main_markup()
    await event.reply("Main", reply_markup=main_menu_markup)
