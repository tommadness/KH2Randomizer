from configDict import itemType
from dataclasses import dataclass

@dataclass (frozen=True)
class KH2Item:
    Id: int
    Name: str
    ItemType: itemType



