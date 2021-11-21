from enum import Enum
from List.configDict import itemType
from dataclasses import dataclass
from json import JSONEncoder

class itemRarity(str, Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    MYTHIC = "Mythic"

@dataclass (frozen=True)
class KH2Item:
    Id: int
    Name: str
    ItemType: itemType
    Rarity: itemRarity = itemRarity.COMMON

class ItemEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__




