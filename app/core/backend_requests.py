import os
from typing import Dict, Any

import requests


def get_request(router: str) -> Any:
    # TODO Use reverse proxy
    backend_url = os.getenv("backend")
    target_url = backend_url + router
    response = requests.get(target_url)
    return response.json()


def post_request(router: str, body: Dict[str, Any]) -> Any:
    backend_url = os.getenv("backend")
    target_url = backend_url + router
    response = requests.post(target_url, json=body)
    return response.json()


def get_services() -> Any:
    service_list_router = "/services_list"
    return get_request(router=service_list_router)


def get_service_info(service_id: int) -> Any:
    service_info_router = "/service_info/{0}".format(service_id)
    return get_request(router=service_info_router)


def post_task(service_id: int, task_data: Dict[str, Any]):
    post_task_router = "/add_task/{0}".format(service_id)
    return post_request(router=post_task_router, body=task_data)
