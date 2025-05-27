from List.configDict import itemType, itemRarity
from dataclasses import dataclass, field
from json import JSONEncoder

from List.inventory.item import InventoryItem


@dataclass(frozen=True)
class KH2Item:
    item: InventoryItem
    Rarity: itemRarity = itemRarity.COMMON
    Id: int = field(init=False)
    Name: str = field(init=False)
    ItemType: itemType = field(init=False)

    def __post_init__(self):
        # Working around the frozen-ness here to set these
        object.__setattr__(self, "Id", self.item.id)
        object.__setattr__(self, "Name", self.item.name)
        object.__setattr__(self, "ItemType", self.item.type)

    def __lt__(self,value):
        return self.Id < value.Id


class ItemEncoder(JSONEncoder):

    def default(self, o):
        # Keep the JSON the same as it was previously even though we changed the structure a bit
        if isinstance(o, KH2Item):
            return {
                "Id": o.Id,
                "Name": o.Name,
                "ItemType": o.ItemType,
                "Rarity": o.Rarity
            }
        else:
            return o.__dict__
