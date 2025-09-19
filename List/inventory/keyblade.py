from dataclasses import dataclass, field
from typing import Optional

from List.configDict import itemType
from List.inventory import ability
from List.inventory.item import InventoryItem
from List.location import weaponslot


@dataclass(frozen=True)
class Keyblade(InventoryItem):
    id: int
    name: str
    weaponslot_id: int
    strength: int
    magic: int
    ability: Optional[ability.Ability]
    start_item_eligible: bool
    can_unlock_chests: bool
    struggle_weapon: bool = field(init=True, default=False)
    type: itemType = field(init=False, default=itemType.KEYBLADE)


KingdomKey = Keyblade(
    41,
    "Kingdom Key",
    weaponslot_id=weaponslot.LocationId.KingdomKey,
    strength=3,
    magic=1,
    ability=ability.DamageControl,
    start_item_eligible=False,
    can_unlock_chests=False,
)
Oathkeeper = Keyblade(
    42,
    "Oathkeeper",
    weaponslot_id=weaponslot.LocationId.Oathkeeper,
    strength=3,
    magic=3,
    ability=ability.FormBoost,
    start_item_eligible=True,
    can_unlock_chests=True,
)
Oblivion = Keyblade(
    43,
    "Oblivion",
    weaponslot_id=weaponslot.LocationId.Oblivion,
    strength=6,
    magic=2,
    ability=ability.DriveBoost,
    start_item_eligible=True,
    can_unlock_chests=False,
)
StarSeeker = Keyblade(
    480,
    "Star Seeker",
    weaponslot_id=weaponslot.LocationId.StarSeeker,
    strength=3,
    magic=1,
    ability=ability.AirComboPlus,
    start_item_eligible=True,
    can_unlock_chests=False,
)
HiddenDragon = Keyblade(
    481,
    "Hidden Dragon",
    weaponslot_id=weaponslot.LocationId.HiddenDragon,
    strength=2,
    magic=2,
    ability=ability.MpRage,
    start_item_eligible=True,
    can_unlock_chests=True,
)
HerosCrest = Keyblade(
    484,
    "Hero's Crest",
    weaponslot_id=weaponslot.LocationId.HerosCrest,
    strength=4,
    magic=0,
    ability=ability.AirComboBoost,
    start_item_eligible=True,
    can_unlock_chests=True,
)
Monochrome = Keyblade(
    485,
    "Monochrome",
    weaponslot_id=weaponslot.LocationId.Monochrome,
    strength=3,
    magic=2,
    ability=ability.ItemBoost,
    start_item_eligible=True,
    can_unlock_chests=True,
)
FollowTheWind = Keyblade(
    486,
    "Follow the Wind",
    weaponslot_id=weaponslot.LocationId.FollowTheWind,
    strength=3,
    magic=1,
    ability=ability.Draw,
    start_item_eligible=True,
    can_unlock_chests=True,
)
CircleOfLife = Keyblade(
    487,
    "Circle of Life",
    weaponslot_id=weaponslot.LocationId.CircleOfLife,
    strength=4,
    magic=1,
    ability=ability.MpHaste,
    start_item_eligible=True,
    can_unlock_chests=True,
)
PhotonDebugger = Keyblade(
    488,
    "Photon Debugger",
    weaponslot_id=weaponslot.LocationId.PhotonDebugger,
    strength=2,
    magic=1,
    ability=ability.ThunderBoost,
    start_item_eligible=True,
    can_unlock_chests=True,
)
GullWing = Keyblade(
    489,
    "Gull Wing",
    weaponslot_id=weaponslot.LocationId.GullWing,
    strength=2,
    magic=3,
    ability=ability.ExperienceBoost,
    start_item_eligible=True,
    can_unlock_chests=False,
)
RumblingRose = Keyblade(
    490,
    "Rumbling Rose",
    weaponslot_id=weaponslot.LocationId.RumblingRose,
    strength=5,
    magic=0,
    ability=ability.FinishingPlus,
    start_item_eligible=True,
    can_unlock_chests=True,
)
GuardianSoul = Keyblade(
    491,
    "Guardian Soul",
    weaponslot_id=weaponslot.LocationId.GuardianSoul,
    strength=5,
    magic=1,
    ability=ability.ReactionBoost,
    start_item_eligible=True,
    can_unlock_chests=False,
)
WishingLamp = Keyblade(
    492,
    "Wishing Lamp",
    weaponslot_id=weaponslot.LocationId.WishingLamp,
    strength=4,
    magic=3,
    ability=ability.Jackpot,
    start_item_eligible=True,
    can_unlock_chests=True,
)
DecisivePumpkin = Keyblade(
    493,
    "Decisive Pumpkin",
    weaponslot_id=weaponslot.LocationId.DecisivePumpkin,
    strength=6,
    magic=1,
    ability=ability.ComboBoost,
    start_item_eligible=True,
    can_unlock_chests=True,
)
SweetMemories = Keyblade(
    495,
    "Sweet Memories",
    weaponslot_id=weaponslot.LocationId.SweetMemories,
    strength=0,
    magic=4,
    ability=ability.DriveConverter,
    start_item_eligible=True,
    can_unlock_chests=True,
)
MysteriousAbyss = Keyblade(
    496,
    "Mysterious Abyss",
    weaponslot_id=weaponslot.LocationId.MysteriousAbyss,
    strength=3,
    magic=3,
    ability=ability.BlizzardBoost,
    start_item_eligible=True,
    can_unlock_chests=False,
)
SleepingLion = Keyblade(
    494,
    "Sleeping Lion",
    weaponslot_id=weaponslot.LocationId.SleepingLion,
    strength=5,
    magic=3,
    ability=ability.ComboPlus,
    start_item_eligible=True,
    can_unlock_chests=True,
)
BondOfFlame = Keyblade(
    498,
    "Bond of Flame",
    weaponslot_id=weaponslot.LocationId.BondOfFlame,
    strength=4,
    magic=4,
    ability=ability.FireBoost,
    start_item_eligible=True,
    can_unlock_chests=True,
)
TwoBecomeOne = Keyblade(
    543,
    "Two Become One",
    weaponslot_id=weaponslot.LocationId.TwoBecomeOne,
    strength=5,
    magic=4,
    ability=ability.LightAndDarkness,
    start_item_eligible=True,
    can_unlock_chests=True,
)
FatalCrest = Keyblade(
    497,
    "Fatal Crest",
    weaponslot_id=weaponslot.LocationId.FatalCrest,
    strength=3,
    magic=5,
    ability=ability.BerserkCharge,
    start_item_eligible=True,
    can_unlock_chests=False,
)
Fenrir = Keyblade(
    499,
    "Fenrir",
    weaponslot_id=weaponslot.LocationId.Fenrir,
    strength=7,
    magic=1,
    ability=ability.NegativeCombo,
    start_item_eligible=True,
    can_unlock_chests=False,
)
UltimaWeapon = Keyblade(
    500,
    "Ultima Weapon",
    weaponslot_id=weaponslot.LocationId.UltimaWeapon,
    strength=6,
    magic=4,
    ability=ability.MpHastega,
    start_item_eligible=True,
    can_unlock_chests=False,
)
WinnersProof = Keyblade(
    544,
    "Winner's Proof",
    weaponslot_id=weaponslot.LocationId.WinnersProof,
    strength=5,
    magic=7,
    ability=ability.NoExperience,
    start_item_eligible=True,
    can_unlock_chests=True,
)
StruggleSword = Keyblade(
    384,
    "Struggle Sword",
    weaponslot_id=weaponslot.LocationId.StruggleSword,
    strength=3,
    magic=0,
    ability=None,
    start_item_eligible=False,
    can_unlock_chests=False,
    struggle_weapon=True,
)
StruggleWand = Keyblade(
    501,
    "Struggle Wand",
    weaponslot_id=weaponslot.LocationId.StruggleWand,
    strength=3,
    magic=0,
    ability=None,
    start_item_eligible=False,
    can_unlock_chests=False,
    struggle_weapon=True,
)
StruggleHammer = Keyblade(
    502,
    "Struggle Hammer",
    weaponslot_id=weaponslot.LocationId.StruggleHammer,
    strength=3,
    magic=0,
    ability=None,
    start_item_eligible=False,
    can_unlock_chests=False,
    struggle_weapon=True,
)
# Detection Saber / Alpha Weapon
AlphaWeapon = Keyblade(
    44,
    "Alpha Weapon",
    weaponslot_id=weaponslot.LocationId.AlphaWeapon,
    strength=4,
    magic=6,
    ability=ability.MpHastera,
    start_item_eligible=False,
    can_unlock_chests=False,
)
# Frontier of Ultima / Omega Weapon
OmegaWeapon = Keyblade(
    45,
    "Omega Weapon",
    weaponslot_id=weaponslot.LocationId.OmegaWeapon,
    strength=3,
    magic=6,
    ability=ability.AirComboBoost,
    start_item_eligible=False,
    can_unlock_chests=False,
)
# Antiform Dummy / Pureblood
Pureblood = Keyblade(
    71,
    "Pureblood",
    weaponslot_id=weaponslot.LocationId.Pureblood,
    strength=6,
    magic=0,
    ability=ability.DamageDrive,
    start_item_eligible=True,
    can_unlock_chests=False,
)
# FAKE / Kingdom Key D
KingdomKeyD = Keyblade(
    81,
    "Kingdom Key D",
    weaponslot_id=weaponslot.LocationId.KingdomKeyD,
    strength=1,
    magic=3,
    ability=ability.Defender,
    start_item_eligible=False,
    can_unlock_chests=False,
)


def get_all_keyblades() -> list[Keyblade]:
    """Returns a list of all available keyblades, including the Struggle weapons and form keyblades."""
    return [
        KingdomKey,
        Oathkeeper,
        Oblivion,
        StarSeeker,
        HiddenDragon,
        HerosCrest,
        Monochrome,
        FollowTheWind,
        CircleOfLife,
        PhotonDebugger,
        GullWing,
        RumblingRose,
        GuardianSoul,
        WishingLamp,
        DecisivePumpkin,
        SweetMemories,
        MysteriousAbyss,
        SleepingLion,
        BondOfFlame,
        TwoBecomeOne,
        FatalCrest,
        Fenrir,
        UltimaWeapon,
        WinnersProof,
        StruggleSword,
        StruggleWand,
        StruggleHammer,
        AlphaWeapon,
        OmegaWeapon,
        Pureblood,
        KingdomKeyD,
    ]


def get_locking_keyblades() -> list[Keyblade]:
    """Returns a list of the keyblades that can lock chests if the associated setting is enabled."""
    return [key for key in get_all_keyblades() if key.can_unlock_chests]
