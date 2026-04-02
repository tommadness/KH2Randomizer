from enum import Enum

from Class.newLocationClass import KH2Location
from List.configDict import locationCategory, locationType
from List.location.graph import START_NODE, DefaultLogicGraph, LocationGraphBuilder
from Module.itemPlacementRestriction import ItemPlacementHelpers

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

    AbilityRing = 48
    EngineersRing = 49
    TechniciansRing = 50
    ExpertsRing = 51
    SardonyxRing = 52
    TourmalineRing = 53
    AquamarineRing = 54
    GarnetRing = 55
    DiamondRing = 56
    SilverRing = 57
    GoldRing = 58
    PlatinumRing = 59
    MythrilRing = 60
    OrichalcumRing = 61
    MastersRing = 62
    MoonAmulet = 63
    StarCharm = 64
    SkillRing = 65
    SkillfulRing = 66
    SoldierEarring = 67
    FencerEarring = 68
    MageEarring = 69
    SlayerEarring = 70
    CosmicRing = 71
    Medal = 72
    CosmicArts = 73
    ShadowArchive = 74
    ShadowArchivePlus = 75
    LuckyRing = 76
    FullBloom = 77
    DrawRing = 78
    FullBloomPlus = 79
    ExecutivesRing = 164
    ElvenBandanna = 0
    DivineBandanna = 1
    PowerBand = 2
    BusterBand = 3
    ProtectBelt = 4
    GaiaBelt = 5
    CosmicBelt = 6
    ShockCharm = 7
    ShockCharmPlus = 8
    GrandRibbon = 9
    FireBangle = 12
    FiraBangle = 13
    FiragaBangle = 14
    FiragunBangle = 15
    BlizzardArmlet = 17
    BlizzaraArmlet = 18
    BlizzagaArmlet = 19
    BlizzagunArmlet = 20
    ThunderTrinket = 22
    ThundaraTrinket = 23
    ThundagaTrinket = 24
    ThundagunTrinket = 25
    ShadowAnklet = 27
    DarkAnklet = 28
    MidnightAnklet = 29
    ChaosAnklet = 30
    AbasChain = 32
    AegisChain = 33
    Acrisius = 34
    Ribbon = 35
    ChampionBelt = 36
    PetiteRibbon = 37
    AcrisiusPlus = 38
    CosmicChain = 39


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

    AbilityRing = "Ability Ring"
    EngineersRing = "Engineer's Ring"
    TechniciansRing = "Technician's Ring"
    ExpertsRing = "Expert's Ring"
    SardonyxRing = "Sardonyx Ring"
    TourmalineRing = "Tourmaline Ring"
    AquamarineRing = "Aquamarine Ring"
    GarnetRing = "Garnet Ring"
    DiamondRing = "Diamond Ring"
    SilverRing = "Silver Ring"
    GoldRing = "Gold Ring"
    PlatinumRing = "Platinum Ring"
    MythrilRing = "Mythril Ring"
    OrichalcumRing = "Orichalcum Ring"
    MastersRing = "Master's Ring"
    MoonAmulet = "Moon Amulet"
    StarCharm = "Star Charm"
    SkillRing = "Skill Ring"
    SkillfulRing = "Skillful Ring"
    SoldierEarring = "Soldier Earring"
    FencerEarring = "Fencer Earring"
    MageEarring = "Mage Earring"
    SlayerEarring = "Slayer Earring"
    CosmicRing = "Cosmic Ring"
    Medal = "Medal"
    CosmicArts = "Cosmic Arts"
    ShadowArchive = "Shadow Archive"
    ShadowArchivePlus = "Shadow Archive+"
    LuckyRing = "Lucky Ring"
    FullBloom = "Full Bloom"
    DrawRing = "Draw Ring"
    FullBloomPlus = "Full Bloom+"
    ExecutivesRing = "Executive's Ring"
    ElvenBandanna = "Elven Bandana"
    DivineBandanna = "Divine Bandana"
    PowerBand = "Power Band"
    BusterBand = "Buster Band"
    ProtectBelt = "Protect Belt"
    GaiaBelt = "Gaia Belt"
    CosmicBelt = "Cosmic Belt"
    ShockCharm = "Shock Charm"
    ShockCharmPlus = "Shock Charm+"
    GrandRibbon = "Grand Ribbon"
    FireBangle = "Fire Bangle"
    FiraBangle = "Fira Bangle"
    FiragaBangle = "Firaga Bangle"
    FiragunBangle = "Firagun Bangle"
    BlizzardArmlet = "Blizzard Armlet"
    BlizzaraArmlet = "Blizzara Armlet"
    BlizzagaArmlet = "Blizzaga Armlet"
    BlizzagunArmlet = "Blizzagun Armlet"
    ThunderTrinket = "Thunder Trinket"
    ThundaraTrinket = "Thundara Trinket"
    ThundagaTrinket = "Thundaga Trinket"
    ThundagunTrinket = "Thundagun Trinket"
    ShadowAnklet = "Shadow Anklet"
    DarkAnklet = "Dark Anklet"
    MidnightAnklet = "Midnight Anklet"
    ChaosAnklet = "Chaos Anklet"
    AbasChain = "Abas Chain"
    AegisChain = "Aegis Chain"
    Acrisius = "Acrisius"
    Ribbon = "Ribbon"
    ChampionBelt = "Champion Belt"
    PetiteRibbon = "Petite Ribbon"
    AcrisiusPlus = "Acrisius+"
    CosmicChain = "Cosmic Chain"

