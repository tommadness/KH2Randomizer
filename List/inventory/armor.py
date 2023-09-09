from dataclasses import dataclass, field

from List.configDict import itemType
from List.inventory.item import InventoryItem


@dataclass(frozen=True)
class Armor(InventoryItem):
    id: int
    name: str
    type: itemType = field(init=False, default=itemType.ARMOR)


ElvenBandanna = Armor(67, "Elven Bandana")
DivineBandanna = Armor(68, "Divine Bandana")
PowerBand = Armor(69, "Power Band")
BusterBand = Armor(70, "Buster Band")
ProtectBelt = Armor(78, "Protect Belt")
GaiaBelt = Armor(79, "Gaia Belt")
CosmicBelt = Armor(111, "Cosmic Belt")
ShockCharm = Armor(132, "Shock Charm")
ShockCharmPlus = Armor(133, "Shock Charm+")
GrandRibbon = Armor(157, "Grand Ribbon")
FireBangle = Armor(173, "Fire Bangle")
FiraBangle = Armor(174, "Fira Bangle")
FiragaBangle = Armor(197, "Firaga Bangle")
FiragunBangle = Armor(284, "Firagun Bangle")
BlizzardArmlet = Armor(286, "Blizzard Armlet")
BlizzaraArmlet = Armor(287, "Blizzara Armlet")
BlizzagaArmlet = Armor(288, "Blizzaga Armlet")
BlizzagunArmlet = Armor(289, "Blizzagun Armlet")
ThunderTrinket = Armor(291, "Thunder Trinket")
ThundaraTrinket = Armor(292, "Thundara Trinket")
ThundagaTrinket = Armor(293, "Thundaga Trinket")
ThundagunTrinket = Armor(294, "Thundagun Trinket")
ShadowAnklet = Armor(296, "Shadow Anklet")
DarkAnklet = Armor(297, "Dark Anklet")
MidnightAnklet = Armor(298, "Midnight Anklet")
ChaosAnklet = Armor(299, "Chaos Anklet")
AbasChain = Armor(301, "Abas Chain")
AegisChain = Armor(302, "Aegis Chain")
Acrisius = Armor(303, "Acrisius")
Ribbon = Armor(304, "Ribbon")
ChampionBelt = Armor(305, "Champion Belt")
PetiteRibbon = Armor(306, "Petite Ribbon")
AcrisiusPlus = Armor(307, "Acrisius+")
CosmicChain = Armor(308, "Cosmic Chain")
