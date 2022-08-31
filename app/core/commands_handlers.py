import enum
import io

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import backend_requests
import dependencies
import argument_types
from keyboard_markups import create_main_markup, services_list_markup


class HandlerType(enum.Enum):
    MessageHandler = 0
    CallbackQueryHandler = 1


class TaskForm(StatesGroup):
    select_service = State()
    next_argument = State()
    notify_service = State()


async def root_handler(message: types.Message):
    markup = create_main_markup()
    await message.answer(text="Root handler", reply_markup=markup)


async def about_handler(message: types.Message):
    await message.answer(text="About handler")


async def services_list_handler(message: types.Message):
    markup = services_list_markup()
    await message.answer(text="Service list handler", reply_markup=markup)
    await TaskForm.select_service.set()


async def select_service_handler(query: types.CallbackQuery, state: FSMContext):
    service_id = int(query.data)
    service_info = backend_requests.get_service_info(service_id=service_id)

    task_data = {
        "service_id": service_id,
        "index": 1,
        "arguments": service_info["arguments"],
        "data": {}
    }

    argument = task_data["arguments"][0]
    await dependencies.send_req_for_arg(arg=argument, message=query.message)
    await state.set_data(data=task_data)
    await TaskForm.next()


async def next_argument_state_handler(message: types.Message, state: FSMContext):

    task_data = await state.get_data()
    arg_index = task_data["index"]

    prev_arg_index = arg_index - 1
    prev_arg = task_data["arguments"][prev_arg_index]
    prev_arg_name = prev_arg["argument_name"]
    prev_arg_mime = prev_arg["type"]

    match prev_arg_mime:
        case argument_types.Image:
            last_image = message.photo.pop()
            image_binary = io.BytesIO()
            await last_image.download(destination_file=image_binary)
            encoded_image = dependencies.encode_binary(raw=image_binary.getvalue())
            task_data["data"][prev_arg_name] = encoded_image
        case argument_types.Text:
            task_data["data"][prev_arg_name] = message.text
        case _:
            pass

    if arg_index >= len(task_data["arguments"]):
        await TaskForm.select_service.set()
        response = backend_requests.post_task(service_id=task_data["service_id"], task_data=task_data["data"])
        # TODO Handler response
        await root_handler(message=message)
        return

    argument = task_data["arguments"][arg_index]
    await dependencies.send_req_for_arg(arg=argument, message=message)

    task_data["index"] += 1
    await state.set_data(data=task_data)
    await TaskForm.next_argument.set()


def get_commands_handler_bind():
    binding = [
        {
            "filters": {
                "commands": ["start"],
                "state": ["*"]
            },
            "handler": root_handler,
            "handler_type": HandlerType.MessageHandler
        },
        {
            "filters": {
                "commands": ["about"],
                "state": ["*"]
            },
            "handler": about_handler,
            "handler_type": HandlerType.MessageHandler
        },
        {
            "filters": {
                "commands": ["services"],
                "state": ["*"]
            },
            "handler": services_list_handler,
            "handler_type": HandlerType.MessageHandler
        },
        {
            "filters": {
                "state": [TaskForm.next_argument],
                "content_types": [types.ContentType.PHOTO, types.ContentType.TEXT]
            },
            "handler": next_argument_state_handler,
            "handler_type": HandlerType.MessageHandler
        },
        {
            "filters": {
                "state": [TaskForm.select_service]
            },
            "handler": select_service_handler,
            "handler_type": HandlerType.CallbackQueryHandler
        }
    ]
    return binding
