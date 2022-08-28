from aiogram import types

from backend_requests import get_services


def create_main_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    services_button = types.KeyboardButton("Services list")
    about_button = types.KeyboardButton("About")

    markup.row(services_button)
    markup.row(about_button)

    return markup


def services_list_markup():
    markup = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    services_list = get_services()
    [markup.row(types.InlineKeyboardButton(service["service_name"], callback_data=service["service_id"])) for service in
     services_list]

    return markup
