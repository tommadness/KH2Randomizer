from dataclasses import dataclass, field

from List.configDict import itemType
from List.inventory.item import InventoryItem
from List.location import weaponslot


@dataclass(frozen=True)
class Keyblade(InventoryItem):
    id: int
    name: str
    weaponslot_id: int
    type: itemType = field(init=False, default=itemType.KEYBLADE)


Oathkeeper = Keyblade(42, "Oathkeeper", weaponslot_id=weaponslot.LocationId.Oathkeeper)
Oblivion = Keyblade(43, "Oblivion", weaponslot_id=weaponslot.LocationId.Oblivion)
Pureblood = Keyblade(71, "Pureblood", weaponslot_id=weaponslot.LocationId.Pureblood)  # Anti-Form Dummy
StarSeeker = Keyblade(480, "Star Seeker", weaponslot_id=weaponslot.LocationId.StarSeeker)
HiddenDragon = Keyblade(481, "Hidden Dragon", weaponslot_id=weaponslot.LocationId.HiddenDragon)
HerosCrest = Keyblade(484, "Hero's Crest", weaponslot_id=weaponslot.LocationId.HerosCrest)
Monochrome = Keyblade(485, "Monochrome", weaponslot_id=weaponslot.LocationId.Monochrome)
FollowTheWind = Keyblade(486, "Follow the Wind", weaponslot_id=weaponslot.LocationId.FollowTheWind)
CircleOfLife = Keyblade(487, "Circle of Life", weaponslot_id=weaponslot.LocationId.CircleOfLife)
PhotonDebugger = Keyblade(488, "Photon Debugger", weaponslot_id=weaponslot.LocationId.PhotonDebugger)
GullWing = Keyblade(489, "Gull Wing", weaponslot_id=weaponslot.LocationId.GullWing)
RumblingRose = Keyblade(490, "Rumbling Rose", weaponslot_id=weaponslot.LocationId.RumblingRose)
GuardianSoul = Keyblade(491, "Guardian Soul", weaponslot_id=weaponslot.LocationId.GuardianSoul)
WishingLamp = Keyblade(492, "Wishing Lamp", weaponslot_id=weaponslot.LocationId.WishingLamp)
DecisivePumpkin = Keyblade(493, "Decisive Pumpkin", weaponslot_id=weaponslot.LocationId.DecisivePumpkin)
SleepingLion = Keyblade(494, "Sleeping Lion", weaponslot_id=weaponslot.LocationId.SleepingLion)
SweetMemories = Keyblade(495, "Sweet Memories", weaponslot_id=weaponslot.LocationId.SweetMemories)
MysteriousAbyss = Keyblade(496, "Mysterious Abyss", weaponslot_id=weaponslot.LocationId.MysteriousAbyss)
FatalCrest = Keyblade(497, "Fatal Crest", weaponslot_id=weaponslot.LocationId.FatalCrest)
BondOfFlame = Keyblade(498, "Bond of Flame", weaponslot_id=weaponslot.LocationId.BondOfFlame)
Fenrir = Keyblade(499, "Fenrir", weaponslot_id=weaponslot.LocationId.Fenrir)
UltimaWeapon = Keyblade(500, "Ultima Weapon", weaponslot_id=weaponslot.LocationId.UltimaWeapon)
TwoBecomeOne = Keyblade(543, "Two Become One", weaponslot_id=weaponslot.LocationId.TwoBecomeOne)
WinnersProof = Keyblade(544, "Winner's Proof", weaponslot_id=weaponslot.LocationId.WinnersProof)
