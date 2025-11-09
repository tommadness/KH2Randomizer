from dataclasses import dataclass

from List.configDict import itemType
from List.inventory.item import InventoryItem


@dataclass(frozen=True)
class MagicElement(InventoryItem):
    id: int
    name: str
    type: itemType


Fire = MagicElement(21, "Fire Element", itemType.FIRE)
Blizzard = MagicElement(22, "Blizzard Element", itemType.BLIZZARD)
Thunder = MagicElement(23, "Thunder Element", itemType.THUNDER)
Cure = MagicElement(24, "Cure Element", itemType.CURE)
Magnet = MagicElement(87, "Magnet Element", itemType.MAGNET)
Reflect = MagicElement(88, "Reflect Element", itemType.REFLECT)


def all_unique_magics() -> list[MagicElement]:
    return [Fire, Blizzard, Thunder, Cure, Magnet, Reflect]


def all_individual_magics() -> list[MagicElement]:
    result: list[MagicElement] = []
    for unique in all_unique_magics():
        result.extend([unique] * 3)
    return result