class NodeId(str,Enum):
    KingdomKeyDSlot = "Kingdom Key D (Slot)"
    AlphaWeaponSlot = "Alpha Weapon (Slot)"
    OmegaWeaponSlot = "Omega Weapon (Slot)"
    KingdomKeySlot = "Kingdom Key (Slot)"
    OathkeeperSlot = "Oathkeeper (Slot)"
    OblivionSlot = "Oblivion (Slot)"
    StarSeekerSlot = "Star Seeker (Slot)"
    HiddenDragonSlot = "Hidden Dragon (Slot)"
    HerosCrestSlot = "Hero's Crest (Slot)"
    MonochromeSlot = "Monochrome (Slot)"
    FollowTheWindSlot = "Follow the Wind (Slot)"
    CircleOfLifeSlot = "Circle of Life (Slot)"
    PhotonDebuggerSlot = "Photon Debugger (Slot)"
    GullWingSlot = "Gull Wing (Slot)"
    RumblingRoseSlot = "Rumbling Rose (Slot)"
    GuardianSoulSlot = "Guardian Soul (Slot)"
    WishingLampSlot = "Wishing Lamp (Slot)"
    DecisivePumpkinSlot = "Decisive Pumpkin (Slot)"
    SweetMemoriesSlot = "Sweet Memories (Slot)"
    MysteriousAbyssSlot = "Mysterious Abyss (Slot)"
    SleepingLionSlot = "Sleeping Lion (Slot)"
    BondOfFlameSlot = "Bond of Flame (Slot)"
    TwoBecomeOneSlot = "Two Become One (Slot)"
    FatalCrestSlot = "Fatal Crest (Slot)"
    FenrirSlot = "Fenrir (Slot)"
    UltimaWeaponSlot = "Ultima Weapon (Slot)"
    WinnersProofSlot = "Winner's Proof (Slot)"
    PurebloodSlot = "Pureblood (Slot)"
    StruggleSwordSlot = "Struggle Sword (Slot)"
    StruggleWandSlot = "Struggle Wand (Slot)"
    StruggleHammerSlot = "Struggle Hammer (Slot)"

def weapon_slot(loc_id: int, description: str) -> KH2Location:
    return KH2Location(loc_id, description, locationCategory.WEAPONSLOT, [locationType.WeaponSlot])

