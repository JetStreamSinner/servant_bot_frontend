import base64
from typing import Any

from aiogram import types


def make_argument_message(arg_name: str, arg_description: str, arg_type: str):
    message = """
Заголовок: {0}
Описание: {1}
Тип: {2}
""".format(arg_name, arg_description, arg_type)
    return message


async def send_req_for_arg(arg: Any, message: types.Message):
    chat_id = message.chat.id
    send_message = message.bot.send_message
    await send_message(chat_id=chat_id, text="Сервис выбран, введите данные")

    answer = make_argument_message(arg_name=arg["argument_name"], arg_description=arg["argument_description"],
                                   arg_type=arg["type"])
    await send_message(chat_id=chat_id, text=answer)


def encode_binary(raw: bytes):
    return base64.b64encode(raw)


def decode_text(text: str):
    return base64.b64decode(text)
