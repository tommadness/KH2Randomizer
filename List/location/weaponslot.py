from Class.newLocationClass import KH2Location
from List.configDict import locationCategory, locationType


class LocationId:
    KingdomKey = 80
    Oathkeeper = 81
    Oblivion = 82
    AlphaWeapon = 83
    OmegaWeapon = 84
    Pureblood = 85
    KingdomKeyD = 116
    StruggleSword = 122
    StarSeeker = 123
    HiddenDragon = 124
    HerosCrest = 127
    Monochrome = 128
    FollowTheWind = 129
    CircleOfLife = 130
    PhotonDebugger = 131
    GullWing = 132
    RumblingRose = 133
    GuardianSoul = 134
    WishingLamp = 135
    DecisivePumpkin = 136
    SleepingLion = 137
    SweetMemories = 138
    MysteriousAbyss = 139
    FatalCrest = 140
    BondOfFlame = 141
    Fenrir = 142
    UltimaWeapon = 143
    StruggleWand = 144
    StruggleHammer = 145
    TwoBecomeOne = 148
    WinnersProof = 149

    HammerStaff = 87
    CometStaff = 90
    LordsBroom = 91
    MagesStaff = 86
    VictoryBell = 88
    MeteorStaff = 89
    WisdomWand = 92
    RisingDragon = 93
    NobodyLance = 94
    ShamansRelic = 95
    SaveTheQueenPlus = 146
    CenturionPlus = 151
    PreciousMushroom = 154
    PreciousMushroomPlus = 155
    PremiumMushroom = 156

    KnightsShield = 99
    AdamantShield = 100
    ChainGear = 101
    OgreShield = 102
    FallingStar = 103
    DreamCloud = 104
    KnightDefender = 105
    GenjiShield = 106
    AkashicRecord = 107
    NobodyGuard = 108
    SaveTheKingPlus = 147
    MajesticMushroom = 161
    FrozenPridePlus = 158
    MajesticMushroomPlus = 162
    UltimateMushroom = 163


class CheckLocation:
    KingdomKeyD = "Kingdom Key D (Slot)"
    AlphaWeapon = "Alpha Weapon (Slot)"
    OmegaWeapon = "Omega Weapon (Slot)"
    KingdomKey = "Kingdom Key (Slot)"
    Oathkeeper = "Oathkeeper (Slot)"
    Oblivion = "Oblivion (Slot)"
    StarSeeker = "Star Seeker (Slot)"
    HiddenDragon = "Hidden Dragon (Slot)"
    HerosCrest = "Hero's Crest (Slot)"
    Monochrome = "Monochrome (Slot)"
    FollowTheWind = "Follow the Wind (Slot)"
    CircleOfLife = "Circle of Life (Slot)"
    PhotonDebugger = "Photon Debugger (Slot)"
    GullWing = "Gull Wing (Slot)"
    RumblingRose = "Rumbling Rose (Slot)"
    GuardianSoul = "Guardian Soul (Slot)"
    WishingLamp = "Wishing Lamp (Slot)"
    DecisivePumpkin = "Decisive Pumpkin (Slot)"
    SweetMemories = "Sweet Memories (Slot)"
    MysteriousAbyss = "Mysterious Abyss (Slot)"
    SleepingLion = "Sleeping Lion (Slot)"
    BondOfFlame = "Bond of Flame (Slot)"
    TwoBecomeOne = "Two Become One (Slot)"
    FatalCrest = "Fatal Crest (Slot)"
    Fenrir = "Fenrir (Slot)"
    UltimaWeapon = "Ultima Weapon (Slot)"
    WinnersProof = "Winner's Proof (Slot)"
    Pureblood = "Pureblood (Slot)"

    StruggleSword = "Struggle Sword (Slot)"
    StruggleWand = "Struggle Wand (Slot)"
    StruggleHammer = "Struggle Hammer (Slot)"

    CenturionPlus = "Centurion+"
    CometStaff = "Comet Staff"
    HammerStaff = "Hammer Staff"
    LordsBroom = "Lord's Broom"
    MagesStaff = "Mage's Staff"
    MeteorStaff = "Meteor Staff"
    NobodyLance = "Nobody Lance"
    PreciousMushroom = "Precious Mushroom"
    PreciousMushroomPlus = "Precious Mushroom+"
    PremiumMushroom = "Premium Mushroom"
    RisingDragon = "Rising Dragon"
    SaveTheQueenPlus = "Save the Queen+"
    ShamansRelic = "Shaman's Relic"
    VictoryBell = "Victory Bell"
    WisdomWand = "Wisdom Wand"

    AdamantShield = "Adamant Shield"
    AkashicRecord = "Akashic Record"
    ChainGear = "Chain Gear"
    DreamCloud = "Dream Cloud"
    FallingStar = "Falling Star"
    FrozenPridePlus = "Frozen Pride+"
    GenjiShield = "Genji Shield"
    KnightDefender = "Knight Defender"
    KnightsShield = "Knight's Shield"
    MajesticMushroom = "Majestic Mushroom"
    MajesticMushroomPlus = "Majestic Mushroom+"
    NobodyGuard = "Nobody Guard"
    OgreShield = "Ogre Shield"
    SaveTheKingPlus = "Save The King+"
    UltimateMushroom = "Ultimate Mushroom"


def weapon_slot(loc_id: int, description: str) -> KH2Location:
    return KH2Location(loc_id, description, locationCategory.WEAPONSLOT, [locationType.WeaponSlot])


