from dataclasses import dataclass

from List.configDict import itemType
from List.inventory.item import InventoryItem


@dataclass(frozen=True)
class BonusItem(InventoryItem):
    id: int
    name: str
    type: itemType


ItemSlotUp = BonusItem(463, "Item Slot Up", itemType.SLOT)  # Dummy 16
MaxHpUp = BonusItem(470, "Max HP Up", itemType.GAUGE)  # Dummy 23
MaxMpUp = BonusItem(471, "Max MP Up", itemType.GAUGE)  # Dummy 24
DriveGaugeUp = BonusItem(472, "Drive Gauge Up", itemType.GAUGE)  # Dummy 25
ArmorSlotUp = BonusItem(473, "Armor Slot Up", itemType.SLOT)  # Dummy 26
AccessorySlotUp = BonusItem(474, "Accessory Slot Up", itemType.SLOT)  # Dummy 27
