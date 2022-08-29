import enum
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import backend_requests
import helpers
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
    await message.reply(text="Root handler", reply_markup=markup)


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
        "index": 1,
        "arguments": service_info["arguments"]
    }

    argument = task_data["arguments"][0]
    await helpers.send_req_for_arg(arg=argument, message=query.message)
    await state.set_data(data=task_data)
    await TaskForm.next()


async def next_argument_state_handler(message: types.Message, state: FSMContext):
    task_data = await state.get_data()
    arg_index = task_data["index"]
    if arg_index >= len(task_data["arguments"]):
        return

    argument = task_data["arguments"][arg_index]
    await helpers.send_req_for_arg(arg=argument, message=message)

    task_data["index"] += 1
    await state.set_data(data=task_data)
    await TaskForm.next_argument.set()


def get_commands_handler_bind():
    binding = [
        {
            "filters": {
                "commands": ["start"]
            },
            "handler": root_handler,
            "handler_type": HandlerType.MessageHandler
        },
        {
            "filters": {
                "commands": ["about"]
            },
            "handler": about_handler,
            "handler_type": HandlerType.MessageHandler
        },
        {
            "filters": {
                "commands": ["services"]
            },
            "handler": services_list_handler,
            "handler_type": HandlerType.MessageHandler
        },
        {
            "filters": {
                "state": [TaskForm.next_argument]
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
