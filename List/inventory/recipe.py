from dataclasses import dataclass, field

from List.configDict import itemType
from List.inventory.item import InventoryItem


@dataclass(frozen=True)
class Recipe(InventoryItem):
    id: int
    name: str
    type: itemType = field(init=False, default=itemType.RECIPE)


MegaRecipe = Recipe(382, "Mega-Recipe")
StarRecipe = Recipe(449, "Star Recipe")
RecoveryRecipe = Recipe(450, "Recovery Recipe")
SkillRecipe = Recipe(451, "Skill Recipe")
GuardRecipe = Recipe(452, "Guard Recipe")
RoadToDiscovery = Recipe(464, "Road to Discovery")
StrengthBeyondStrength = Recipe(465, "Strength Beyond Strength")
BookOfShadows = Recipe(466, "Book of Shadows")
CloakedThunder = Recipe(467, "Cloaked Thunder")
EternalBlossom = Recipe(468, "Eternal Blossom")
RareDocument = Recipe(469, "Rare Document")
StyleRecipe = Recipe(475, "Style Recipe")
MoonRecipe = Recipe(476, "Moon Recipe")
QueenRecipe = Recipe(477, "Queen Recipe")
KingRecipe = Recipe(478, "King Recipe")
UltimateRecipe = Recipe(479, "Ultimate Recipe")
