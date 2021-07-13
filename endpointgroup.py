from typing import Optional

class EndpointGroup:
    id: str
    name: str
    description: str

    def __init__(self, name: str, id: Optional[str] = "", description: Optional[str] = ""):
        self.id = id
        self.name = name
        self.description = description