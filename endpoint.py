from typing import Optional

class Endpoint:
    id: str
    name: str
    mac: str
    description: str

    def __init__(self, name: Optional[str] = "", mac: Optional[str] = "", id: Optional[str] = "", description: Optional[str] = ""):
        self.id = id
        self.name = name
        self.mac = mac
        self.description = description