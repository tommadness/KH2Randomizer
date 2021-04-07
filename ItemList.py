from itemClass import KH2Item
from configDict import itemType

itemList = [
    KH2Item(593, "Proof of Connection", itemType.PROOF_OF_CONNECTION),
    KH2Item(594, "Proof of Nonexistence", itemType.PROOF),
    KH2Item(595, "Proof of Peace", itemType.PROOF_OF_PEACE),

    KH2Item(21, "Fire Element", itemType.FIRE),
    KH2Item(21, "Fire Element", itemType.FIRE),
    KH2Item(21, "Fire Element", itemType.FIRE),

    KH2Item(22, "Blizzard Element", itemType.BLIZZARD),
    KH2Item(22, "Blizzard Element", itemType.BLIZZARD),
    KH2Item(22, "Blizzard Element", itemType.BLIZZARD),

    KH2Item(23, "Thunder Element", itemType.THUNDER),
    KH2Item(23, "Thunder Element", itemType.THUNDER),
    KH2Item(23, "Thunder Element", itemType.THUNDER),

    KH2Item(24, "Cure Element", itemType.CURE),
    KH2Item(24, "Cure Element", itemType.CURE),
    KH2Item(24, "Cure Element", itemType.CURE),

    KH2Item(87, "Magnet Element", itemType.MAGNET),
    KH2Item(87, "Magnet Element", itemType.MAGNET),
    KH2Item(87, "Magnet Element", itemType.MAGNET),

    KH2Item(88, "Reflect Element", itemType.REFLECT),
    KH2Item(88, "Reflect Element", itemType.REFLECT),
    KH2Item(88, "Reflect Element", itemType.REFLECT),

    KH2Item(94, "High Jump",itemType.GROWTH_ABILITY),
    KH2Item(95, "High Jump",itemType.GROWTH_ABILITY),
    KH2Item(96, "High Jump",itemType.GROWTH_ABILITY),
    KH2Item(97, "High Jump",itemType.GROWTH_ABILITY),

    KH2Item(98, "Quick Run",itemType.GROWTH_ABILITY),
    KH2Item(99, "Quick Run",itemType.GROWTH_ABILITY),
    KH2Item(100, "Quick Run",itemType.GROWTH_ABILITY),
    KH2Item(101, "Quick Run",itemType.GROWTH_ABILITY),

    KH2Item(102, "Aerial Dodge",itemType.GROWTH_ABILITY),
    KH2Item(103, "Aerial Dodge",itemType.GROWTH_ABILITY),
    KH2Item(104, "Aerial Dodge",itemType.GROWTH_ABILITY),
    KH2Item(105, "Aerial Dodge",itemType.GROWTH_ABILITY),

    KH2Item(106, "Glide",itemType.GROWTH_ABILITY),
    KH2Item(107, "Glide",itemType.GROWTH_ABILITY),
    KH2Item(108, "Glide",itemType.GROWTH_ABILITY),
    KH2Item(109, "Glide",itemType.GROWTH_ABILITY),

    KH2Item(564, "Dodge Roll",itemType.GROWTH_ABILITY),
    KH2Item(565, "Dodge Roll",itemType.GROWTH_ABILITY),
    KH2Item(567, "Dodge Roll",itemType.GROWTH_ABILITY),
    KH2Item(568, "Dodge Roll",itemType.GROWTH_ABILITY),

    KH2Item(32, "Torn Pages",itemType.TORN_PAGE),
    KH2Item(32, "Torn Pages",itemType.TORN_PAGE),
    KH2Item(32, "Torn Pages",itemType.TORN_PAGE),
    KH2Item(32, "Torn Pages",itemType.TORN_PAGE),
    KH2Item(32, "Torn Pages",itemType.TORN_PAGE),

    KH2Item(159, "Lamp Charm (Genie)",itemType.SUMMON),
    KH2Item(160, "Feather Charm (Peter Pan)", itemType.SUMMON),
    KH2Item(25, "Ukulele Charm (Stitch)", itemType.SUMMON),
    KH2Item(383, "Baseball Charm (Chicken Little)", itemType.SUMMON),

    KH2Item(226, "Secret Ansem's Report 1", itemType.REPORT),
    KH2Item(227, "Secret Ansem's Report 2", itemType.REPORT),
    KH2Item(228, "Secret Ansem's Report 3", itemType.REPORT),
    KH2Item(229, "Secret Ansem's Report 4", itemType.REPORT),
    KH2Item(230, "Secret Ansem's Report 5", itemType.REPORT),
    KH2Item(231, "Secret Ansem's Report 6", itemType.REPORT),
    KH2Item(232, "Secret Ansem's Report 7", itemType.REPORT),
    KH2Item(233, "Secret Ansem's Report 8", itemType.REPORT),
    KH2Item(234, "Secret Ansem's Report 9", itemType.REPORT),
    KH2Item(235, "Secret Ansem's Report 10", itemType.REPORT),
    KH2Item(236, "Secret Ansem's Report 11", itemType.REPORT),
    KH2Item(237, "Secret Ansem's Report 12", itemType.REPORT),
    KH2Item(238, "Secret Ansem's Report 13", itemType.REPORT),

    KH2Item(42,"Oathkeeper", itemType.KEYBLADE),
    KH2Item(43,"Oblivion",itemType.KEYBLADE),
    KH2Item(484,"Hero's Crest",itemType.KEYBLADE),
    KH2Item(485,"Monochrome",itemType.KEYBLADE),
    KH2Item(486,"Follow the Wind",itemType.KEYBLADE),
    KH2Item(487,"Circle of Life",itemType.KEYBLADE),
    KH2Item(488,"Photon Debugger",itemType.KEYBLADE),
    KH2Item(489,"Gull Wing",itemType.KEYBLADE),
    KH2Item(490,"Rumbling Rose",itemType.KEYBLADE),
    KH2Item(491,"Guardian Soul",itemType.KEYBLADE),
    KH2Item(492,"Wishing Lamp",itemType.KEYBLADE),
    KH2Item(493,"Decisive Pumpkin",itemType.KEYBLADE),
    KH2Item(494,"Sleeping Lion",itemType.KEYBLADE),
    KH2Item(495,"Sweet Memories",itemType.KEYBLADE),
    KH2Item(496,"Mysterious Abyss",itemType.KEYBLADE),
    KH2Item(497,"Fatal Crest",itemType.KEYBLADE),
    KH2Item(498,"Bond of Flame",itemType.KEYBLADE),
    KH2Item(499,"Fenrir",itemType.KEYBLADE),
    KH2Item(500,"Ultima Weapon",itemType.KEYBLADE),

    KH2Item(546, "Centurion+", itemType.STAFF), #StatEntry = 151
    KH2Item(151, "Comet Staff", itemType.STAFF), #StatEntry = 90
    KH2Item(148, "Hammer Staff", itemType.STAFF), #StatEntry = 87
    KH2Item(152, "Lord's Broom", itemType.STAFF), #StatEntry = 91
    KH2Item(75, "Mage's Staff", itemType.STAFF), #StatEntry = 86
    KH2Item(150, "Meteor Staff", itemType.STAFF), #StatEntry = 89
    KH2Item(155, "Nobody Lance", itemType.STAFF), #StatEntry = 94
    KH2Item(549, "Precious Mushroom", itemType.STAFF), #StatEntry = 154
    KH2Item(550, "Precious Mushroom+", itemType.STAFF), #StatEntry = 155
    KH2Item(551, "Premium Mushroom", itemType.STAFF), #StatEntry = 156
    KH2Item(154, "Rising Dragon", itemType.STAFF), #StatEntry = 93
    KH2Item(503, "Save The Queen+", itemType.STAFF), #StatEntry = 146
    KH2Item(156, "Shaman's Relic", itemType.STAFF), #StatEntry = 95
    KH2Item(149, "Victory Bell", itemType.STAFF), #StatEntry = 88
    KH2Item(153, "Wisdom Wand", itemType.STAFF), #StatEntry = 92

    KH2Item(139, "Adamant Shield", itemType.SHIELD), #StatEntry = 100
    KH2Item(146, "Akashic Record", itemType.SHIELD), #StatEntry = 107
    KH2Item(140, "Chain Shield", itemType.SHIELD), #StatEntry = 101
    KH2Item(143, "Dream Cloud", itemType.SHIELD), #StatEntry = 104
    KH2Item(142, "Falling Star", itemType.SHIELD), #StatEntry = 103
    KH2Item(553, "Frozen Pride+", itemType.SHIELD), #StatEntry = 158
    KH2Item(145, "Akashic Record", itemType.SHIELD), #StatEntry = 106
    KH2Item(144, "Knight Defender", itemType.SHIELD), #StatEntry = 105
    KH2Item(49, "Knight's Shield", itemType.SHIELD), #StatEntry = 99
    KH2Item(556, "Majestic Mushroom", itemType.SHIELD), #StatEntry = 161
    KH2Item(557, "Majestic Mushroom+", itemType.SHIELD), #StatEntry = 162
    KH2Item(147, "Nobody Guard", itemType.SHIELD), #StatEntry = 108
    KH2Item(141, "Ogre Shield", itemType.SHIELD), #StatEntry = 102
    KH2Item(504, "Save The King+", itemType.SHIELD), #StatEntry = 147
    KH2Item(558, "Ultimate Mushroom", itemType.SHIELD), #StatEntry = 163

    KH2Item(535,"Munny Pouch",itemType.MUNNY_POUCH),
    KH2Item(362, "Munny Pouch",itemType.MUNNY_POUCH),

    KH2Item(1, "Potion",itemType.ITEM),
    KH2Item(2, "Hi-Potion",itemType.ITEM),
    KH2Item(3, "Ether", itemType.ITEM),
    KH2Item(4, "Elixir", itemType.ITEM),
    KH2Item(5,"Mega-Potion",itemType.ITEM),
    KH2Item(6,"Mega-Ether",itemType.ITEM),
    KH2Item(7,"Megalixir",itemType.ITEM),



]

