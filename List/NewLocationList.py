from Class.newLocationClass import *
from Class.itemClass import *
from List.configDict import itemType, locationType, locationCategory

class Locations:
    """A set of methods to get all the location information for Sora, Donald, and Goofy. Limited logic about item placement here"""
    @staticmethod
    def getAllSoraLocations():
        return Locations.LoD() + Locations.AG() + Locations.DC() + Locations.HundredAcre() + \
                Locations.OC() + Locations.BC() + Locations.SP() + Locations.HT() + Locations.PR() + \
                Locations.HB() + Locations.CoR() + Locations.PL() + Locations.STT() + Locations.TT() + Locations.TWTNW() + \
                Locations.GoA() + Locations.Atl() + Locations.Levels() + Locations.FormLevels() + \
                Locations.StartingItems() + Locations.Puzzles() + Locations.WeaponList()


    @staticmethod
    def getAllDonaldLocations():
        return Locations.DonaldBonusList()+Locations.DonaldWeaponList()+Locations.DonaldStartingItems()


    @staticmethod
    def getAllGoofyLocations():
        return Locations.GoofyBonusList()+Locations.GoofyWeaponList()+Locations.GoofyStartingItems()


    @staticmethod
    def LoD():
        return [KH2Location(245, "Bamboo Grove Dark Shard", locationCategory.CHEST,[locationType.LoD]),
                KH2Location(497, "Bamboo Grove Ether", locationCategory.CHEST,[locationType.LoD]),
                KH2Location(498, "Bamboo Grove Mythril Shard", locationCategory.CHEST,[locationType.LoD]),
                KH2Location(350, "Bamboo Grove Encampment Area Map", locationCategory.POPUP,[locationType.LoD]),
                KH2Location(417, "Missions", locationCategory.POPUP,[locationType.LoD]),
                KH2Location(21, "Checkpoint Hi-Potion", locationCategory.CHEST,[locationType.LoD]),
                KH2Location(121, "Checkpoint Mythril Shard", locationCategory.CHEST,[locationType.LoD]),
                KH2Location(22, "Mountain Trail Lightning Shard", locationCategory.CHEST,[locationType.LoD]),
                KH2Location(23, "Mountain Trail Recovery Recipe", locationCategory.CHEST,[locationType.LoD]),
                KH2Location(122, "Mountain Trail Ether", locationCategory.CHEST,[locationType.LoD]),
                KH2Location(123, "Mountain Trail Mythril Shard", locationCategory.CHEST,[locationType.LoD]),
                KH2Location(495, "Village Cave Area Map", locationCategory.POPUP,[locationType.LoD]),
                KH2Location(124, "Village Cave AP Boost", locationCategory.CHEST,[locationType.LoD]),
                KH2Location(125, "Village Cave Dark Shard", locationCategory.CHEST,[locationType.LoD]),
                KH2Location(43, "Village Cave Bonus", locationCategory.ITEMBONUS,[locationType.LoD]),
                KH2Location(24, "Ridge Frost Shard", locationCategory.CHEST,[locationType.LoD]),
                KH2Location(126, "Ridge AP Boost", locationCategory.CHEST,[locationType.LoD]),
                KH2Location(9, "Shan-Yu", locationCategory.HYBRIDBONUS,[locationType.LoD]),
                KH2Location(257, "Hidden Dragon", locationCategory.POPUP,[locationType.LoD]),
                KH2Location(25, "Throne Room Torn Pages", locationCategory.CHEST,[locationType.LoD]),
                KH2Location(127, "Throne Room Palace Map", locationCategory.CHEST,[locationType.LoD]),
                KH2Location(26, "Throne Room AP Boost", locationCategory.CHEST,[locationType.LoD]),
                KH2Location(27, "Throne Room Queen Recipe", locationCategory.CHEST,[locationType.LoD]),
                KH2Location(128, "Throne Room AP Boost (2)", locationCategory.CHEST,[locationType.LoD]),
                KH2Location(129, "Throne Room Ogre Shield", locationCategory.CHEST,[locationType.LoD]),
                KH2Location(130, "Throne Room Mythril Crystal", locationCategory.CHEST,[locationType.LoD]),
                KH2Location(131, "Throne Room Orichalcum", locationCategory.CHEST,[locationType.LoD]),
                KH2Location(10, "Storm Rider", locationCategory.ITEMBONUS,[locationType.LoD]),
                KH2Location(555, "Xigbar (Data) Defense Boost", locationCategory.POPUP,[locationType.LoD, locationType.DataOrg]),
                ]

    @staticmethod
    def AG():
        return [KH2Location(353, "Agrabah Map", locationCategory.POPUP,[locationType.Agrabah]),
                KH2Location(28, "Agrabah Dark Shard", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(29, "Agrabah Mythril Shard", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(30, "Agrabah Hi-Potion", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(132, "Agrabah AP Boost", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(133, "Agrabah Mythril Stone", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(249, "Agrabah Mythril Shard (2)", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(501, "Agrabah Serenity Shard", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(31, "Bazaar Mythril Gem", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(32, "Bazaar Power Shard", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(33, "Bazaar Hi-Potion", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(134, "Bazaar AP Boost", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(135, "Bazaar Mythril Shard", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(136, "Palace Walls Skill Ring", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(520, "Palace Walls Mythril Stone", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(250, "Cave Entrance Power Stone", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(251, "Cave Entrance Mythril Shard", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(35, "Valley of Stone Mythril Stone", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(36, "Valley of Stone AP Boost", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(137, "Valley of Stone Mythril Shard", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(138, "Valley of Stone Hi-Potion", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(42, "Abu Escort", locationCategory.ITEMBONUS,[locationType.Agrabah]),
                KH2Location(487, "Chasm of Challenges Cave of Wonders Map", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(37, "Chasm of Challenges AP Boost", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(46, "Treasure Room", locationCategory.STATBONUS,[locationType.Agrabah]),
                KH2Location(502, "Treasure Room AP Boost", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(503, "Treasure Room Serenity Gem", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(37, "Elemental Lords", locationCategory.ITEMBONUS,[locationType.Agrabah]),
                KH2Location(300, "Lamp Charm", locationCategory.POPUP,[locationType.Agrabah]),
                KH2Location(34, "Ruined Chamber Torn Pages", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(486, "Ruined Chamber Ruins Map", locationCategory.CHEST,[locationType.Agrabah]),
                KH2Location(15, "Genie Jafar", locationCategory.ITEMBONUS,[locationType.Agrabah]),
                KH2Location(303, "Wishing Lamp", locationCategory.POPUP,[locationType.Agrabah]),
                KH2Location(65, "Lexaeus Bonus", locationCategory.STATBONUS,[locationType.Agrabah, locationType.AS]),
                KH2Location(545, "Lexaeus (AS) Strength Beyond Strength", locationCategory.POPUP,[locationType.Agrabah, locationType.AS]),
                KH2Location(550, "Lexaeus (Data) Lost Illusion", locationCategory.POPUP,[locationType.Agrabah, locationType.DataOrg]),
                ]

    @staticmethod
    def DC():
        return [KH2Location(16, "DC Courtyard Mythril Shard", locationCategory.CHEST,[locationType.DC]),
                KH2Location(17, "DC Courtyard Star Recipe", locationCategory.CHEST,[locationType.DC]),
                KH2Location(18, "DC Courtyard AP Boost", locationCategory.CHEST,[locationType.DC]),
                KH2Location(92, "DC Courtyard Mythril Stone", locationCategory.CHEST,[locationType.DC]),
                KH2Location(93, "DC Courtyard Blazing Stone", locationCategory.CHEST,[locationType.DC]),
                KH2Location(247, "DC Courtyard Blazing Shard", locationCategory.CHEST,[locationType.DC]),
                KH2Location(248, "DC Courtyard Mythril Shard (2)", locationCategory.CHEST,[locationType.DC]),
                KH2Location(91, "Library Torn Pages", locationCategory.CHEST,[locationType.DC]),
                KH2Location(332, "Disney Castle Map", locationCategory.POPUP,[locationType.DC]),
                KH2Location(38, "Minnie Escort", locationCategory.HYBRIDBONUS,[locationType.DC]),
                KH2Location(79, "Cornerstone Hill Map", locationCategory.CHEST,[locationType.DC]),
                KH2Location(12, "Cornerstone Hill Frost Shard", locationCategory.CHEST,[locationType.DC]),
                KH2Location(81, "Pier Mythril Shard", locationCategory.CHEST,[locationType.DC]),
                KH2Location(82, "Pier Hi-Potion", locationCategory.CHEST,[locationType.DC]),
                KH2Location(83, "Waterway Mythril Stone", locationCategory.CHEST,[locationType.DC]),
                KH2Location(84, "Waterway AP Boost", locationCategory.CHEST,[locationType.DC]),
                KH2Location(85, "Waterway Frost Stone", locationCategory.CHEST,[locationType.DC]),
                KH2Location(368, "Window of Time Map", locationCategory.POPUP,[locationType.DC]),
                KH2Location(16, "Boat Pete", locationCategory.ITEMBONUS,[locationType.DC]),
                KH2Location(17, "Future Pete", locationCategory.HYBRIDBONUS,[locationType.DC]),
                KH2Location(261, "Monochrome", locationCategory.POPUP,[locationType.DC]),
                KH2Location(262, "Wisdom Form", locationCategory.POPUP,[locationType.DC]),
                KH2Location(67, "Marluxia Bonus", locationCategory.STATBONUS,[locationType.DC, locationType.AS]),
                KH2Location(548, "Marluxia (AS) Eternal Blossom", locationCategory.POPUP,[locationType.DC, locationType.AS]),
                KH2Location(553, "Marluxia (Data) Lost Illusion", locationCategory.POPUP,[locationType.DC, locationType.DataOrg]),
                KH2Location(70, "Lingering Will Bonus", locationCategory.STATBONUS,[locationType.HT, locationType.LW], InvalidChecks=[itemType.PROOF_OF_CONNECTION]),
                KH2Location(587, "Lingering Will Proof of Connection", locationCategory.POPUP,[locationType.DC, locationType.LW], InvalidChecks=[itemType.PROOF_OF_CONNECTION]),
                KH2Location(591, "Lingering Will Manifest Illusion", locationCategory.POPUP,[locationType.DC, locationType.LW], InvalidChecks=[itemType.PROOF_OF_CONNECTION]),
                ]

    @staticmethod
    def HundredAcre():
        return [KH2Location(313, "Pooh's House 100 Acre Wood Map", locationCategory.CHEST,[locationType.HUNDREDAW]),
                KH2Location(97, "Pooh's House AP Boost", locationCategory.CHEST,[locationType.HUNDREDAW]),
                KH2Location(98, "Pooh's House Mythril Stone", locationCategory.CHEST,[locationType.HUNDREDAW]),
                KH2Location(105, "Piglet's House Defense Boost", locationCategory.CHEST,[locationType.HUNDREDAW]),
                KH2Location(103, "Piglet's House AP Boost", locationCategory.CHEST,[locationType.HUNDREDAW]),
                KH2Location(104, "Piglet's House Mythril Gem", locationCategory.CHEST,[locationType.HUNDREDAW]),
                KH2Location(314, "Rabbit's House Draw Ring", locationCategory.CHEST,[locationType.HUNDREDAW]),
                KH2Location(100, "Rabbit's House Mythril Crystal", locationCategory.CHEST,[locationType.HUNDREDAW]),
                KH2Location(101, "Rabbit's House AP Boost", locationCategory.CHEST,[locationType.HUNDREDAW]),
                KH2Location(108, "Kanga's House Magic Boost", locationCategory.CHEST,[locationType.HUNDREDAW]),
                KH2Location(106, "Kanga's House AP Boost", locationCategory.CHEST,[locationType.HUNDREDAW]),
                KH2Location(107, "Kanga's House Orichalcum", locationCategory.CHEST,[locationType.HUNDREDAW]),
                KH2Location(110, "Spooky Cave Mythril Gem", locationCategory.CHEST,[locationType.HUNDREDAW]),
                KH2Location(111, "Spooky Cave AP Boost", locationCategory.CHEST,[locationType.HUNDREDAW]),
                KH2Location(112, "Spooky Cave Orichalcum", locationCategory.CHEST,[locationType.HUNDREDAW]),
                KH2Location(113, "Spooky Cave Guard Recipe", locationCategory.CHEST,[locationType.HUNDREDAW]),
                KH2Location(115, "Spooky Cave Mythril Crystal", locationCategory.CHEST,[locationType.HUNDREDAW]),
                KH2Location(116, "Spooky Cave AP Boost (2)", locationCategory.CHEST,[locationType.HUNDREDAW]),
                KH2Location(284, "Sweet Memories", locationCategory.POPUP,[locationType.HUNDREDAW]),
                KH2Location(485, "Spooky Cave Map", locationCategory.POPUP,[locationType.HUNDREDAW]),
                KH2Location(312, "Starry Hill Cosmic Ring", locationCategory.CHEST,[locationType.HUNDREDAW]),
                KH2Location(94, "Starry Hill Style Recipe", locationCategory.CHEST,[locationType.HUNDREDAW]),
                KH2Location(285, "Starry Hill Cure Element", locationCategory.POPUP,[locationType.HUNDREDAW]),
                KH2Location(539, "Starry Hill Orichalcum+", locationCategory.POPUP,[locationType.HUNDREDAW]),
                ]

    @staticmethod
    def OC():
        return [KH2Location(7,"Passage Mythril Shard", locationCategory.CHEST,[locationType.OC]),
                KH2Location(8,"Passage Mythril Stone", locationCategory.CHEST,[locationType.OC]),
                KH2Location(144, "Passage Ether", locationCategory.CHEST,[locationType.OC]),
                KH2Location(145, "Passage AP Boost", locationCategory.CHEST,[locationType.OC]),
                KH2Location(146, "Passage Hi-Potion", locationCategory.CHEST,[locationType.OC]),
                KH2Location(2,"Inner Chamber Underworld Map", locationCategory.CHEST,[locationType.OC]),
                KH2Location(243, "Inner Chamber Mythril Shard", locationCategory.CHEST,[locationType.OC]),
                KH2Location(5, "Cerberus", locationCategory.ITEMBONUS,[locationType.OC]),
                KH2Location(338, "Coliseum Map", locationCategory.POPUP,[locationType.OC]),
                KH2Location(57, "Urns", locationCategory.ITEMBONUS,[locationType.OC]),
                KH2Location(242, "Underworld Entrance Power Boost", locationCategory.CHEST,[locationType.OC]),
                KH2Location(3,"Caverns Entrance Lucid Shard", locationCategory.CHEST,[locationType.OC]),
                KH2Location(11, "Caverns Entrance AP Boost", locationCategory.CHEST,[locationType.OC]),
                KH2Location(504, "Caverns Entrance Mythril Shard", locationCategory.CHEST,[locationType.OC]),
                KH2Location(9,"The Lost Road Bright Shard", locationCategory.CHEST,[locationType.OC]),
                KH2Location(10, "The Lost Road Ether", locationCategory.CHEST,[locationType.OC]),
                KH2Location(148, "The Lost Road Mythril Shard", locationCategory.CHEST,[locationType.OC]),
                KH2Location(149, "The Lost Road Mythril Stone", locationCategory.CHEST,[locationType.OC]),
                KH2Location(150, "Atrium Lucid Stone", locationCategory.CHEST,[locationType.OC]),
                KH2Location(151, "Atrium AP Boost", locationCategory.CHEST,[locationType.OC]),
                KH2Location(58, "Demyx OC", locationCategory.STATBONUS,[locationType.OC]),
                KH2Location(529, "Secret Ansem Report 5", locationCategory.POPUP,[locationType.OC]),
                KH2Location(293, "Olympus Stone", locationCategory.POPUP,[locationType.OC]),
                KH2Location(244, "The Lock Caverns Map", locationCategory.CHEST,[locationType.OC]),
                KH2Location(5,"The Lock Mythril Shard", locationCategory.CHEST,[locationType.OC]),
                KH2Location(142, "The Lock AP Boost", locationCategory.CHEST,[locationType.OC]),
                KH2Location(6, "Pete (OC)", locationCategory.ITEMBONUS,[locationType.OC]),
                KH2Location(7, "Hydra", locationCategory.HYBRIDBONUS,[locationType.OC]),
                KH2Location(260, "Hero´s Crest", locationCategory.POPUP,[locationType.OC]),
                KH2Location(295, "Auron´s Statue", locationCategory.POPUP,[locationType.OC]),
                KH2Location(8, "Hades", locationCategory.HYBRIDBONUS,[locationType.OC]),
                KH2Location(272, "Guardian Soul", locationCategory.POPUP,[locationType.OC]),
                KH2Location(513, "Protect Belt (Pain and Panic Cup)", locationCategory.POPUP,[locationType.OC, locationType.OCCups], InvalidChecks=[itemType.TROPHY]),
                KH2Location(540, "Serenity Gem (Pain and Panic Cup)", locationCategory.POPUP,[locationType.OC, locationType.OCCups], InvalidChecks=[itemType.TROPHY]),
                KH2Location(515, "Rising Dragon (Cerberus Cup)", locationCategory.POPUP,[locationType.OC, locationType.OCCups], InvalidChecks=[itemType.TROPHY]),
                KH2Location(542, "Serenity Crystal (Cerberus Cup)", locationCategory.POPUP,[locationType.OC, locationType.OCCups], InvalidChecks=[itemType.TROPHY]),
                KH2Location(514, "Genji Shield (Titan Cup)", locationCategory.POPUP,[locationType.OC, locationType.OCCups], InvalidChecks=[itemType.TROPHY]),
                KH2Location(541, "Skillful Ring (Titan Cup)", locationCategory.POPUP,[locationType.OC, locationType.OCCups], InvalidChecks=[itemType.TROPHY]),
                KH2Location(516, "Fatal Crest (Goddess of Fate Cup)", locationCategory.POPUP,[locationType.OC, locationType.OCCups], InvalidChecks=[itemType.TROPHY]),
                KH2Location(517, "Orichalcum+ (Goddess of Fate Cup)", locationCategory.POPUP,[locationType.OC, locationType.OCCups], InvalidChecks=[itemType.TROPHY]),
                KH2Location(518, "Hades Cup Trophy (Paradox Cups)", locationCategory.POPUP,[locationType.OC, locationType.OCCups, locationType.OCParadoxCup], InvalidChecks=[itemType.TROPHY, itemType.FORM, itemType.SUMMON]),
                KH2Location(66, "Zexion Bonus", locationCategory.STATBONUS,[locationType.OC, locationType.AS]),
                KH2Location(546, "Zexion (AS) Book of Shadows", locationCategory.POPUP,[locationType.OC, locationType.AS]),
                KH2Location(551, "Zexion (Data) Lost Illusion", locationCategory.POPUP,[locationType.OC, locationType.DataOrg]),
                ]

    @staticmethod
    def BC():
        return [KH2Location(39, "BC Courtyard AP Boost", locationCategory.CHEST,[locationType.BC]),
                KH2Location(40, "BC Courtyard Hi-Potion", locationCategory.CHEST,[locationType.BC]),
                KH2Location(505, "BC Courtyard Mythril Shard", locationCategory.CHEST,[locationType.BC]),
                KH2Location(46, "Belle's Room Castle Map", locationCategory.CHEST,[locationType.BC]),
                KH2Location(240, "Belle's Room Mega-Recipe", locationCategory.CHEST,[locationType.BC]),
                KH2Location(63, "The East Wing Mythril Shard", locationCategory.CHEST,[locationType.BC]),
                KH2Location(155, "The East Wing Tent", locationCategory.CHEST,[locationType.BC]),
                KH2Location(41, "The West Hall Hi-Potion", locationCategory.CHEST,[locationType.BC]),
                KH2Location(207, "The West Hall Power Shard", locationCategory.CHEST,[locationType.BC]),
                KH2Location(158, "The West Hall AP Boost", locationCategory.CHEST,[locationType.BC]),
                KH2Location(159, "The West Hall Bright Stone", locationCategory.CHEST,[locationType.BC]),
                KH2Location(206, "The West Hall Mythril Shard", locationCategory.CHEST,[locationType.BC]),
                KH2Location(2, "Thresholder", locationCategory.ITEMBONUS,[locationType.BC]),
                KH2Location(239, "Dungeon Basement Map", locationCategory.CHEST,[locationType.BC]),
                KH2Location(43, "Dungeon AP Boost", locationCategory.CHEST,[locationType.BC]),
                KH2Location(44, "Secret Passage Mythril Shard", locationCategory.CHEST,[locationType.BC]),
                KH2Location(168, "Secret Passage Hi-Potion", locationCategory.CHEST,[locationType.BC]),
                KH2Location(45, "Secret Passage Lucid Shard", locationCategory.CHEST,[locationType.BC]),
                KH2Location(208, "The West Hall Mythril Shard (Post Dungeon)", locationCategory.CHEST,[locationType.BC]),
                KH2Location(42, "The West Wing Mythril Shard", locationCategory.CHEST,[locationType.BC]),
                KH2Location(164, "The West Wing Tent", locationCategory.CHEST,[locationType.BC]),
                KH2Location(12, "Beast", locationCategory.STATBONUS,[locationType.BC]),
                KH2Location(241, "The Beast's Room Blazing Shard", locationCategory.CHEST,[locationType.BC]),
                KH2Location(3, "Dark Thorn Bonus", locationCategory.HYBRIDBONUS,[locationType.BC]),
                KH2Location(299, "Dark Thorn Cure Element", locationCategory.POPUP,[locationType.BC]),
                KH2Location(270, "Rumbling Rose", locationCategory.POPUP,[locationType.BC]),
                KH2Location(325, "Castle Walls Map", locationCategory.POPUP,[locationType.BC]),
                KH2Location(4, "Xaldin Bonus", locationCategory.HYBRIDBONUS,[locationType.BC]),
                KH2Location(528, "Secret Ansem Report 6", locationCategory.POPUP,[locationType.BC]),
                KH2Location(559, "Xaldin (Data) Defense Boost", locationCategory.POPUP,[locationType.BC, locationType.DataOrg]),
                ]

    @staticmethod
    def SP():
        return [KH2Location(316, "Pit Cell Area Map", locationCategory.CHEST,[locationType.SP]),
                KH2Location(64, "Pit Cell Mythril Crystal", locationCategory.CHEST,[locationType.SP]),
                KH2Location(65, "Canyon Dark Crystal", locationCategory.CHEST,[locationType.SP]),
                KH2Location(171, "Canyon Mythril Stone", locationCategory.CHEST,[locationType.SP]),
                KH2Location(253, "Canyon Mythril Gem", locationCategory.CHEST,[locationType.SP]),
                KH2Location(521, "Canyon Frost Crystal", locationCategory.CHEST,[locationType.SP]),
                KH2Location(49, "Hallway Power Crystal", locationCategory.CHEST,[locationType.SP]),
                KH2Location(50, "Hallway AP Boost", locationCategory.CHEST,[locationType.SP]),
                KH2Location(45, "Screens", locationCategory.STATBONUS,[locationType.SP]),
                KH2Location(255, "Communications Room I/O Tower Map", locationCategory.CHEST,[locationType.SP]),
                KH2Location(499, "Communications Room Gaia Belt", locationCategory.CHEST,[locationType.SP]),
                KH2Location(31, "Hostile Program", locationCategory.HYBRIDBONUS,[locationType.SP]),
                KH2Location(267, "Photon Debugger", locationCategory.POPUP,[locationType.SP]),
                KH2Location(61, "Solar Sailer", locationCategory.ITEMBONUS,[locationType.SP]),
                KH2Location(177, "Central Computer Core AP Boost", locationCategory.CHEST,[locationType.SP]),
                KH2Location(178, "Central Computer Core Orichalcum+", locationCategory.CHEST,[locationType.SP]),
                KH2Location(51, "Central Computer Core Cosmic Arts", locationCategory.CHEST,[locationType.SP]),
                KH2Location(488, "Central Computer Core Map", locationCategory.CHEST,[locationType.SP]),
                KH2Location(32, "MCP", locationCategory.HYBRIDBONUS,[locationType.SP]),
                KH2Location(68, "Larxene Bonus", locationCategory.STATBONUS,[locationType.SP, locationType.AS]),
                KH2Location(547, "Larxene (AS) Cloaked Thunder", locationCategory.POPUP,[locationType.SP, locationType.AS]),
                KH2Location(552, "Larxene (Data) Lost Illusion", locationCategory.POPUP,[locationType.SP, locationType.DataOrg]),
                ]

    @staticmethod
    def HT():
        return [KH2Location(53, "Graveyard Mythril Shard", locationCategory.CHEST,[locationType.HT]),
                KH2Location(212, "Graveyard Serenity Gem", locationCategory.CHEST,[locationType.HT]),
                KH2Location(211, "Finklestein's Lab Halloween Town Map", locationCategory.CHEST,[locationType.HT]),
                KH2Location(209, "Town Square Mythril Stone", locationCategory.CHEST,[locationType.HT]),
                KH2Location(210, "Town Square Energy Shard", locationCategory.CHEST,[locationType.HT]),
                KH2Location(54, "Hinterlands Lightning Shard", locationCategory.CHEST,[locationType.HT]),
                KH2Location(213, "Hinterlands Mythril Stone", locationCategory.CHEST,[locationType.HT]),
                KH2Location(214, "Hinterlands AP Boost", locationCategory.CHEST,[locationType.HT]),
                KH2Location(55, "Candy Cane Lane Mega-Potion", locationCategory.CHEST,[locationType.HT]),
                KH2Location(56, "Candy Cane Lane Mythril Gem", locationCategory.CHEST,[locationType.HT]),
                KH2Location(216, "Candy Cane Lane Lightning Stone", locationCategory.CHEST,[locationType.HT]),
                KH2Location(217, "Candy Cane Lane Mythril Stone", locationCategory.CHEST,[locationType.HT]),
                KH2Location(57, "Santa's House Christmas Town Map", locationCategory.CHEST,[locationType.HT]),
                KH2Location(58, "Santa's House AP Boost", locationCategory.CHEST,[locationType.HT]),
                KH2Location(18, "Prison Keeper", locationCategory.HYBRIDBONUS,[locationType.HT]),
                KH2Location(19, "Oogie Boogie", locationCategory.STATBONUS,[locationType.HT]),
                KH2Location(301, "Oogie Boogie Magnet Element", locationCategory.POPUP,[locationType.HT]),
                KH2Location(40, "Lock, Shock, and Barrel", locationCategory.STATBONUS,[locationType.HT]),
                KH2Location(297, "Present", locationCategory.POPUP,[locationType.HT]),
                KH2Location(298, "Decoy Presents", locationCategory.POPUP,[locationType.HT]),
                KH2Location(20, "Experiment", locationCategory.STATBONUS,[locationType.HT]),
                KH2Location(275, "Decisive Pumpkin", locationCategory.POPUP,[locationType.HT]),
                KH2Location(64, "Vexen Bonus", locationCategory.STATBONUS,[locationType.HT, locationType.AS]),
                KH2Location(544, "Vexen (AS) Road to Discovery", locationCategory.POPUP,[locationType.HT, locationType.AS]),
                KH2Location(549, "Vexen (Data) Lost Illusion", locationCategory.POPUP,[locationType.HT, locationType.DataOrg])
                ]

    @staticmethod
    def PR():
        return [KH2Location(70, "Rampart Naval Map", locationCategory.CHEST,[locationType.PR]),
                KH2Location(219, "Rampart Mythril Stone", locationCategory.CHEST,[locationType.PR]),
                KH2Location(220, "Rampart Dark Shard", locationCategory.CHEST,[locationType.PR]),
                KH2Location(71, "Town Dark Stone", locationCategory.CHEST,[locationType.PR]),
                KH2Location(72, "Town AP Boost", locationCategory.CHEST,[locationType.PR]),
                KH2Location(73, "Town Mythril Shard", locationCategory.CHEST,[locationType.PR]),
                KH2Location(221, "Town Mythril Gem", locationCategory.CHEST,[locationType.PR]),
                KH2Location(74, "Cave Mouth Bright Shard", locationCategory.CHEST,[locationType.PR]),
                KH2Location(223, "Cave Mouth Mythril Shard", locationCategory.CHEST,[locationType.PR]),
                KH2Location(329, "Isla de Muerta Map", locationCategory.POPUP,[locationType.PR]),
                KH2Location(62, "Boat Fight", locationCategory.ITEMBONUS,[locationType.PR]),
                KH2Location(39, "Interceptor Barrels", locationCategory.STATBONUS,[locationType.PR]),
                KH2Location(369, "Powder Store AP Boost (1)", locationCategory.CHEST,[locationType.PR]),
                KH2Location(370, "Powder Store AP Boost (2)", locationCategory.CHEST,[locationType.PR]),
                KH2Location(75, "Moonlight Nook Mythril Shard", locationCategory.CHEST,[locationType.PR]),
                KH2Location(224, "Moonlight Nook Serenity Gem", locationCategory.CHEST,[locationType.PR]),
                KH2Location(371, "Moonlight Nook Power Stone", locationCategory.CHEST,[locationType.PR]),
                KH2Location(21, "Barbossa", locationCategory.HYBRIDBONUS,[locationType.PR]),
                KH2Location(263, "Follow the Wind", locationCategory.POPUP,[locationType.PR]),
                KH2Location(59, "Grim Reaper 1", locationCategory.ITEMBONUS,[locationType.PR]),
                KH2Location(252, "Interceptor's Hold Feather Charm", locationCategory.CHEST,[locationType.PR]),
                KH2Location(76, "Seadrift Keep AP Boost", locationCategory.CHEST,[locationType.PR]),
                KH2Location(225, "Seadrift Keep Orichalcum", locationCategory.CHEST,[locationType.PR]),
                KH2Location(372, "Seadrift Keep Meteor Staff", locationCategory.CHEST,[locationType.PR]),
                KH2Location(77, "Seadrift Row Serenity Gem", locationCategory.CHEST,[locationType.PR]),
                KH2Location(78, "Seadrift Row King Recipe", locationCategory.CHEST,[locationType.PR]),
                KH2Location(373, "Seadrift Row Mythril Crystal", locationCategory.CHEST,[locationType.PR]),
                KH2Location(296, "Seadrift Row Cursed Medallion", locationCategory.POPUP,[locationType.PR]),
                KH2Location(331, "Seadrift Row Ship Graveyard Map", locationCategory.POPUP,[locationType.PR]),
                KH2Location(22, "Grim Reaper 2", locationCategory.ITEMBONUS,[locationType.PR]),
                KH2Location(530, "Secret Ansem Report 4", locationCategory.POPUP,[locationType.PR]),
                KH2Location(557, "Luxord (Data) AP Boost", locationCategory.POPUP,[locationType.PR, locationType.DataOrg]),
                ]

    @staticmethod
    def HB():
        return [KH2Location(362, "Marketplace Map", locationCategory.POPUP,[locationType.HB]),
                KH2Location(194, "Borough Drive Recovery", locationCategory.CHEST,[locationType.HB]),
                KH2Location(195, "Borough AP Boost", locationCategory.CHEST,[locationType.HB]),
                KH2Location(196, "Borough Hi-Potion", locationCategory.CHEST,[locationType.HB]),
                KH2Location(305, "Borough Mythril Shard", locationCategory.CHEST,[locationType.HB]),
                KH2Location(506, "Borough Dark Shard", locationCategory.CHEST,[locationType.HB]),
                KH2Location(47, "Bailey", locationCategory.ITEMBONUS,[locationType.HB]),
                KH2Location(256, "Merlin's House Membership Card", locationCategory.POPUP,[locationType.HB]),
                KH2Location(292, "Merlin's House Blizzard Element", locationCategory.POPUP,[locationType.HB]),
                KH2Location(531, "Bailey Secret Ansem Report 7", locationCategory.POPUP,[locationType.HB]),
                KH2Location(258, "Baseball Charm", locationCategory.POPUP,[locationType.HB]),
                KH2Location(310, "Postern Castle Perimeter Map", locationCategory.CHEST,[locationType.HB]),
                KH2Location(189, "Postern Mythril Gem", locationCategory.CHEST,[locationType.HB]),
                KH2Location(190, "Postern AP Boost", locationCategory.CHEST,[locationType.HB]),
                KH2Location(200, "Corridors Mythril Stone", locationCategory.CHEST,[locationType.HB]),
                KH2Location(201, "Corridors Mythril Crystal", locationCategory.CHEST,[locationType.HB]),
                KH2Location(202, "Corridors Dark Crystal", locationCategory.CHEST,[locationType.HB]),
                KH2Location(307, "Corridors AP Boost", locationCategory.CHEST,[locationType.HB]),
                KH2Location(184, "Ansem's Study Skill Recipe", locationCategory.CHEST,[locationType.HB]),
                KH2Location(266, "Ansem's Study Master Form", locationCategory.POPUP,[locationType.HB]),
                KH2Location(276, "Ansem's Study Sleeping Lion", locationCategory.POPUP,[locationType.HB]),
                KH2Location(183, "Ansem's Study Ukulele Charm", locationCategory.CHEST,[locationType.HB]),
                KH2Location(309, "Restoration Site Moon Recipe", locationCategory.CHEST,[locationType.HB]),
                KH2Location(507, "Restoration Site AP Boost", locationCategory.CHEST,[locationType.HB]),
                KH2Location(28, "Demyx (HB)", locationCategory.HYBRIDBONUS,[locationType.HB]),
                KH2Location(361, "FF Fights Cure Element", locationCategory.POPUP,[locationType.HB]),
                KH2Location(179, "Crystal Fissure Torn Pages", locationCategory.CHEST,[locationType.HB]),
                KH2Location(489, "Crystal Fissure The Great Maw Map", locationCategory.CHEST,[locationType.HB]),
                KH2Location(180, "Crystal Fissure Energy Crystal", locationCategory.CHEST,[locationType.HB]),
                KH2Location(181, "Crystal Fissure AP Boost", locationCategory.CHEST,[locationType.HB]),
                KH2Location(60, "1000 Heartless", locationCategory.ITEMBONUS,[locationType.HB]),
                KH2Location(525, "1000 Heartless Secret Ansem Report 1", locationCategory.POPUP,[locationType.HB]),
                KH2Location(269, "1000 Heartless Ice Cream", locationCategory.POPUP,[locationType.HB]),
                KH2Location(511, "1000 Heartless Picture", locationCategory.POPUP,[locationType.HB]),
                KH2Location(491, "Postern Gull Wing", locationCategory.CHEST,[locationType.HB]),
                KH2Location(311, "Heartless Manufactory Cosmic Chain", locationCategory.CHEST,[locationType.HB], InvalidChecks=[itemType.MEMBERSHIPCARD]),
                KH2Location(35, "Sephiroth Bonus", locationCategory.STATBONUS,[locationType.HB, locationType.Sephi]),
                KH2Location(282, "Sephiroth Fenrir", locationCategory.POPUP,[locationType.HB, locationType.Sephi]),
                KH2Location(560, "Demyx (Data) AP Boost", locationCategory.POPUP,[locationType.HB, locationType.DataOrg], InvalidChecks=[itemType.FORM]),
                KH2Location(588, "Winner's Proof", locationCategory.POPUP,[locationType.HB, locationType.Mush13], InvalidChecks=[itemType.PROOF_OF_PEACE]),
                KH2Location(589, "Proof of Peace", locationCategory.POPUP,[locationType.HB, locationType.Mush13], InvalidChecks=[itemType.PROOF_OF_PEACE]),
                ]

    @staticmethod
    def CoR():
        return [#free
                KH2Location(562, "CoR Depths AP Boost", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                KH2Location(563, "CoR Depths Power Crystal", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                KH2Location(564, "CoR Depths Frost Crystal", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                KH2Location(565, "CoR Depths Manifest Illusion", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                KH2Location(566, "CoR Depths AP Boost (2)", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                KH2Location(580, "CoR Mineshaft Lower Level Depths of Remembrance Map", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                KH2Location(578, "CoR Mineshaft Lower Level AP Boost", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                #post fight 1
                KH2Location(567, "CoR Depths Upper Level Remembrance Gem", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                KH2Location(568, "CoR Mining Area Serenity Gem", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                KH2Location(569, "CoR Mining Area AP Boost", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                KH2Location(570, "CoR Mining Area Serenity Crystal", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                KH2Location(571, "CoR Mining Area Manifest Illusion", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                KH2Location(572, "CoR Mining Area Serenity Gem (2)", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                KH2Location(573, "CoR Mining Area Dark Remembrance Map", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                KH2Location(581, "CoR Mineshaft Mid Level Power Boost", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                #post fight 2
                KH2Location(574, "CoR Engine Chamber Serenity Crystal", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                KH2Location(575, "CoR Engine Chamber Remembrance Crystal", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                KH2Location(576, "CoR Engine Chamber AP Boost", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                KH2Location(577, "CoR Engine Chamber Manifest Illusion", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                KH2Location(582, "CoR Mineshaft Upper Level Magic Boost", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                #last chest
                KH2Location(579, "CoR Mineshaft Upper Level AP Boost", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                KH2Location(72, "Transport to Remembrance", locationCategory.STATBONUS,[locationType.HB, locationType.CoR, locationType.TTR]),
                ]

    @staticmethod
    def PL():
        return [KH2Location(492, "Gorge Savannah Map", locationCategory.CHEST,[locationType.PL]),
                KH2Location(404, "Gorge Dark Gem", locationCategory.CHEST,[locationType.PL]),
                KH2Location(405, "Gorge Mythril Stone", locationCategory.CHEST,[locationType.PL]),
                KH2Location(401, "Elephant Graveyard Frost Gem", locationCategory.CHEST,[locationType.PL]),
                KH2Location(402, "Elephant Graveyard Mythril Stone", locationCategory.CHEST,[locationType.PL]),
                KH2Location(403, "Elephant Graveyard Bright Stone", locationCategory.CHEST,[locationType.PL]),
                KH2Location(508, "Elephant Graveyard AP Boost", locationCategory.CHEST,[locationType.PL]),
                KH2Location(509, "Elephant Graveyard Mythril Shard", locationCategory.CHEST,[locationType.PL]),
                KH2Location(418, "Pride Rock Map", locationCategory.CHEST,[locationType.PL]),
                KH2Location(392, "Pride Rock Mythril Stone", locationCategory.CHEST,[locationType.PL]),
                KH2Location(393, "Pride Rock Serenity Crystal", locationCategory.CHEST,[locationType.PL]),
                KH2Location(396, "Wildebeest Valley Energy Stone", locationCategory.CHEST,[locationType.PL]),
                KH2Location(397, "Wildebeest Valley AP Boost", locationCategory.CHEST,[locationType.PL]),
                KH2Location(398, "Wildebeest Valley Mythril Gem", locationCategory.CHEST,[locationType.PL]),
                KH2Location(399, "Wildebeest Valley Mythril Stone", locationCategory.CHEST,[locationType.PL]),
                KH2Location(400, "Wildebeest Valley Lucid Gem", locationCategory.CHEST,[locationType.PL]),
                KH2Location(406, "Wastelands Mythril Shard", locationCategory.CHEST,[locationType.PL]),
                KH2Location(407, "Wastelands Serenity Gem", locationCategory.CHEST,[locationType.PL]),
                KH2Location(408, "Wastelands Mythril Stone", locationCategory.CHEST,[locationType.PL]),
                KH2Location(409, "Jungle Serenity Gem", locationCategory.CHEST,[locationType.PL]),
                KH2Location(410, "Jungle Mythril Stone", locationCategory.CHEST,[locationType.PL]),
                KH2Location(411, "Jungle Serenity Crystal", locationCategory.CHEST,[locationType.PL]),
                KH2Location(412, "Oasis Map", locationCategory.CHEST,[locationType.PL]),
                KH2Location(493, "Oasis Torn Pages", locationCategory.CHEST,[locationType.PL]),
                KH2Location(413, "Oasis AP Boost", locationCategory.CHEST,[locationType.PL]),
                KH2Location(49, "Hyenas 1", locationCategory.STATBONUS,[locationType.PL]),
                KH2Location(264, "Circle of Life", locationCategory.POPUP,[locationType.PL]),
                KH2Location(29, "Scar", locationCategory.STATBONUS,[locationType.PL]),
                KH2Location(302, "Scar Fire Element", locationCategory.POPUP,[locationType.PL]),
                KH2Location(50, "Hyenas 2", locationCategory.STATBONUS,[locationType.PL]),
                KH2Location(30, "Groundshaker", locationCategory.HYBRIDBONUS,[locationType.PL]),
                KH2Location(556, "Saix (Data) Defense Boost", locationCategory.POPUP,[locationType.PL, locationType.DataOrg]),
                ]

    @staticmethod
    def STT():
        return [KH2Location(319, "Twilight Town Map", locationCategory.POPUP,[locationType.STT]),
                KH2Location(288, "Munny Pouch (Olette)", locationCategory.POPUP,[locationType.STT]),
                KH2Location(54, "Station Dusks", locationCategory.ITEMBONUS,[locationType.STT]),
                KH2Location(315, "Station of Serenity Potion", locationCategory.CHEST,[locationType.STT]),
                KH2Location(472, "Station of Calling Potion", locationCategory.CHEST,[locationType.STT]),
                KH2Location(33, "Twilight Thorn", locationCategory.ITEMBONUS,[locationType.STT]),
                KH2Location(73, "Axel 1", locationCategory.ITEMBONUS,[locationType.STT]),
                KH2Location(389, "(Junk) Champion Belt", locationCategory.CHEST,[locationType.STT], InvalidChecks=[e for e in itemType if e not in [itemType.SYNTH,itemType.ITEM] ]),
                KH2Location(390, "(Junk) Medal", locationCategory.CHEST,[locationType.STT], InvalidChecks=[e for e in itemType if e not in [itemType.SYNTH,itemType.ITEM] ]),
                KH2Location(519, "The Struggle Trophy", locationCategory.POPUP,[locationType.STT]),
                KH2Location(428, "Central Station Potion (1)", locationCategory.CHEST,[locationType.STT]),
                KH2Location(429, "STT Central Station Hi-Potion", locationCategory.CHEST,[locationType.STT]),
                KH2Location(430, "Central Station Potion (2)", locationCategory.CHEST,[locationType.STT]),
                KH2Location(434, "Sunset Terrace Ability Ring", locationCategory.CHEST,[locationType.STT]),
                KH2Location(435, "Sunset Terrace Hi-Potion", locationCategory.CHEST,[locationType.STT]),
                KH2Location(436, "Sunset Terrace Potion (1)", locationCategory.CHEST,[locationType.STT]),
                KH2Location(437, "Sunset Terrace Potion (2)", locationCategory.CHEST,[locationType.STT]),
                KH2Location(449, "Mansion Foyer Hi-Potion", locationCategory.CHEST,[locationType.STT]),
                KH2Location(450, "Mansion Foyer Potion (1)", locationCategory.CHEST,[locationType.STT]),
                KH2Location(451, "Mansion Foyer Potion (2)", locationCategory.CHEST,[locationType.STT]),
                KH2Location(455, "Mansion Dining Room Elven Bandanna", locationCategory.CHEST,[locationType.STT]),
                KH2Location(456, "Mansion Dining Room Potion", locationCategory.CHEST,[locationType.STT]),
                KH2Location(289, "Naminé´s Sketches", locationCategory.POPUP,[locationType.STT]),
                KH2Location(483, "Mansion Map", locationCategory.POPUP,[locationType.STT]),
                KH2Location(459, "Mansion Library Hi-Potion", locationCategory.CHEST,[locationType.STT]),
                KH2Location(463, "Mansion Basement Corridor Hi-Potion", locationCategory.CHEST,[locationType.STT]),
                KH2Location(34, "Axel 2", locationCategory.STATBONUS,[locationType.STT]),
                KH2Location(558, "Roxas (Data) Magic Boost", locationCategory.POPUP,[locationType.STT, locationType.DataOrg]),
                ]

    @staticmethod
    def TT():
        return [KH2Location(447, "Old Mansion Potion", locationCategory.CHEST,[locationType.TT]),
                KH2Location(448, "Old Mansion Mythril Shard", locationCategory.CHEST,[locationType.TT]),
                KH2Location(442, "The Woods Potion", locationCategory.CHEST,[locationType.TT]),
                KH2Location(443, "The Woods Mythril Shard", locationCategory.CHEST,[locationType.TT]),
                KH2Location(444, "The Woods Hi-Potion", locationCategory.CHEST,[locationType.TT]),
                KH2Location(420, "Tram Common Hi-Potion", locationCategory.CHEST,[locationType.TT]),
                KH2Location(421, "Tram Common AP Boost", locationCategory.CHEST,[locationType.TT]),
                KH2Location(422, "Tram Common Tent", locationCategory.CHEST,[locationType.TT]),
                KH2Location(423, "Tram Common Mythril Shard (1)", locationCategory.CHEST,[locationType.TT]),
                KH2Location(424, "Tram Common Potion (1)", locationCategory.CHEST,[locationType.TT]),
                KH2Location(425, "Tram Common Mythril Shard (2)", locationCategory.CHEST,[locationType.TT]),
                KH2Location(484, "Tram Common Potion (2)", locationCategory.CHEST,[locationType.TT]),
                KH2Location(526, "Station Plaza Secret Ansem Report 2", locationCategory.POPUP,[locationType.TT]),
                KH2Location(290, "Munny Pouch (Mickey)", locationCategory.POPUP,[locationType.TT]),
                KH2Location(291, "Crystal Orb", locationCategory.POPUP,[locationType.TT]),
                KH2Location(431, "Central Station Tent", locationCategory.CHEST,[locationType.TT]),
                KH2Location(432, "TT Central Station Hi-Potion", locationCategory.CHEST,[locationType.TT]),
                KH2Location(433, "Central Station Mythril Shard", locationCategory.CHEST,[locationType.TT]),
                KH2Location(465, "The Tower Potion", locationCategory.CHEST,[locationType.TT]),
                KH2Location(466, "The Tower Hi-Potion", locationCategory.CHEST,[locationType.TT]),
                KH2Location(522, "The Tower Ether", locationCategory.CHEST,[locationType.TT]),
                KH2Location(467, "Tower Entryway Ether", locationCategory.CHEST,[locationType.TT]),
                KH2Location(468, "Tower Entryway Mythril Shard", locationCategory.CHEST,[locationType.TT]),
                KH2Location(469, "Sorcerer's Loft Tower Map", locationCategory.CHEST,[locationType.TT]),
                KH2Location(470, "Tower Wardrobe Mythril Stone", locationCategory.CHEST,[locationType.TT]),
                KH2Location(304, "Star Seeker", locationCategory.POPUP,[locationType.TT]),
                KH2Location(286, "Valor Form", locationCategory.POPUP,[locationType.TT]),
                KH2Location(294, "Seifer´s Trophy", locationCategory.POPUP,[locationType.TT]),
                KH2Location(265, "Oathkeeper", locationCategory.POPUP,[locationType.TT]),
                KH2Location(543, "Limit Form", locationCategory.POPUP,[locationType.TT]),
                KH2Location(479, "Underground Concourse Mythril Gem", locationCategory.CHEST,[locationType.TT]),
                KH2Location(480, "Underground Concourse Orichalcum", locationCategory.CHEST,[locationType.TT]),
                KH2Location(481, "Underground Concourse AP Boost", locationCategory.CHEST,[locationType.TT]),
                KH2Location(482, "Underground Concourse Mythril Crystal", locationCategory.CHEST,[locationType.TT]),
                KH2Location(477, "Tunnelway Orichalcum", locationCategory.CHEST,[locationType.TT]),
                KH2Location(478, "Tunnelway Mythril Crystal", locationCategory.CHEST,[locationType.TT]),
                KH2Location(438, "Sunset Terrace Orichalcum+", locationCategory.CHEST,[locationType.TT]),
                KH2Location(439, "Sunset Terrace Mythril Shard", locationCategory.CHEST,[locationType.TT]),
                KH2Location(440, "Sunset Terrace Mythril Crystal", locationCategory.CHEST,[locationType.TT]),
                KH2Location(441, "Sunset Terrace AP Boost", locationCategory.CHEST,[locationType.TT]),
                KH2Location(56, "Mansion Nobodies", locationCategory.STATBONUS,[locationType.TT]),
                KH2Location(452, "Mansion Foyer Mythril Crystal", locationCategory.CHEST,[locationType.TT]),
                KH2Location(453, "Mansion Foyer Mythril Stone", locationCategory.CHEST,[locationType.TT]),
                KH2Location(454, "Mansion Foyer Serenity Crystal", locationCategory.CHEST,[locationType.TT]),
                KH2Location(457, "Mansion Dining Room Mythril Crystal", locationCategory.CHEST,[locationType.TT]),
                KH2Location(458, "Mansion Dining Room Mythril Stone", locationCategory.CHEST,[locationType.TT]),
                KH2Location(460, "Mansion Library Orichalcum", locationCategory.CHEST,[locationType.TT]),
                KH2Location(534, "Beam Secret Ansem Report 10", locationCategory.POPUP,[locationType.TT]),
                KH2Location(464, "Mansion Basement Corridor Ultimate Recipe", locationCategory.CHEST,[locationType.TT]),
                KH2Location(63, "Betwixt and Between", locationCategory.ITEMBONUS,[locationType.TT]),
                KH2Location(317, "Betwixt and Between Bond of Flame", locationCategory.POPUP,[locationType.TT]),
                KH2Location(561, "Axel (Data) Magic Boost", locationCategory.POPUP,[locationType.TT, locationType.DataOrg]),
                ]

    @staticmethod
    def TWTNW():
        return [KH2Location(374, "Fragment Crossing Mythril Stone", locationCategory.CHEST,[locationType.TWTNW]),
                KH2Location(375, "Fragment Crossing Mythril Crystal", locationCategory.CHEST,[locationType.TWTNW]),
                KH2Location(376, "Fragment Crossing AP Boost", locationCategory.CHEST,[locationType.TWTNW]),
                KH2Location(377, "Fragment Crossing Orichalcum", locationCategory.CHEST,[locationType.TWTNW]),
                KH2Location(69, "Roxas", locationCategory.HYBRIDBONUS,[locationType.TWTNW]),
                KH2Location(532, "Roxas Secret Ansem Report 8", locationCategory.POPUP,[locationType.TWTNW]),
                KH2Location(277, "Two Become One", locationCategory.POPUP,[locationType.TWTNW]),
                KH2Location(391, "Memory's Skyscaper Mythril Crystal", locationCategory.CHEST,[locationType.TWTNW]),
                KH2Location(523, "Memory's Skyscaper AP Boost", locationCategory.CHEST,[locationType.TWTNW]),
                KH2Location(524, "Memory's Skyscaper Mythril Stone", locationCategory.CHEST,[locationType.TWTNW]),
                KH2Location(335, "The Brink of Despair Dark City Map", locationCategory.CHEST,[locationType.TWTNW]),
                KH2Location(500, "The Brink of Despair Orichalcum+", locationCategory.CHEST,[locationType.TWTNW]),
                KH2Location(378, "Nothing's Call Mythril Gem", locationCategory.CHEST,[locationType.TWTNW]),
                KH2Location(379, "Nothing's Call Orichalcum", locationCategory.CHEST,[locationType.TWTNW]),
                KH2Location(336, "Twilight's View Cosmic Belt", locationCategory.CHEST,[locationType.TWTNW]),
                KH2Location(23, "Xigbar Bonus", locationCategory.STATBONUS,[locationType.TWTNW]),
                KH2Location(527, "Xigbar Secret Ansem Report 3", locationCategory.POPUP,[locationType.TWTNW]),
                KH2Location(380, "Naught's Skyway Mythril Gem", locationCategory.CHEST,[locationType.TWTNW]),
                KH2Location(381, "Naught's Skyway Orichalcum", locationCategory.CHEST,[locationType.TWTNW]),
                KH2Location(382, "Naught's Skyway Mythril Crystal", locationCategory.CHEST,[locationType.TWTNW]),
                KH2Location(278, "Oblivion", locationCategory.POPUP,[locationType.TWTNW]),
                KH2Location(496, "Castle That Never Was Map", locationCategory.POPUP,[locationType.TWTNW]),
                KH2Location(24, "Luxord Bonus", locationCategory.HYBRIDBONUS,[locationType.TWTNW]),
                KH2Location(533, "Luxord Secret Ansem Report 9", locationCategory.POPUP,[locationType.TWTNW]),
                KH2Location(25, "Saix Bonus", locationCategory.STATBONUS,[locationType.TWTNW]),
                KH2Location(536, "Saix Secret Ansem Report 12", locationCategory.POPUP,[locationType.TWTNW]),
                KH2Location(535, "(Pre-Xemnas 1) Secret Ansem Report 11", locationCategory.POPUP,[locationType.TWTNW]),
                KH2Location(385, "Ruin and Creation's Passage Mythril Stone", locationCategory.CHEST,[locationType.TWTNW]),
                KH2Location(386, "Ruin and Creation's Passage AP Boost", locationCategory.CHEST,[locationType.TWTNW]),
                KH2Location(387, "Ruin and Creation's Passage Mythril Crystal", locationCategory.CHEST,[locationType.TWTNW]),
                KH2Location(388, "Ruin and Creation's Passage Orichalcum", locationCategory.CHEST,[locationType.TWTNW]),
                KH2Location(26, "Xemnas 1 Bonus", locationCategory.DOUBLEBONUS, [locationType.TWTNW]),
                KH2Location(537, "Xemnas 1 Secret Ansem Report 13", locationCategory.POPUP,[locationType.TWTNW]),
                KH2Location(71, "Final Xemnas", locationCategory.STATBONUS,[locationType.TWTNW]),
                KH2Location(554, "Xemnas (Data) Power Boost", locationCategory.POPUP,[locationType.TWTNW, locationType.DataOrg]),
                ]

    @staticmethod
    def GoA():
        return [KH2Location(585, "Garden of Assemblage Map", locationCategory.CHEST,[locationType.Free]),
                KH2Location(586, "GoA Lost Illusion", locationCategory.CHEST,[locationType.Free]),
                KH2Location(590, "Proof of Nonexistence", locationCategory.CHEST,[locationType.Free]),
                ]

    @staticmethod
    def Atl():
        return [KH2Location(367, "Undersea Kingdom Map", locationCategory.POPUP,[locationType.Atlantica]),
                KH2Location(287, "Mysterious Abyss", locationCategory.POPUP,[locationType.Atlantica]),
                KH2Location(279, "Musical Blizzard Element", locationCategory.POPUP,[locationType.Atlantica]),
                KH2Location(538, "Musical Orichalcum+", locationCategory.POPUP,[locationType.Atlantica]),
                ]

    @staticmethod
    def Levels():
        return [KH2Location(i, f"Level {i}", locationCategory.LEVEL,[locationType.Level]) for i in range(1,100)]

    @staticmethod
    def FormLevels():
        return [KH2Location(i,f"Valor Level {i}", locationCategory.VALORLEVEL,[locationType.FormLevel] + ([locationType.FormLevel1] if i==1 else [])) for i in range(1,8)] + \
            [KH2Location(i,f"Wisdom Level {i}", locationCategory.WISDOMLEVEL,[locationType.FormLevel] + ([locationType.FormLevel1] if i==1 else [])) for i in range(1,8)] + \
            [KH2Location(i,f"Limit Level {i}", locationCategory.LIMITLEVEL,[locationType.FormLevel] + ([locationType.FormLevel1] if i==1 else [])) for i in range(1,8)] + \
            [KH2Location(i,f"Master Level {i}", locationCategory.MASTERLEVEL,[locationType.FormLevel] + ([locationType.FormLevel1] if i==1 else [])) for i in range(1,8)] + \
            [KH2Location(i,f"Final Level {i}", locationCategory.FINALLEVEL,[locationType.FormLevel] + ([locationType.FormLevel1] if i==1 else [])) for i in range(1,8)] + \
            [KH2Location(i,f"Summon Level {i}", locationCategory.SUMMONLEVEL,[locationType.SummonLevel]) for i in range(1,8)]

    @staticmethod
    def WeaponList():
        return [KH2Location(116,"FAKE (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(83,"Detection Saber (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(84,"Edge of Ultima (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(80,"Kingdom Key (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(81,"Oathkeeper (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(82,"Oblivion (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(123,"Star Seeker (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(124,"Hidden Dragon (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(127,"Hero's Crest (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(128,"Monochrome (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(129,"Follow the Wind (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(130,"Circle of Life (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(131,"Photon Debugger (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(132,"Gull Wing (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(133,"Rumbling Rose (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(134,"Guardian Soul (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(135,"Wishing Lamp (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(136,"Decisive Pumpkin (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(138,"Sweet Memories (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(139,"Mysterious Abyss (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(137,"Sleeping Lion (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(141,"Bond of Flame (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(148,"Two Become One (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(140,"Fatal Crest (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(142,"Fenrir (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(143,"Ultima Weapon (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(149,"Winner's Proof (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                ]

    @staticmethod
    def StartingItems():
        return [KH2Location(i, f"Starting Item {i}", locationCategory.CHEST, [locationType.Critical]) for i in range(1,8)]

    @staticmethod
    def Puzzles():
        return [KH2Location(0, "Awakening (AP Boost)",  locationCategory.POPUP, LocationTypes=[locationType.Puzzle],InvalidChecks=[itemType.REPORT]),
                KH2Location(1, "Heart (Serenity Crystal)", locationCategory.POPUP,  LocationTypes=[locationType.Puzzle],InvalidChecks=[itemType.REPORT]),
                KH2Location(2, "Duality (Rare Document)", locationCategory.POPUP,  LocationTypes=[locationType.Puzzle],InvalidChecks=[itemType.REPORT]),
                KH2Location(3, "Frontier (Manifest Illusion)", locationCategory.POPUP,  LocationTypes=[locationType.Puzzle],InvalidChecks=[itemType.REPORT]),
                KH2Location(4, "Daylight (Executive's Ring)", locationCategory.POPUP,  LocationTypes=[locationType.Puzzle],InvalidChecks=[itemType.TORN_PAGE, itemType.REPORT]),
                KH2Location(5, "Sunset (Grand Ribbon)", locationCategory.POPUP,  LocationTypes=[locationType.Puzzle],InvalidChecks=[itemType.REPORT]),
                ]

    @staticmethod
    def DonaldBonusList():
        return [
            KH2Location(42,"Abu Escort", locationCategory.ITEMBONUS, LocationTypes=[locationType.Agrabah]),
            KH2Location(45,"Screens", locationCategory.ITEMBONUS, LocationTypes=[locationType.SP]),
            KH2Location(28,"Demyx (Hollow Bastion)", locationCategory.ITEMBONUS, LocationTypes=[locationType.HB]),
            KH2Location(58,"Demyx (Olympus)", locationCategory.ITEMBONUS, LocationTypes=[locationType.OC]),
            KH2Location(22,"Grim Reaper 2", locationCategory.ITEMBONUS, LocationTypes=[locationType.PR]),
            KH2Location(16,"Boat Pete", locationCategory.DOUBLEBONUS, LocationTypes=[locationType.DC]),
            KH2Location(18,"Prison Keeper", locationCategory.ITEMBONUS, LocationTypes=[locationType.HT]),
            KH2Location(29,"Scar", locationCategory.ITEMBONUS, LocationTypes=[locationType.PL]),
            KH2Location(61,"Solar Sailor", locationCategory.ITEMBONUS, LocationTypes=[locationType.SP]),
            KH2Location(20,"Experiment", locationCategory.ITEMBONUS, LocationTypes=[locationType.HT]),
            KH2Location(62,"Boat Fight", locationCategory.ITEMBONUS, LocationTypes=[locationType.PR]),
            KH2Location(56,"Mansion", locationCategory.ITEMBONUS, LocationTypes=[locationType.TT]),
            KH2Location(2, "Posessor",locationCategory.ITEMBONUS, LocationTypes=[locationType.BC]),
            KH2Location(4, "Xaldin",locationCategory.ITEMBONUS, LocationTypes=[locationType.BC]),
        ]

    @staticmethod
    def DonaldWeaponList():
        return [KH2Location(151,"Centurion+",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(90,"Comet Staff",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(87,"Hammer Staff",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(91,"Lord's Broom",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(86,"Mage's Staff",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(89,"Meteor Staff",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(94,"Nobody Lance",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(154,"Precious Mushroom",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(155,"Precious Mushroom+",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(156,"Premium Mushroom",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(93,"Rising Dragon",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(146,"Save the Queen+",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(95,"Shaman's Relic",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(88,"Victory Bell",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(92,"Wisdom Wand",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            ]

    @staticmethod
    def DonaldStartingItems():
        return [KH2Location(i, f"Donald Starting Item {i}", locationCategory.CHEST, [locationType.Free]) for i in range(1,3)]


    @staticmethod
    def GoofyBonusList():
        return [KH2Location(21,"Barbossa",locationCategory.DOUBLEBONUS, [locationType.PR]),
                KH2Location(59,"Grim Reaper 1",locationCategory.ITEMBONUS, [locationType.PR]),
                KH2Location(31,"Hostile Program",locationCategory.ITEMBONUS, [locationType.SP]),
                KH2Location(49,"Hyenas 1",locationCategory.ITEMBONUS, [locationType.PL]),
                KH2Location(50,"Hyenas 2",locationCategory.ITEMBONUS, [locationType.PL]),
                KH2Location(40,"Lock/Shock/Barrel",locationCategory.ITEMBONUS, [locationType.HT]),
                KH2Location(19, "Oogie Boogie", locationCategory.ITEMBONUS, [locationType.HT]),
                KH2Location(6,"Pete (Olympus)",locationCategory.ITEMBONUS, [locationType.OC]),
                KH2Location(17,"Pete (Wharf)",locationCategory.ITEMBONUS, [locationType.DC]),
                KH2Location(9,"Shan-Yu",locationCategory.ITEMBONUS, [locationType.LoD]),
                KH2Location(10, "Storm Rider", locationCategory.ITEMBONUS, [locationType.LoD]),
                KH2Location(12,"Beast",locationCategory.ITEMBONUS, [locationType.BC]),
                KH2Location(39,"Interceptor Barrels",locationCategory.ITEMBONUS, [locationType.PR]),
                KH2Location(46,"Treasure Room Heartless",locationCategory.ITEMBONUS, [locationType.Agrabah]),
                KH2Location(66,"Zexion",locationCategory.ITEMBONUS, [locationType.OC, locationType.AS]),
                ]

    @staticmethod
    def GoofyWeaponList():
        return [
            KH2Location(100,"Adamant Shield",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(107,"Akashic Record",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(101,"Chain Gear",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(104,"Dream Cloud",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(103,"Falling Star",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(158,"Frozen Pride+",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(106,"Genji Shield",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(105,"Knight Defender",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(99,"Knight's Shield",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(161,"Majestic Mushroom",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(162,"Majestic Mushroom+",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(108,"Nobody Guard",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(102,"Ogre Shield",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(147,"Save The King+",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(163,"Ultimate Mushroom",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
        ]

    @staticmethod
    def GoofyStartingItems():
        return [KH2Location(i, f"Goofy Starting Item {i}", locationCategory.CHEST, [locationType.Free]) for i in range(1,4)]
