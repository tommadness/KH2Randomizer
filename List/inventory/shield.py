from dataclasses import dataclass, field

from List.configDict import itemType
from List.inventory.item import InventoryItem


@dataclass(frozen=True)
class Shield(InventoryItem):
    id: int
    name: str
    type: itemType = field(init=False, default=itemType.SHIELD)
    stat_entry: int


AkashicRecord = Shield(146, "Akashic Record", stat_entry=107)
FrozenPridePlus = Shield(553, "Frozen Pride+", stat_entry=158)
GenjiShield = Shield(145, "Genji Shield", stat_entry=106)
MajesticMushroom = Shield(556, "Majestic Mushroom", stat_entry=161)
MajesticMushroomPlus = Shield(557, "Majestic Mushroom+", stat_entry=162)
NobodyGuard = Shield(147, "Nobody Guard", stat_entry=108)
OgreShield = Shield(141, "Ogre Shield", stat_entry=102)
SaveTheKingPlus = Shield(504, "Save The King+", stat_entry=147)
UltimateMushroom = Shield(558, "Ultimate Mushroom", stat_entry=163)
