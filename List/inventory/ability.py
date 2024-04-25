from dataclasses import dataclass, field

from List.configDict import itemType
from List.inventory.item import InventoryItem


@dataclass(frozen=True)
class Ability(InventoryItem):
    id: int
    name: str
    type: itemType
    sort_index: int


@dataclass(frozen=True)
class DonaldAbility(InventoryItem):
    id: int
    name: str
    type: itemType = field(init=False, default=itemType.DONALD_ABILITY)


@dataclass(frozen=True)
class GoofyAbility(InventoryItem):
    id: int
    name: str
    type: itemType = field(init=False, default=itemType.GOOFY_ABILITY)


Scan = Ability(138, "Scan", itemType.SUPPORT_ABILITY, sort_index=100)
AerialRecovery = Ability(158, "Aerial Recovery", itemType.SUPPORT_ABILITY, sort_index=101)
ComboPlus = Ability(162, "Combo Plus", itemType.SUPPORT_ABILITY, sort_index=103)
AirComboPlus = Ability(163, "Air Combo Plus", itemType.SUPPORT_ABILITY, sort_index=104)
ComboBoost = Ability(390, "Combo Boost", itemType.SUPPORT_ABILITY, sort_index=105)
AirComboBoost = Ability(391, "Air Combo Boost", itemType.SUPPORT_ABILITY, sort_index=106)
ReactionBoost = Ability(392, "Reaction Boost", itemType.SUPPORT_ABILITY, sort_index=107)
FinishingPlus = Ability(393, "Finishing Plus", itemType.SUPPORT_ABILITY, sort_index=108)
NegativeCombo = Ability(394, "Negative Combo", itemType.SUPPORT_ABILITY, sort_index=109)
BerserkCharge = Ability(395, "Berserk Charge", itemType.SUPPORT_ABILITY, sort_index=111)
DamageDrive = Ability(396, "Damage Drive", itemType.SUPPORT_ABILITY, sort_index=112)
DriveBoost = Ability(397, "Drive Boost", itemType.SUPPORT_ABILITY, sort_index=113)
FormBoost = Ability(398, "Form Boost", itemType.SUPPORT_ABILITY, sort_index=114)
SummonBoost = Ability(399, "Summon Boost", itemType.SUPPORT_ABILITY, sort_index=115)
CombinationBoost = Ability(400, "Combination Boost", itemType.SUPPORT_ABILITY, sort_index=116)
ExperienceBoost = Ability(401, "Experience Boost", itemType.SUPPORT_ABILITY, sort_index=117)
LeafBracer = Ability(402, "Leaf Bracer", itemType.SUPPORT_ABILITY, sort_index=118)
MagicLockOn = Ability(403, "Magic Lock-On", itemType.SUPPORT_ABILITY, sort_index=119)
NoExperience = Ability(404, "No Experience", itemType.SUPPORT_ABILITY, sort_index=141)
Draw = Ability(405, "Draw", itemType.SUPPORT_ABILITY, sort_index=121)
Jackpot = Ability(406, "Jackpot", itemType.SUPPORT_ABILITY, sort_index=122)
LuckyLucky = Ability(407, "Lucky Lucky", itemType.SUPPORT_ABILITY, sort_index=123)
FireBoost = Ability(408, "Fire Boost", itemType.SUPPORT_ABILITY, sort_index=125)
BlizzardBoost = Ability(409, "Blizzard Boost", itemType.SUPPORT_ABILITY, sort_index=126)
ThunderBoost = Ability(410, "Thunder Boost", itemType.SUPPORT_ABILITY, sort_index=127)
ItemBoost = Ability(411, "Item Boost", itemType.SUPPORT_ABILITY, sort_index=128)
MpRage = Ability(412, "MP Rage", itemType.SUPPORT_ABILITY, sort_index=129)
MpHaste = Ability(413, "MP Haste", itemType.SUPPORT_ABILITY, sort_index=131)
Defender = Ability(414, "Defender", itemType.SUPPORT_ABILITY, sort_index=134)
SecondChance = Ability(415, "Second Chance", itemType.SUPPORT_ABILITY, sort_index=136)
OnceMore = Ability(416, "Once More", itemType.SUPPORT_ABILITY, sort_index=137)
MpHastera = Ability(421, "MP Hastera", itemType.SUPPORT_ABILITY, sort_index=132)
MpHastega = Ability(422, "MP Hastega", itemType.SUPPORT_ABILITY, sort_index=133)
ComboMaster = Ability(539, "Combo Master", itemType.SUPPORT_ABILITY, sort_index=102)
DriveConverter = Ability(540, "Drive Converter", itemType.SUPPORT_ABILITY, sort_index=124)
LightAndDarkness = Ability(541, "Light & Darkness", itemType.SUPPORT_ABILITY, sort_index=120)
DamageControl = Ability(542, "Damage Control", itemType.SUPPORT_ABILITY, sort_index=135)