supportAbilityList = [
    KH2Item(138,"Scan",itemType.SUPPORT_ABILITY),
    KH2Item(138,"Scan",itemType.SUPPORT_ABILITY),
    KH2Item(158,"Aerial Recovery",itemType.SUPPORT_ABILITY),
    KH2Item(539,"Combo Master",itemType.SUPPORT_ABILITY),
    KH2Item(162,"Combo Plus",itemType.SUPPORT_ABILITY),
    KH2Item(162,"Combo Plus",itemType.SUPPORT_ABILITY),
    KH2Item(162,"Combo Plus",itemType.SUPPORT_ABILITY),
    KH2Item(163,"Air Combo Plus",itemType.SUPPORT_ABILITY),
    KH2Item(163,"Air Combo Plus",itemType.SUPPORT_ABILITY),
    KH2Item(163,"Air Combo Plus",itemType.SUPPORT_ABILITY),
    KH2Item(390,"Combo Boost",itemType.SUPPORT_ABILITY),
    KH2Item(390,"Combo Boost",itemType.SUPPORT_ABILITY),
    KH2Item(391,"Air Combo Boost",itemType.SUPPORT_ABILITY),
    KH2Item(391,"Air Combo Boost",itemType.SUPPORT_ABILITY),
    KH2Item(392,"Reaction Boost",itemType.SUPPORT_ABILITY),
    KH2Item(392,"Reaction Boost",itemType.SUPPORT_ABILITY),
    KH2Item(392,"Reaction Boost",itemType.SUPPORT_ABILITY),
    KH2Item(393,"Finishing Plus",itemType.SUPPORT_ABILITY),
    KH2Item(393,"Finishing Plus",itemType.SUPPORT_ABILITY),
    KH2Item(393,"Finishing Plus",itemType.SUPPORT_ABILITY),
    KH2Item(394,"Negative Combo",itemType.SUPPORT_ABILITY),
    KH2Item(394,"Negative Combo",itemType.SUPPORT_ABILITY),
    KH2Item(395,"Berserk Charge",itemType.SUPPORT_ABILITY),
    KH2Item(395,"Berserk Charge",itemType.SUPPORT_ABILITY),
    KH2Item(396,"Damage Drive",itemType.SUPPORT_ABILITY),
    KH2Item(397,"Drive Boost",itemType.SUPPORT_ABILITY),
    KH2Item(397,"Drive Boost",itemType.SUPPORT_ABILITY),
    KH2Item(398,"Form Boost",itemType.SUPPORT_ABILITY),
    KH2Item(398,"Form Boost",itemType.SUPPORT_ABILITY),
    KH2Item(398,"Form Boost",itemType.SUPPORT_ABILITY),
    KH2Item(399,"Summon Boost",itemType.SUPPORT_ABILITY),
    KH2Item(400,"Combination Boost",itemType.SUPPORT_ABILITY),
    KH2Item(401,"Experience Boost",itemType.SUPPORT_ABILITY),
    KH2Item(401,"Experience Boost",itemType.SUPPORT_ABILITY),
    KH2Item(402,"Leaf Bracer",itemType.SUPPORT_ABILITY),
    KH2Item(403,"Magic Lock-On",itemType.SUPPORT_ABILITY),
    KH2Item(405,"Draw",itemType.SUPPORT_ABILITY),
    KH2Item(405,"Draw",itemType.SUPPORT_ABILITY),
    KH2Item(405,"Draw",itemType.SUPPORT_ABILITY),
    KH2Item(405,"Draw",itemType.SUPPORT_ABILITY),
    KH2Item(406,"Jackpot",itemType.SUPPORT_ABILITY),
    KH2Item(406,"Jackpot",itemType.SUPPORT_ABILITY),
    KH2Item(407,"Lucky Lucky",itemType.SUPPORT_ABILITY),
    KH2Item(407,"Lucky Lucky",itemType.SUPPORT_ABILITY),
    KH2Item(407,"Lucky Lucky",itemType.SUPPORT_ABILITY),
    KH2Item(540,"Drive Converter",itemType.SUPPORT_ABILITY),
    KH2Item(540,"Drive Converter",itemType.SUPPORT_ABILITY),
    KH2Item(408,"Fire Boost",itemType.SUPPORT_ABILITY),
    KH2Item(408,"Fire Boost",itemType.SUPPORT_ABILITY),
    KH2Item(409,"Blizzard Boost",itemType.SUPPORT_ABILITY),
    KH2Item(409,"Blizzard Boost",itemType.SUPPORT_ABILITY),
    KH2Item(410,"Thunder Boost",itemType.SUPPORT_ABILITY),
    KH2Item(410,"Thunder Boost",itemType.SUPPORT_ABILITY),
    KH2Item(411,"Item Boost",itemType.SUPPORT_ABILITY),
    KH2Item(411,"Item Boost",itemType.SUPPORT_ABILITY),
    KH2Item(412,"MP Rage",itemType.SUPPORT_ABILITY),
    KH2Item(412,"MP Rage",itemType.SUPPORT_ABILITY),
    KH2Item(413,"MP Haste",itemType.SUPPORT_ABILITY),
    KH2Item(413,"MP Haste",itemType.SUPPORT_ABILITY),
    KH2Item(421,"MP Hastera",itemType.SUPPORT_ABILITY),
    KH2Item(421,"MP Hastera",itemType.SUPPORT_ABILITY),
    KH2Item(422,"MP Hastega",itemType.SUPPORT_ABILITY),
    KH2Item(414,"Defender",itemType.SUPPORT_ABILITY),
    KH2Item(414,"Defender",itemType.SUPPORT_ABILITY),
    KH2Item(542,"Damage Control",itemType.SUPPORT_ABILITY),
    KH2Item(542,"Damage Control",itemType.SUPPORT_ABILITY),
    KH2Item(415,"Second Chance",itemType.SUPPORT_ABILITY),
    KH2Item(416,"Once More",itemType.SUPPORT_ABILITY),
    KH2Item(404,"No Experience",itemType.SUPPORT_ABILITY),
    KH2Item(404,"No Experience",itemType.SUPPORT_ABILITY),
    KH2Item(541,"Light & Darkness",itemType.SUPPORT_ABILITY),


]