class WeaponSlotLogicGraph(DefaultLogicGraph):
    def __init__(self):
        DefaultLogicGraph.__init__(self,NodeId)
        self.logic[START_NODE][NodeId.KingdomKeyDSlot] = ItemPlacementHelpers.has_valor_form
        self.logic[START_NODE][NodeId.AlphaWeaponSlot] = ItemPlacementHelpers.has_master_form
        self.logic[START_NODE][NodeId.OmegaWeaponSlot] = ItemPlacementHelpers.has_final_form
        self.logic[START_NODE][NodeId.OathkeeperSlot] = ItemPlacementHelpers.make_keyblade_slot_logic_lambda(LocationId.Oathkeeper)
        self.logic[START_NODE][NodeId.OblivionSlot] = ItemPlacementHelpers.make_keyblade_slot_logic_lambda(LocationId.Oblivion)
        self.logic[START_NODE][NodeId.StarSeekerSlot] = ItemPlacementHelpers.make_keyblade_slot_logic_lambda(LocationId.StarSeeker)
        self.logic[START_NODE][NodeId.HiddenDragonSlot] = ItemPlacementHelpers.make_keyblade_slot_logic_lambda(LocationId.HiddenDragon)
        self.logic[START_NODE][NodeId.HerosCrestSlot] = ItemPlacementHelpers.make_keyblade_slot_logic_lambda(LocationId.HerosCrest)
        self.logic[START_NODE][NodeId.MonochromeSlot] = ItemPlacementHelpers.make_keyblade_slot_logic_lambda(LocationId.Monochrome)
        self.logic[START_NODE][NodeId.FollowTheWindSlot] = ItemPlacementHelpers.make_keyblade_slot_logic_lambda(LocationId.FollowTheWind)
        self.logic[START_NODE][NodeId.CircleOfLifeSlot] = ItemPlacementHelpers.make_keyblade_slot_logic_lambda(LocationId.CircleOfLife)
        self.logic[START_NODE][NodeId.PhotonDebuggerSlot] = ItemPlacementHelpers.make_keyblade_slot_logic_lambda(LocationId.PhotonDebugger)
        self.logic[START_NODE][NodeId.GullWingSlot] = ItemPlacementHelpers.make_keyblade_slot_logic_lambda(LocationId.GullWing)
        self.logic[START_NODE][NodeId.RumblingRoseSlot] = ItemPlacementHelpers.make_keyblade_slot_logic_lambda(LocationId.RumblingRose)
        self.logic[START_NODE][NodeId.GuardianSoulSlot] = ItemPlacementHelpers.make_keyblade_slot_logic_lambda(LocationId.GuardianSoul)
        self.logic[START_NODE][NodeId.WishingLampSlot] = ItemPlacementHelpers.make_keyblade_slot_logic_lambda(LocationId.WishingLamp)
        self.logic[START_NODE][NodeId.DecisivePumpkinSlot] = ItemPlacementHelpers.make_keyblade_slot_logic_lambda(LocationId.DecisivePumpkin)
        self.logic[START_NODE][NodeId.SweetMemoriesSlot] = ItemPlacementHelpers.make_keyblade_slot_logic_lambda(LocationId.SweetMemories)
        self.logic[START_NODE][NodeId.MysteriousAbyssSlot] = ItemPlacementHelpers.make_keyblade_slot_logic_lambda(LocationId.MysteriousAbyss)
        self.logic[START_NODE][NodeId.SleepingLionSlot] = ItemPlacementHelpers.make_keyblade_slot_logic_lambda(LocationId.SleepingLion)
        self.logic[START_NODE][NodeId.BondOfFlameSlot] = ItemPlacementHelpers.make_keyblade_slot_logic_lambda(LocationId.BondOfFlame)
        self.logic[START_NODE][NodeId.TwoBecomeOneSlot] = ItemPlacementHelpers.make_keyblade_slot_logic_lambda(LocationId.TwoBecomeOne)
        self.logic[START_NODE][NodeId.FatalCrestSlot] = ItemPlacementHelpers.make_keyblade_slot_logic_lambda(LocationId.FatalCrest)
        self.logic[START_NODE][NodeId.FenrirSlot] = ItemPlacementHelpers.make_keyblade_slot_logic_lambda(LocationId.Fenrir)
        self.logic[START_NODE][NodeId.UltimaWeaponSlot] = ItemPlacementHelpers.make_keyblade_slot_logic_lambda(LocationId.UltimaWeapon)
        self.logic[START_NODE][NodeId.WinnersProofSlot] = ItemPlacementHelpers.make_keyblade_slot_logic_lambda(LocationId.WinnersProof)
        self.logic[START_NODE][NodeId.PurebloodSlot] = ItemPlacementHelpers.make_keyblade_slot_logic_lambda(LocationId.Pureblood)