Guard = Ability(82, "Guard", itemType.ACTION_ABILITY, sort_index=0)
UpperSlash = Ability(137, "Upper Slash", itemType.ACTION_ABILITY, sort_index=1)
TrinityLimit = Ability(198, "Trinity Limit", itemType.ACTION_ABILITY, sort_index=24)
Slapshot = Ability(262, "Slapshot", itemType.ACTION_ABILITY, sort_index=5)
DodgeSlash = Ability(263, "Dodge Slash", itemType.ACTION_ABILITY, sort_index=6)
SlideDash = Ability(264, "Slide Dash", itemType.ACTION_ABILITY, sort_index=8)
GuardBreak = Ability(265, "Guard Break", itemType.ACTION_ABILITY, sort_index=10)
Explosion = Ability(266, "Explosion", itemType.ACTION_ABILITY, sort_index=11)
FinishingLeap = Ability(267, "Finishing Leap", itemType.ACTION_ABILITY, sort_index=3)
Counterguard = Ability(268, "Counterguard", itemType.ACTION_ABILITY, sort_index=17)
AerialSweep = Ability(269, "Aerial Sweep", itemType.ACTION_ABILITY, sort_index=12)
AerialSpiral = Ability(270, "Aerial Spiral", itemType.ACTION_ABILITY, sort_index=14)
HorizontalSlash = Ability(271, "Horizontal Slash", itemType.ACTION_ABILITY, sort_index=2)
AerialFinish = Ability(272, "Aerial Finish", itemType.ACTION_ABILITY, sort_index=15)
RetaliatingSlash = Ability(273, "Retaliating Slash", itemType.ACTION_ABILITY, sort_index=4)
AutoValor = Ability(385, "Auto Valor", itemType.ACTION_ABILITY, sort_index=18)
AutoWisdom = Ability(386, "Auto Wisdom", itemType.ACTION_ABILITY, sort_index=19)
AutoMaster = Ability(387, "Auto Master", itemType.ACTION_ABILITY, sort_index=21)
AutoFinal = Ability(388, "Auto Final", itemType.ACTION_ABILITY, sort_index=22)
AutoSummon = Ability(389, "Auto Summon", itemType.ACTION_ABILITY, sort_index=23)
FlashStep = Ability(559, "Flash Step", itemType.ACTION_ABILITY, sort_index=7)
AerialDive = Ability(560, "Aerial Dive", itemType.ACTION_ABILITY, sort_index=13)
MagnetBurst = Ability(561, "Magnet Burst", itemType.ACTION_ABILITY, sort_index=16)
VicinityBreak = Ability(562, "Vicinity Break", itemType.ACTION_ABILITY, sort_index=9)
AutoLimitForm = Ability(568, "Auto Limit", itemType.ACTION_ABILITY, sort_index=20)


class DonaldAbilities:
    # These are in a separate namespace because some share IDs with common and/or Goofy abilities
    DonaldFire = DonaldAbility(165, "Donald Fire")
    DonaldBlizzard = DonaldAbility(166, "Donald Blizzard")
    DonaldThunder = DonaldAbility(167, "Donald Thunder")
    DonaldCure = DonaldAbility(168, "Donald Cure")
    Fantasia = DonaldAbility(199, "Fantasia (Comet)")
    FlareForce = DonaldAbility(200, "Flare Force (Duckflare)")
    Draw = DonaldAbility(405, "Draw")
    Jackpot = DonaldAbility(406, "Jackpot")
    LuckyLucky = DonaldAbility(407, "Lucky Lucky")
    FireBoost = DonaldAbility(408, "Fire Boost")
    BlizzardBoost = DonaldAbility(409, "Blizzard Boost")
    ThunderBoost = DonaldAbility(410, "Thunder Boost")
    ItemBoost = DonaldAbility(411, "Item Boost")
    MpRage = DonaldAbility(412, "MP Rage")
    MpHaste = DonaldAbility(413, "MP Haste")
    AutoLimitParty = DonaldAbility(417, "Auto Limit")
    HyperHealing = DonaldAbility(419, "Hyper Healing")
    AutoHealing = DonaldAbility(420, "Auto Healing")
    MpHastera = DonaldAbility(421, "MP Hastera")
    MpHastega = DonaldAbility(422, "MP Hastega")
    DamageControl = DonaldAbility(542, "Damage Control")


class GoofyAbilities:
    # These are in a separate namespace because some share IDs with common and/or Donald abilities
    TornadoFusion = GoofyAbility(201, "Tornado Fusion (Whirligoof)")
    Teamwork = GoofyAbility(202, "Teamwork (Knocksmash)")
    Draw = GoofyAbility(405, "Draw")
    Jackpot = GoofyAbility(406, "Jackpot")
    LuckyLucky = GoofyAbility(407, "Lucky Lucky")
    ItemBoost = GoofyAbility(411, "Item Boost")
    MpRage = GoofyAbility(412, "MP Rage")
    MpHaste = GoofyAbility(413, "MP Haste")
    Defender = GoofyAbility(414, "Defender")
    SecondChance = GoofyAbility(415, "Second Chance")
    OnceMore = GoofyAbility(416, "Once More")
    AutoLimitParty = GoofyAbility(417, "Auto Limit")
    AutoChange = GoofyAbility(418, "Auto Change")
    HyperHealing = GoofyAbility(419, "Hyper Healing")
    AutoHealing = GoofyAbility(420, "Auto Healing")
    MpHastera = GoofyAbility(421, "MP Hastera")
    MpHastega = GoofyAbility(422, "MP Hastega")
    GoofyTornado = GoofyAbility(423, "Goofy Tornado")
    GoofyTurbo = GoofyAbility(425, "Goofy Turbo")
    GoofyBash = GoofyAbility(429, "Goofy Bash")
    DamageControl = GoofyAbility(542, "Damage Control")
    Protect = GoofyAbility(596, "Protect")
    Protera = GoofyAbility(597, "Protera")
    Protega = GoofyAbility(598, "Protega")