def keyblade_slots() -> list[KH2Location]:
    return [
        weapon_slot(LocationId.KingdomKeyD, CheckLocation.KingdomKeyD),
        weapon_slot(LocationId.AlphaWeapon, CheckLocation.AlphaWeapon),
        weapon_slot(LocationId.OmegaWeapon, CheckLocation.OmegaWeapon),
        weapon_slot(LocationId.KingdomKey, CheckLocation.KingdomKey),
        weapon_slot(LocationId.Oathkeeper, CheckLocation.Oathkeeper),
        weapon_slot(LocationId.Oblivion, CheckLocation.Oblivion),
        weapon_slot(LocationId.StarSeeker, CheckLocation.StarSeeker),
        weapon_slot(LocationId.HiddenDragon, CheckLocation.HiddenDragon),
        weapon_slot(LocationId.HerosCrest, CheckLocation.HerosCrest),
        weapon_slot(LocationId.Monochrome, CheckLocation.Monochrome),
        weapon_slot(LocationId.FollowTheWind, CheckLocation.FollowTheWind),
        weapon_slot(LocationId.CircleOfLife, CheckLocation.CircleOfLife),
        weapon_slot(LocationId.PhotonDebugger, CheckLocation.PhotonDebugger),
        weapon_slot(LocationId.GullWing, CheckLocation.GullWing),
        weapon_slot(LocationId.RumblingRose, CheckLocation.RumblingRose),
        weapon_slot(LocationId.GuardianSoul, CheckLocation.GuardianSoul),
        weapon_slot(LocationId.WishingLamp, CheckLocation.WishingLamp),
        weapon_slot(LocationId.DecisivePumpkin, CheckLocation.DecisivePumpkin),
        weapon_slot(LocationId.SweetMemories, CheckLocation.SweetMemories),
        weapon_slot(LocationId.MysteriousAbyss, CheckLocation.MysteriousAbyss),
        weapon_slot(LocationId.SleepingLion, CheckLocation.SleepingLion),
        weapon_slot(LocationId.BondOfFlame, CheckLocation.BondOfFlame),
        weapon_slot(LocationId.TwoBecomeOne, CheckLocation.TwoBecomeOne),
        weapon_slot(LocationId.FatalCrest, CheckLocation.FatalCrest),
        weapon_slot(LocationId.Fenrir, CheckLocation.Fenrir),
        weapon_slot(LocationId.UltimaWeapon, CheckLocation.UltimaWeapon),
        weapon_slot(LocationId.WinnersProof, CheckLocation.WinnersProof),
        weapon_slot(LocationId.Pureblood, CheckLocation.Pureblood),
    ]


def struggle_weapon_slots() -> list[KH2Location]:
    return [
        weapon_slot(LocationId.StruggleSword, CheckLocation.StruggleSword),
        weapon_slot(LocationId.StruggleWand, CheckLocation.StruggleWand),
        weapon_slot(LocationId.StruggleHammer, CheckLocation.StruggleHammer),
    ]


def donald_staff_slots() -> list[KH2Location]:
    return [
        weapon_slot(LocationId.CenturionPlus, CheckLocation.CenturionPlus),
        weapon_slot(LocationId.CometStaff, CheckLocation.CometStaff),
        weapon_slot(LocationId.HammerStaff, CheckLocation.HammerStaff),
        weapon_slot(LocationId.LordsBroom, CheckLocation.LordsBroom),
        weapon_slot(LocationId.MagesStaff, CheckLocation.MagesStaff),
        weapon_slot(LocationId.MeteorStaff, CheckLocation.MeteorStaff),
        weapon_slot(LocationId.NobodyLance, CheckLocation.NobodyLance),
        weapon_slot(LocationId.PreciousMushroom, CheckLocation.PreciousMushroom),
        weapon_slot(LocationId.PreciousMushroomPlus, CheckLocation.PreciousMushroomPlus),
        weapon_slot(LocationId.PremiumMushroom, CheckLocation.PremiumMushroom),
        weapon_slot(LocationId.RisingDragon, CheckLocation.RisingDragon),
        weapon_slot(LocationId.SaveTheQueenPlus, CheckLocation.SaveTheQueenPlus),
        weapon_slot(LocationId.ShamansRelic, CheckLocation.ShamansRelic),
        weapon_slot(LocationId.VictoryBell, CheckLocation.VictoryBell),
        weapon_slot(LocationId.WisdomWand, CheckLocation.WisdomWand),
    ]


def goofy_shield_slots() -> list[KH2Location]:
    return [
        weapon_slot(LocationId.AdamantShield, CheckLocation.AdamantShield),
        weapon_slot(LocationId.AkashicRecord, CheckLocation.AkashicRecord),
        weapon_slot(LocationId.ChainGear, CheckLocation.ChainGear),
        weapon_slot(LocationId.DreamCloud, CheckLocation.DreamCloud),
        weapon_slot(LocationId.FallingStar, CheckLocation.FallingStar),
        weapon_slot(LocationId.FrozenPridePlus, CheckLocation.FrozenPridePlus),
        weapon_slot(LocationId.GenjiShield, CheckLocation.GenjiShield),
        weapon_slot(LocationId.KnightDefender, CheckLocation.KnightDefender),
        weapon_slot(LocationId.KnightsShield, CheckLocation.KnightsShield),
        weapon_slot(LocationId.MajesticMushroom, CheckLocation.MajesticMushroom),
        weapon_slot(LocationId.MajesticMushroomPlus, CheckLocation.MajesticMushroomPlus),
        weapon_slot(LocationId.NobodyGuard, CheckLocation.NobodyGuard),
        weapon_slot(LocationId.OgreShield, CheckLocation.OgreShield),
        weapon_slot(LocationId.SaveTheKingPlus, CheckLocation.SaveTheKingPlus),
        weapon_slot(LocationId.UltimateMushroom, CheckLocation.UltimateMushroom),
    ]