def make_graph(graph: LocationGraphBuilder):
    slot_logic = WeaponSlotLogicGraph()
    graph.add_logic(slot_logic)

    kingdomkeyd = graph.add_location(NodeId.KingdomKeyDSlot, [
        weapon_slot(LocationId.KingdomKeyD, CheckLocation.KingdomKeyD),
    ])
    alphaweapon = graph.add_location(NodeId.AlphaWeaponSlot, [
        weapon_slot(LocationId.AlphaWeapon, CheckLocation.AlphaWeapon),
    ])
    omegaweapon = graph.add_location(NodeId.OmegaWeaponSlot, [
        weapon_slot(LocationId.OmegaWeapon, CheckLocation.OmegaWeapon),
    ])
    kingdomkey = graph.add_location(NodeId.KingdomKeySlot, [
        weapon_slot(LocationId.KingdomKey, CheckLocation.KingdomKey),
    ])
    oathkeeper = graph.add_location(NodeId.OathkeeperSlot, [
        weapon_slot(LocationId.Oathkeeper, CheckLocation.Oathkeeper),
    ])
    oblivion = graph.add_location(NodeId.OblivionSlot, [
        weapon_slot(LocationId.Oblivion, CheckLocation.Oblivion),
    ])
    starseeker = graph.add_location(NodeId.StarSeekerSlot, [
        weapon_slot(LocationId.StarSeeker, CheckLocation.StarSeeker),
    ])
    hiddendragon = graph.add_location(NodeId.HiddenDragonSlot, [
        weapon_slot(LocationId.HiddenDragon, CheckLocation.HiddenDragon),
    ])
    heroscrest = graph.add_location(NodeId.HerosCrestSlot, [
        weapon_slot(LocationId.HerosCrest, CheckLocation.HerosCrest),
    ])
    monochrome = graph.add_location(NodeId.MonochromeSlot, [
        weapon_slot(LocationId.Monochrome, CheckLocation.Monochrome),
    ])
    followthewind = graph.add_location(NodeId.FollowTheWindSlot, [
        weapon_slot(LocationId.FollowTheWind, CheckLocation.FollowTheWind),
    ])
    circleoflife = graph.add_location(NodeId.CircleOfLifeSlot, [
        weapon_slot(LocationId.CircleOfLife, CheckLocation.CircleOfLife),
    ])
    photondebugger = graph.add_location(NodeId.PhotonDebuggerSlot, [
        weapon_slot(LocationId.PhotonDebugger, CheckLocation.PhotonDebugger),
    ])
    gullwing = graph.add_location(NodeId.GullWingSlot, [
        weapon_slot(LocationId.GullWing, CheckLocation.GullWing),
    ])
    rumblingrose = graph.add_location(NodeId.RumblingRoseSlot, [
        weapon_slot(LocationId.RumblingRose, CheckLocation.RumblingRose),
    ])
    guardiansoul = graph.add_location(NodeId.GuardianSoulSlot, [
        weapon_slot(LocationId.GuardianSoul, CheckLocation.GuardianSoul),
    ])
    wishinglamp = graph.add_location(NodeId.WishingLampSlot, [
        weapon_slot(LocationId.WishingLamp, CheckLocation.WishingLamp),
    ])
    decisivepumpkin = graph.add_location(NodeId.DecisivePumpkinSlot, [
        weapon_slot(LocationId.DecisivePumpkin, CheckLocation.DecisivePumpkin),
    ])
    sweetmemories = graph.add_location(NodeId.SweetMemoriesSlot, [
        weapon_slot(LocationId.SweetMemories, CheckLocation.SweetMemories),
    ])
    mysteriousabyss = graph.add_location(NodeId.MysteriousAbyssSlot, [
        weapon_slot(LocationId.MysteriousAbyss, CheckLocation.MysteriousAbyss),
    ])
    sleepinglion = graph.add_location(NodeId.SleepingLionSlot, [
        weapon_slot(LocationId.SleepingLion, CheckLocation.SleepingLion),
    ])
    bondofflame = graph.add_location(NodeId.BondOfFlameSlot, [
        weapon_slot(LocationId.BondOfFlame, CheckLocation.BondOfFlame),
    ])
    twobecomeone = graph.add_location(NodeId.TwoBecomeOneSlot, [
        weapon_slot(LocationId.TwoBecomeOne, CheckLocation.TwoBecomeOne),
    ])
    fatalcrest = graph.add_location(NodeId.FatalCrestSlot, [
        weapon_slot(LocationId.FatalCrest, CheckLocation.FatalCrest),
    ])
    fenrir = graph.add_location(NodeId.FenrirSlot, [
        weapon_slot(LocationId.Fenrir, CheckLocation.Fenrir),
    ])
    ultimaweapon = graph.add_location(NodeId.UltimaWeaponSlot, [
        weapon_slot(LocationId.UltimaWeapon, CheckLocation.UltimaWeapon),
    ])
    winnersproof = graph.add_location(NodeId.WinnersProofSlot, [
        weapon_slot(LocationId.WinnersProof, CheckLocation.WinnersProof),
    ])
    pureblood = graph.add_location(NodeId.PurebloodSlot, [
        weapon_slot(LocationId.Pureblood, CheckLocation.Pureblood),
    ])
    strugglesword = graph.add_location(NodeId.StruggleSwordSlot, [
        weapon_slot(LocationId.StruggleSword, CheckLocation.StruggleSword),
    ])
    strugglewand = graph.add_location(NodeId.StruggleWandSlot, [
        weapon_slot(LocationId.StruggleWand, CheckLocation.StruggleWand),
    ])
    strugglehammer = graph.add_location(NodeId.StruggleHammerSlot, [
        weapon_slot(LocationId.StruggleHammer, CheckLocation.StruggleHammer),
    ])

    
    graph.add_edge(START_NODE, kingdomkeyd)
    graph.add_edge(START_NODE, alphaweapon)
    graph.add_edge(START_NODE, omegaweapon)
    graph.add_edge(START_NODE, kingdomkey)
    graph.add_edge(START_NODE, oathkeeper)
    graph.add_edge(START_NODE, oblivion)
    graph.add_edge(START_NODE, starseeker)
    graph.add_edge(START_NODE, hiddendragon)
    graph.add_edge(START_NODE, heroscrest)
    graph.add_edge(START_NODE, monochrome)
    graph.add_edge(START_NODE, followthewind)
    graph.add_edge(START_NODE, circleoflife)
    graph.add_edge(START_NODE, photondebugger)
    graph.add_edge(START_NODE, gullwing)
    graph.add_edge(START_NODE, rumblingrose)
    graph.add_edge(START_NODE, guardiansoul)
    graph.add_edge(START_NODE, wishinglamp)
    graph.add_edge(START_NODE, decisivepumpkin)
    graph.add_edge(START_NODE, sweetmemories)
    graph.add_edge(START_NODE, mysteriousabyss)
    graph.add_edge(START_NODE, sleepinglion)
    graph.add_edge(START_NODE, bondofflame)
    graph.add_edge(START_NODE, twobecomeone)
    graph.add_edge(START_NODE, fatalcrest)
    graph.add_edge(START_NODE, fenrir)
    graph.add_edge(START_NODE, ultimaweapon)
    graph.add_edge(START_NODE, winnersproof)
    graph.add_edge(START_NODE, pureblood)
    graph.add_edge(START_NODE, strugglesword)
    graph.add_edge(START_NODE, strugglewand)
    graph.add_edge(START_NODE, strugglehammer)



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

