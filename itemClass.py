from configDict import itemType
from dataclasses import dataclass
from json import JSONEncoder

@dataclass (frozen=True)
class KH2Item:
    Id: int
    Name: str
    ItemType: itemType

class ItemEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__




