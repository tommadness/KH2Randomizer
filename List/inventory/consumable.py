from dataclasses import dataclass, field

from List.configDict import itemType
from List.inventory.item import InventoryItem


@dataclass(frozen=True)
class Consumable(InventoryItem):
    id: int
    name: str
    type: itemType = field(init=False, default=itemType.ITEM)


Potion = Consumable(1, "Potion")
HiPotion = Consumable(2, "Hi-Potion")
Ether = Consumable(3, "Ether")
Elixir = Consumable(4, "Elixir")
MegaPotion = Consumable(5, "Mega-Potion")
MegaEther = Consumable(6, "Mega-Ether")
Megalixir = Consumable(7, "Megalixir")
Tent = Consumable(131, "Tent")
DriveRecovery = Consumable(274, "Drive Recovery")
HighDriveRecovery = Consumable(275, "High Drive Recovery")
PowerBoost = Consumable(276, "Power Boost")
MagicBoost = Consumable(277, "Magic Boost")
DefenseBoost = Consumable(278, "Defense Boost")
ApBoost = Consumable(279, "AP Boost")
