from dataclasses import dataclass, field

from List.configDict import itemType
from List.inventory.item import InventoryItem


@dataclass(frozen=True)
class Staff(InventoryItem):
    id: int
    name: str
    type: itemType = field(init=False, default=itemType.STAFF)
    stat_entry: int


MeteorStaff = Staff(150, "Meteor Staff", stat_entry=89)
RisingDragon = Staff(154, "Rising Dragon", stat_entry=93)
NobodyLance = Staff(155, "Nobody Lance", stat_entry=94)
ShamansRelic = Staff(156, "Shaman's Relic", stat_entry=95)
SaveTheQueenPlus = Staff(503, "Save The Queen+", stat_entry=146)
PreciousMushroom = Staff(549, "Precious Mushroom", stat_entry=154)
PreciousMushroomPlus = Staff(550, "Precious Mushroom+", stat_entry=155)
PremiumMushroom = Staff(551, "Premium Mushroom", stat_entry=156)
CenturionPlus = Staff(546, "Centurion+", stat_entry=151)
