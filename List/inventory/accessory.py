from dataclasses import dataclass, field

from List.configDict import itemType
from List.inventory.item import InventoryItem


@dataclass(frozen=True)
class Accessory(InventoryItem):
    id: int
    name: str
    type: itemType = field(init=False, default=itemType.ACCESSORY)


AbilityRing = Accessory(8, "Ability Ring")
EngineersRing = Accessory(9, "Engineer's Ring")
TechniciansRing = Accessory(10, "Technician's Ring")
ExpertsRing = Accessory(11, "Expert's Ring")
SardonyxRing = Accessory(12, "Sardonyx Ring")
TourmalineRing = Accessory(13, "Tourmaline Ring")
AquamarineRing = Accessory(14, "Aquamarine Ring")
GarnetRing = Accessory(15, "Garnet Ring")
DiamondRing = Accessory(16, "Diamond Ring")
SilverRing = Accessory(17, "Silver Ring")
GoldRing = Accessory(18, "Gold Ring")
PlatinumRing = Accessory(19, "Platinum Ring")
MythrilRing = Accessory(20, "Mythril Ring")
OrichalcumRing = Accessory(28, "Orichalcum Ring")
MastersRing = Accessory(34, "Master's Ring")
MoonAmulet = Accessory(35, "Moon Amulet")
StarCharm = Accessory(36, "Star Charm")
SkillRing = Accessory(38, "Skill Ring")
SkillfulRing = Accessory(39, "Skillful Ring")
SoldierEarring = Accessory(40, "Soldier Earring")
FencerEarring = Accessory(46, "Fencer Earring")
MageEarring = Accessory(47, "Mage Earring")
SlayerEarring = Accessory(48, "Slayer Earring")
CosmicRing = Accessory(52, "Cosmic Ring")
Medal = Accessory(53, "Medal")
CosmicArts = Accessory(56, "Cosmic Arts")
ShadowArchive = Accessory(57, "Shadow Archive")
ShadowArchivePlus = Accessory(58, "Shadow Archive+")
LuckyRing = Accessory(63, "Lucky Ring")
FullBloom = Accessory(64, "Full Bloom")
DrawRing = Accessory(65, "Draw Ring")
FullBloomPlus = Accessory(66, "Full Bloom+")
ExecutivesRing = Accessory(599, "Executive's Ring")