actionAbilityList = [
    KH2Item(82, "Guard", itemType.ACTION_ABILITY),
    KH2Item(137, "Upper Slash", itemType.ACTION_ABILITY),
    KH2Item(271, "Horizontal Slash", itemType.ACTION_ABILITY),
    KH2Item(267, "Finishing Leap", itemType.ACTION_ABILITY),
    KH2Item(273, "Relatliating Slash", itemType.ACTION_ABILITY),
    KH2Item(262, "Slapshot", itemType.ACTION_ABILITY),
    KH2Item(263, "Dodge Slash", itemType.ACTION_ABILITY),
    KH2Item(559, "Flash Step", itemType.ACTION_ABILITY),
    KH2Item(264, "Slide Dash", itemType.ACTION_ABILITY),
    KH2Item(562, "Vicinity Break", itemType.ACTION_ABILITY),
    KH2Item(265, "Guard Break", itemType.ACTION_ABILITY),
    KH2Item(266, "Explosion", itemType.ACTION_ABILITY),
    KH2Item(269, "Aerial Sweep", itemType.ACTION_ABILITY),
    KH2Item(560, "Aerial Dive", itemType.ACTION_ABILITY),
    KH2Item(270, "Aerial Spiral", itemType.ACTION_ABILITY),
    KH2Item(272, "Aerial Finish", itemType.ACTION_ABILITY),
    KH2Item(561, "Magnet Burst", itemType.ACTION_ABILITY),
    KH2Item(268, "Counterguard", itemType.ACTION_ABILITY),
    KH2Item(385, "Auto Valor", itemType.ACTION_ABILITY),
    KH2Item(386, "Auto Wisdom", itemType.ACTION_ABILITY),
    KH2Item(387, "Auto Master", itemType.ACTION_ABILITY),
    KH2Item(388, "Auto Final", itemType.ACTION_ABILITY),
    KH2Item(389, "Auto Summon", itemType.ACTION_ABILITY),
    KH2Item(568, "Auto Limit", itemType.ACTION_ABILITY),
    KH2Item(198, "Trinity Limit", itemType.ACTION_ABILITY),

]

