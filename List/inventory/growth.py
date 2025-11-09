from dataclasses import dataclass, field
from enum import Enum

from List.configDict import itemType
from List.inventory.item import InventoryItem


class GrowthType(Enum):
    HIGH_JUMP = "High Jump"
    QUICK_RUN = "Quick Run"
    AERIAL_DODGE = "Aerial Dodge"
    GLIDE = "Glide"
    DODGE_ROLL = "Dodge Roll"


@dataclass(frozen=True)
class GrowthAbility(InventoryItem):
    id: int
    name: str
    type: itemType = field(init=False, default=itemType.GROWTH_ABILITY)
    growth_type: GrowthType
    growth_level: int


HighJump1 = GrowthAbility(94, "High Jump", GrowthType.HIGH_JUMP, 1)
HighJump2 = GrowthAbility(95, "High Jump", GrowthType.HIGH_JUMP, 2)
HighJump3 = GrowthAbility(96, "High Jump", GrowthType.HIGH_JUMP, 3)
HighJumpMax = GrowthAbility(97, "High Jump", GrowthType.HIGH_JUMP, 4)
QuickRun1 = GrowthAbility(98, "Quick Run", GrowthType.QUICK_RUN, 1)
QuickRun2 = GrowthAbility(99, "Quick Run", GrowthType.QUICK_RUN, 2)
QuickRun3 = GrowthAbility(100, "Quick Run", GrowthType.QUICK_RUN, 3)
QuickRunMax = GrowthAbility(101, "Quick Run", GrowthType.QUICK_RUN, 4)
AerialDodge1 = GrowthAbility(102, "Aerial Dodge", GrowthType.AERIAL_DODGE, 1)
AerialDodge2 = GrowthAbility(103, "Aerial Dodge", GrowthType.AERIAL_DODGE, 2)
AerialDodge3 = GrowthAbility(104, "Aerial Dodge", GrowthType.AERIAL_DODGE, 3)
AerialDodgeMax = GrowthAbility(105, "Aerial Dodge", GrowthType.AERIAL_DODGE, 4)
Glide1 = GrowthAbility(106, "Glide", GrowthType.GLIDE, 1)
Glide2 = GrowthAbility(107, "Glide", GrowthType.GLIDE, 2)
Glide3 = GrowthAbility(108, "Glide", GrowthType.GLIDE, 3)
GlideMax = GrowthAbility(109, "Glide", GrowthType.GLIDE, 4)
DodgeRoll1 = GrowthAbility(564, "Dodge Roll", GrowthType.DODGE_ROLL, 1)
DodgeRoll2 = GrowthAbility(565, "Dodge Roll", GrowthType.DODGE_ROLL, 2)
DodgeRoll3 = GrowthAbility(566, "Dodge Roll", GrowthType.DODGE_ROLL, 3)
DodgeRollMax = GrowthAbility(567, "Dodge Roll", GrowthType.DODGE_ROLL, 4)


def all_growth() -> list[GrowthAbility]:
    return [
        HighJump1, HighJump2, HighJump3, HighJumpMax,
        QuickRun1, QuickRun2, QuickRun3, QuickRunMax,
        AerialDodge1, AerialDodge2, AerialDodge3, AerialDodgeMax,
        Glide1, Glide2, Glide3, GlideMax,
        DodgeRoll1, DodgeRoll2, DodgeRoll3, DodgeRollMax,
    ]


def all_growth_to_level(growth_level: int) -> list[GrowthAbility]:
    return [g for g in all_growth() if g.growth_level <= growth_level]


def growth_to_level(growth_level: int, growth_type: GrowthType) -> list[GrowthAbility]:
    return [g for g in all_growth_to_level(growth_level) if g.growth_type == growth_type]


def all_unique_growth_types() -> list[GrowthType]:
    return [
        GrowthType.HIGH_JUMP,
        GrowthType.QUICK_RUN,
        GrowthType.DODGE_ROLL,
        GrowthType.AERIAL_DODGE,
        GrowthType.GLIDE,
    ]


def all_individual_growth_types() -> list[GrowthType]:
    result: list[GrowthType] = []
    for unique in all_unique_growth_types():
        result.extend([unique] * 4)
    return result
