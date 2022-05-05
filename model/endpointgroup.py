from typing import Optional
import json

class EndpointGroup:
    id: str
    name: str
    description: str
    systemDefined: bool

    def __init__(self, name: str, id: Optional[str] = "", description: Optional[str] = "", systemDefined: Optional[bool] = False):
        self.id = id
        self.systemDefined = systemDefined
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
                "systemDefined" : self.systemDefined
            }
        }
    
    def __repr__(self):
        return json.dumps(self.toJSON())