junkList = [
    KH2Item(576, "Remembrance Shard", itemType.JUNK),
    KH2Item(577, "Remembrance Stone", itemType.JUNK),
    KH2Item(578, "Remembrance Gem", itemType.JUNK),
    KH2Item(584, "Lost Illusion", itemType.JUNK),
    KH2Item(585, "Manifest Illusion", itemType.JUNK),
    KH2Item(345, "Mythril Shard", itemType.JUNK),
    KH2Item(346, "Mythril Stone", itemType.JUNK),
    KH2Item(347, "Mythril Gem", itemType.JUNK),
    KH2Item(348, "Mythril Crystal", itemType.JUNK),
    KH2Item(349, "Bright Shard", itemType.JUNK),
]

donaldAbilityList = [
    KH2Item(165, "Donald Fire", itemType.DONALD_ABILITY),
    KH2Item(166, "Donald Blizzard", itemType.DONALD_ABILITY),
    KH2Item(167, "Donald Thunder", itemType.DONALD_ABILITY),
    KH2Item(168, "Donald Cure", itemType.DONALD_ABILITY),
    KH2Item(199, "Fantasia", itemType.DONALD_ABILITY),
    KH2Item(200, "Flare Force", itemType.DONALD_ABILITY),
    KH2Item(405, "Draw", itemType.DONALD_ABILITY),
    KH2Item(406, "Jackpot", itemType.DONALD_ABILITY),
    KH2Item(407, "Lucky Lucky", itemType.DONALD_ABILITY),
    KH2Item(408, "Fire Boost", itemType.DONALD_ABILITY),
    KH2Item(409, "Blizzard Boost", itemType.DONALD_ABILITY),
    KH2Item(410, "Thunder Boost", itemType.DONALD_ABILITY),
    KH2Item(408, "Fire Boost", itemType.DONALD_ABILITY),
    KH2Item(409, "Blizzard Boost", itemType.DONALD_ABILITY),
    KH2Item(410, "Thunder Boost", itemType.DONALD_ABILITY),
    KH2Item(412, "MP Rage", itemType.DONALD_ABILITY),
    KH2Item(421, "MP Hastera", itemType.DONALD_ABILITY),
    KH2Item(417, "Auto Limit", itemType.DONALD_ABILITY),
    KH2Item(419, "Hyper Healing", itemType.DONALD_ABILITY),
    KH2Item(420, "Auto Healing", itemType.DONALD_ABILITY),
    KH2Item(414, "Defender", itemType.DONALD_ABILITY),
    KH2Item(411, "Item Boost", itemType.DONALD_ABILITY),
    KH2Item(542, "Damage Control", itemType.DONALD_ABILITY),
    KH2Item(419, "Hyper Healing", itemType.DONALD_ABILITY),
    KH2Item(412, "MP Rage", itemType.DONALD_ABILITY),
    KH2Item(413, "MP Haste", itemType.DONALD_ABILITY),
    KH2Item(421, "MP Hastera", itemType.DONALD_ABILITY),
    KH2Item(422, "MP Hastega", itemType.DONALD_ABILITY),
]

