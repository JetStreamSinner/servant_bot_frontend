import base64
import io
from typing import Any, Dict

from aiogram import types

import argument_types


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


async def get_last_image_binary(message: types.Message):
    last_image = message.photo.pop()
    image_binary = io.BytesIO()
    await last_image.download(destination_file=image_binary)
    return image_binary.getvalue()


async def resolve_argument(message: types.Message, raw_argument: Dict[str, Any]):
    argument_name = raw_argument["argument_name"]
    argument_type = raw_argument["type"]

    async def resolve_value():
        match argument_type:
            case argument_types.Image:
                image_data = await get_last_image_binary(message)
                encoded_image = encode_binary(raw=image_data)
                return encoded_image
            case argument_types.Text:
                return message.text
            case _:
                raise RuntimeError("Unknown argument type")

    resolved_value = await resolve_value()
    return argument_name, resolved_value


async def show_result(message: types.Message, response):
    result_type = response["type"]

    match result_type:
        case argument_types.Image:
            encoded_image = response["data"]
            image_data = decode_text(text=encoded_image)
            await message.answer_photo(photo=image_data)
        case argument_types.Text:
            response_text = response["data"]
            await message.answer(text=response_text)
        case _:
            pass


def encode_binary(raw: bytes):
    return base64.b64encode(raw)


def decode_text(text: str):
    return base64.b64decode(text)
