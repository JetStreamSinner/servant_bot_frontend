import os
from typing import Dict, Any, List
import requests


def get_request(router: str) -> List[Dict[str, Any]]:
    # TODO Use reverse proxy
    backend_url = os.getenv("backend")
    target_url = backend_url + router
    response = requests.get(target_url)
    return response.json()


def get_services() -> List[Dict[str, Any]]:
    service_list_router = "/services_list"
    return get_request(router=service_list_router)


def get_service_info(service_id: int) -> List[Dict[str, Any]]:
    service_info_router = "/service_info/{0}".format(service_id)
    return get_request(router=service_info_router)