def armor_accessory_slots() -> list[KH2Location]:
    return [
        weapon_slot(LocationId.AbilityRing, CheckLocation.AbilityRing),
        weapon_slot(LocationId.EngineersRing, CheckLocation.EngineersRing),
        weapon_slot(LocationId.TechniciansRing, CheckLocation.TechniciansRing),
        weapon_slot(LocationId.ExpertsRing, CheckLocation.ExpertsRing),
        weapon_slot(LocationId.SardonyxRing, CheckLocation.SardonyxRing),
        weapon_slot(LocationId.TourmalineRing, CheckLocation.TourmalineRing),
        weapon_slot(LocationId.AquamarineRing, CheckLocation.AquamarineRing),
        weapon_slot(LocationId.GarnetRing, CheckLocation.GarnetRing),
        weapon_slot(LocationId.DiamondRing, CheckLocation.DiamondRing),
        weapon_slot(LocationId.SilverRing, CheckLocation.SilverRing),
        weapon_slot(LocationId.GoldRing, CheckLocation.GoldRing),
        weapon_slot(LocationId.PlatinumRing, CheckLocation.PlatinumRing),
        weapon_slot(LocationId.MythrilRing, CheckLocation.MythrilRing),
        weapon_slot(LocationId.OrichalcumRing, CheckLocation.OrichalcumRing),
        weapon_slot(LocationId.MastersRing, CheckLocation.MastersRing),
        weapon_slot(LocationId.MoonAmulet, CheckLocation.MoonAmulet),
        weapon_slot(LocationId.StarCharm, CheckLocation.StarCharm),
        weapon_slot(LocationId.SkillRing, CheckLocation.SkillRing),
        weapon_slot(LocationId.SkillfulRing, CheckLocation.SkillfulRing),
        weapon_slot(LocationId.SoldierEarring, CheckLocation.SoldierEarring),
        weapon_slot(LocationId.FencerEarring, CheckLocation.FencerEarring),
        weapon_slot(LocationId.MageEarring, CheckLocation.MageEarring),
        weapon_slot(LocationId.SlayerEarring, CheckLocation.SlayerEarring),
        weapon_slot(LocationId.CosmicRing, CheckLocation.CosmicRing),
        weapon_slot(LocationId.Medal, CheckLocation.Medal),
        weapon_slot(LocationId.CosmicArts, CheckLocation.CosmicArts),
        weapon_slot(LocationId.ShadowArchive, CheckLocation.ShadowArchive),
        weapon_slot(LocationId.ShadowArchivePlus, CheckLocation.ShadowArchivePlus),
        weapon_slot(LocationId.LuckyRing, CheckLocation.LuckyRing),
        weapon_slot(LocationId.FullBloom, CheckLocation.FullBloom),
        weapon_slot(LocationId.DrawRing, CheckLocation.DrawRing),
        weapon_slot(LocationId.FullBloomPlus, CheckLocation.FullBloomPlus),
        weapon_slot(LocationId.ExecutivesRing, CheckLocation.ExecutivesRing),
        weapon_slot(LocationId.ElvenBandanna, CheckLocation.ElvenBandanna),
        weapon_slot(LocationId.DivineBandanna, CheckLocation.DivineBandanna),
        weapon_slot(LocationId.PowerBand, CheckLocation.PowerBand),
        weapon_slot(LocationId.BusterBand, CheckLocation.BusterBand),
        weapon_slot(LocationId.ProtectBelt, CheckLocation.ProtectBelt),
        weapon_slot(LocationId.GaiaBelt, CheckLocation.GaiaBelt),
        weapon_slot(LocationId.CosmicBelt, CheckLocation.CosmicBelt),
        weapon_slot(LocationId.ShockCharm, CheckLocation.ShockCharm),
        weapon_slot(LocationId.ShockCharmPlus, CheckLocation.ShockCharmPlus),
        weapon_slot(LocationId.GrandRibbon, CheckLocation.GrandRibbon),
        weapon_slot(LocationId.FireBangle, CheckLocation.FireBangle),
        weapon_slot(LocationId.FiraBangle, CheckLocation.FiraBangle),
        weapon_slot(LocationId.FiragaBangle, CheckLocation.FiragaBangle),
        weapon_slot(LocationId.FiragunBangle, CheckLocation.FiragunBangle),
        weapon_slot(LocationId.BlizzardArmlet, CheckLocation.BlizzardArmlet),
        weapon_slot(LocationId.BlizzaraArmlet, CheckLocation.BlizzaraArmlet),
        weapon_slot(LocationId.BlizzagaArmlet, CheckLocation.BlizzagaArmlet),
        weapon_slot(LocationId.BlizzagunArmlet, CheckLocation.BlizzagunArmlet),
        weapon_slot(LocationId.ThunderTrinket, CheckLocation.ThunderTrinket),
        weapon_slot(LocationId.ThundaraTrinket, CheckLocation.ThundaraTrinket),
        weapon_slot(LocationId.ThundagaTrinket, CheckLocation.ThundagaTrinket),
        weapon_slot(LocationId.ThundagunTrinket, CheckLocation.ThundagunTrinket),
        weapon_slot(LocationId.ShadowAnklet, CheckLocation.ShadowAnklet),
        weapon_slot(LocationId.DarkAnklet, CheckLocation.DarkAnklet),
        weapon_slot(LocationId.MidnightAnklet, CheckLocation.MidnightAnklet),
        weapon_slot(LocationId.ChaosAnklet, CheckLocation.ChaosAnklet),
        weapon_slot(LocationId.AbasChain, CheckLocation.AbasChain),
        weapon_slot(LocationId.AegisChain, CheckLocation.AegisChain),
        weapon_slot(LocationId.Acrisius, CheckLocation.Acrisius),
        weapon_slot(LocationId.Ribbon, CheckLocation.Ribbon),
        weapon_slot(LocationId.ChampionBelt, CheckLocation.ChampionBelt),
        weapon_slot(LocationId.PetiteRibbon, CheckLocation.PetiteRibbon),
        weapon_slot(LocationId.AcrisiusPlus, CheckLocation.AcrisiusPlus),
        weapon_slot(LocationId.CosmicChain, CheckLocation.CosmicChain),
    ]