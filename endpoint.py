from typing import Optional
import json

class Endpoint:
    id: str
    name: str
    mac: str
    description: str

    def __init__(self, name: Optional[str] = "", mac: Optional[str] = "", id: Optional[str] = "", description: Optional[str] = ""):
        self.name = name
        self.id = id
        self.mac = mac
        self.description = description
        if name == "" and id == "":
            self.name = mac

    def setID(self, id: str):
        self.id = id

    def toJSON(self):
        return {
            "ERSEndPoint" : {
                "id" : self.id,
                "description" : self.description,
                "mac" : self.mac,
                "name" : self.name
            }
        }
        