goofyAbilityList = [
    KH2Item(423, "Goofy Tornado", itemType.GOOFY_ABILITY),
    KH2Item(425, "Goofy Turbo", itemType.GOOFY_ABILITY),
    KH2Item(429, "Goofy Bash", itemType.GOOFY_ABILITY),
    KH2Item(201, "Tornado Fusion", itemType.GOOFY_ABILITY),
    KH2Item(202, "Teamwork", itemType.GOOFY_ABILITY),
    KH2Item(405, "Draw", itemType.GOOFY_ABILITY),
    KH2Item(406, "Jackpot", itemType.GOOFY_ABILITY),
    KH2Item(407, "Lucky Lucky", itemType.GOOFY_ABILITY),
    KH2Item(411, "Item Boost", itemType.GOOFY_ABILITY),
    KH2Item(412, "MP Rage", itemType.GOOFY_ABILITY),
    KH2Item(414, "Defender", itemType.GOOFY_ABILITY),
    KH2Item(542, "Damage Control", itemType.GOOFY_ABILITY),
    KH2Item(417, "Auto Limit", itemType.GOOFY_ABILITY),
    KH2Item(415,"Second Chance",itemType.GOOFY_ABILITY),
    KH2Item(416,"Once More",itemType.GOOFY_ABILITY),
    KH2Item(418, "Auto Change", itemType.GOOFY_ABILITY),
    KH2Item(419, "Hyper Healing", itemType.GOOFY_ABILITY),
    KH2Item(420, "Auto Healing", itemType.GOOFY_ABILITY),
    KH2Item(414, "Defender", itemType.GOOFY_ABILITY),
    KH2Item(419, "Hyper Healing", itemType.GOOFY_ABILITY),
    KH2Item(413, "MP Haste", itemType.GOOFY_ABILITY),
    KH2Item(421, "MP Hastera", itemType.GOOFY_ABILITY),
    KH2Item(412, "MP Rage", itemType.GOOFY_ABILITY),
    KH2Item(422, "MP Hastega", itemType.GOOFY_ABILITY),
    KH2Item(411, "Item Boost", itemType.GOOFY_ABILITY),
    KH2Item(542, "Damage Control", itemType.GOOFY_ABILITY),
    KH2Item(596, "Protect", itemType.GOOFY_ABILITY),
    KH2Item(597, "Protera", itemType.GOOFY_ABILITY),
    KH2Item(598, "Protega", itemType.GOOFY_ABILITY),
]
