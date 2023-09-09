from dataclasses import dataclass, field
from typing import Optional

from List.configDict import itemType, locationCategory
from List.inventory.item import InventoryItem


@dataclass(frozen=True)
class DriveForm(InventoryItem):
    id: int
    name: str
    short_name: str
    level_category: Optional[locationCategory]
    type: itemType = field(init=False, default=itemType.FORM)


ValorForm = DriveForm(26, "Valor Form", "Valor", locationCategory.VALORLEVEL)
WisdomForm = DriveForm(27, "Wisdom Form", "Wisdom", locationCategory.WISDOMLEVEL)
FinalForm = DriveForm(29, "Final Form", "Final", locationCategory.FINALLEVEL)
AntiForm = DriveForm(30, "Anti-Form", "Anti", None)
MasterForm = DriveForm(31, "Master Form", "Master", locationCategory.MASTERLEVEL)
LimitForm = DriveForm(563, "Limit Form", "Limit", locationCategory.LIMITLEVEL)

DummyFinalForm = DriveForm(115, "Final Form", "Final", locationCategory.FINALLEVEL)  # (was Window of Time Map 2)
DummyValorForm = DriveForm(89, "Valor Form", "Valor", locationCategory.VALORLEVEL)  # (was Navigational Map)
