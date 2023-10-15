from dataclasses import dataclass, field

from List.configDict import itemType
from List.inventory.item import InventoryItem


@dataclass(frozen=True)
class SummonCharm(InventoryItem):
    id: int
    name: str
    type: itemType = field(init=False, default=itemType.SUMMON)


UkuleleCharm = SummonCharm(25, "Ukulele Charm (Stitch)")
LampCharm = SummonCharm(159, "Lamp Charm (Genie)")
FeatherCharm = SummonCharm(160, "Feather Charm (Peter Pan)")
BaseballCharm = SummonCharm(383, "Baseball Charm (Chicken Little)")


def all_summon_charms() -> list[SummonCharm]:
    return [LampCharm, FeatherCharm, UkuleleCharm, BaseballCharm]
