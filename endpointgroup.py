from typing import Optional
import json

class EndpointGroup:
    id: str
    name: str
    description: str

    def __init__(self, name: str, id: Optional[str] = "", description: Optional[str] = ""):
        self.id = id
        self.name = name
        self.description = description

    def setID(self, id: str):
        self.id = id

    def toJSON(self):
        return {
            "EndPointGroup" : {
                "id" : self.id,
                "name" : self.name,
                "description" : self.description,
                "systemDefined" : "false"
            }
        }