from typing import Dict

class HttpResponse:
    def __init__(self, body: Dict, status_code: int) -> None:
        self.body = bodyself
        self.status_code = status_code