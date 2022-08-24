from aiogram import types


def create_main_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    services_button = types.KeyboardButton("Services list")
    about_button = types.KeyboardButton("About")

    markup.row(services_button)
    markup.row(about_button)

    return markup
