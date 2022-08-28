import os
from typing import Dict, Any, List
import requests


def get_services() -> List[Dict[str, Any]]:
    # TODO Use reverse proxy
    backend_url = os.getenv("backend")
    service_list_router = "/services_list"
    target_url = backend_url + service_list_router
    services_list_request = requests.get(target_url)
    return services_list_request.json()
