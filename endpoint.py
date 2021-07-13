from typing import Optional

class Endpoint:
    id: str
    mac: str
    description: str

    def __init__(self, mac: str, id: Optional[str] = "", description: Optional[str] = ""):
        self.id = id
        self.mac = mac
        self.description = description