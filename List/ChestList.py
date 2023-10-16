from dataclasses import dataclass

from List.configDict import locationType, itemType


@dataclass(frozen=True)
class KH2Chest:
    # LocationId: int
    ChestIndex: int
    RoomName: str
    SpawnName: str

    def spawn_file_path(self) -> str:
        return f"{self.RoomName}/{self.SpawnName}"


def chests_by_location_id() -> dict[int, KH2Chest]:
    return {
        # Agrabah
        28: KH2Chest(0, "al00", "m_70"),
        29: KH2Chest(1, "al00", "m_70"),
        30: KH2Chest(2, "al00", "m_70"),
        132: KH2Chest(3, "al00", "m_70"),
        133: KH2Chest(4, "al00", "m_70"),
        249: KH2Chest(5, "al00", "m_70"),
        501: KH2Chest(6, "al00", "m_70"),
        # Bazaar
        31: KH2Chest(0, "al01", "m_70"),
        32: KH2Chest(1, "al01", "m_70"),
        33: KH2Chest(2, "al01", "m_70"),
        134: KH2Chest(3, "al01", "m_70"),
        135: KH2Chest(4, "al01", "m_70"),
        # Palace Walls
        136: KH2Chest(0, "al06", "m_70"),
        520: KH2Chest(1, "al06", "m_70"),
        # Cave of Wonders Entrance
        250: KH2Chest(0, "al07", "m_70"),
        251: KH2Chest(1, "al07", "m_70"),
        # Treasure Room
        502: KH2Chest(0, "al10", "m_70"),
        503: KH2Chest(1, "al10", "m_70"),
        # Ruined Chamber
        34: KH2Chest(0, "al11", "m_70"),
        486: KH2Chest(1, "al11", "m_70"),
        # Valley of Stone
        35: KH2Chest(0, "al12", "m_70"),
        36: KH2Chest(1, "al12", "m_70"),
        137: KH2Chest(2, "al12", "m_70"),
        138: KH2Chest(3, "al12", "m_70"),
        # Chasm of Challenges
        37: KH2Chest(0, "al13", "m_70"),
        487: KH2Chest(1, "al13", "m_70"),
        # Belle's Room
        46: KH2Chest(0, "bb02", "m_70"),
        240: KH2Chest(1, "bb02", "m_70"),
        # Beast's Room
        241: KH2Chest(0, "bb03", "m_70"),
        # BC Courtyard
        505: KH2Chest(0, "bb06", "m_70"),
        39: KH2Chest(1, "bb06", "m_70"),
        40: KH2Chest(2, "bb06", "m_70"),
        # East Wing
        63: KH2Chest(0, "bb07", "m_70"),
        155: KH2Chest(1, "bb07", "m_70"),
        # West Hall
        206: KH2Chest(0, "bb08", "m_70"),
        41: KH2Chest(1, "bb08", "m_70"),
        207: KH2Chest(2, "bb08", "m_70"),
        208: KH2Chest(3, "bb08", "m_70"),
        158: KH2Chest(4, "bb08", "m_70"),
        159: KH2Chest(5, "bb08", "m_70"),
        # West Wing
        42: KH2Chest(0, "bb09", "m_70"),
        164: KH2Chest(1, "bb09", "m_70"),
        # Dungeon
        43: KH2Chest(0, "bb10", "m_70"),
        239: KH2Chest(1, "bb10", "m_70"),
        # Secret Passage
        44: KH2Chest(0, "bb12", "m_70"),
        168: KH2Chest(1, "bb12", "m_70"),
        45: KH2Chest(0, "bb12", "m_71"),
        # Ramparts
        70: KH2Chest(0, "ca00", "m_70"),
        219: KH2Chest(1, "ca00", "m_70"),
        220: KH2Chest(2, "ca00", "m_70"),
        # PR Town
        71: KH2Chest(0, "ca02", "m_70"),
        72: KH2Chest(1, "ca02", "m_70"),
        73: KH2Chest(2, "ca02", "m_70"),
        221: KH2Chest(3, "ca02", "m_70"),
        # Cave Mouth
        74: KH2Chest(0, "ca09", "m_70"),
        223: KH2Chest(1, "ca09", "m_70"),
        # Interceptor's Hold
        252: KH2Chest(0, "ca11", "m_70"),
        # Powder Store
        369: KH2Chest(0, "ca12", "m_70"),
        370: KH2Chest(1, "ca12", "m_70"),
        # Moonlight Nook
        75: KH2Chest(0, "ca13", "m_70"),
        224: KH2Chest(1, "ca13", "m_70"),
        371: KH2Chest(2, "ca13", "m_70"),
        # Seadrift Keep
        76: KH2Chest(0, "ca14", "m_70"),
        372: KH2Chest(1, "ca14", "m_70"),
        225: KH2Chest(2, "ca14", "m_70"),
        # Seadrift Row
        77: KH2Chest(0, "ca15", "m_70"),
        373: KH2Chest(1, "ca15", "m_70"),
        78: KH2Chest(2, "ca15", "m_70"),
        # Library
        91: KH2Chest(0, "dc01", "m_70"),
        # DC Courtyard
        16: KH2Chest(0, "dc03", "m_70"),
        17: KH2Chest(1, "dc03", "m_70"),
        18: KH2Chest(2, "dc03", "m_70"),
        92: KH2Chest(3, "dc03", "m_70"),
        93: KH2Chest(4, "dc03", "m_70"),
        247: KH2Chest(5, "dc03", "m_70"),
        248: KH2Chest(6, "dc03", "m_70"),
        # Fragment Crossing
        374: KH2Chest(0, "eh02", "m_70"),
        375: KH2Chest(1, "eh02", "m_70"),
        376: KH2Chest(2, "eh02", "m_70"),
        377: KH2Chest(3, "eh02", "m_70"),
        # Memory's Skyscraper
        391: KH2Chest(0, "eh03", "m_70"),
        523: KH2Chest(1, "eh03", "m_70"),
        524: KH2Chest(2, "eh03", "m_70"),
        # Brink of Despair
        335: KH2Chest(0, "eh04", "m_70"),
        500: KH2Chest(1, "eh04", "m_70"),
        # Nothing's Call
        378: KH2Chest(0, "eh06", "m_70"),
        379: KH2Chest(1, "eh06", "m_70"),
        # Twilight's View
        336: KH2Chest(0, "eh09", "m_70"),
        # Naught's Skyway
        381: KH2Chest(0, "eh12", "m_70"),
        382: KH2Chest(1, "eh12", "m_70"),
        380: KH2Chest(2, "eh12", "m_70"),
        # Ruin and Creation's Passage
        385: KH2Chest(0, "eh17", "m_70"),
        386: KH2Chest(1, "eh17", "m_70"),
        387: KH2Chest(2, "eh17", "m_70"),
        388: KH2Chest(3, "eh17", "m_70"),
        # Crystal Fissure
        180: KH2Chest(0, "hb03", "m_70"),
        181: KH2Chest(1, "hb03", "m_70"),
        179: KH2Chest(2, "hb03", "m_70"),
        489: KH2Chest(3, "hb03", "m_70"),
        # Ansem's Study
        184: KH2Chest(0, "hb05", "m_70"),
        183: KH2Chest(0, "hb05", "m_71"),
        # Postern
        189: KH2Chest(0, "hb06", "m_70"),
        310: KH2Chest(1, "hb06", "m_70"),
        190: KH2Chest(2, "hb06", "m_70"),
        491: KH2Chest(0, "hb06", "m_71"),
        # Borough
        194: KH2Chest(0, "hb09", "m_70"),
        195: KH2Chest(1, "hb09", "m_70"),
        196: KH2Chest(2, "hb09", "m_70"),
        305: KH2Chest(3, "hb09", "m_70"),
        506: KH2Chest(4, "hb09", "m_70"),
        # Corridors
        200: KH2Chest(0, "hb11", "m_70"),
        201: KH2Chest(1, "hb11", "m_70"),
        202: KH2Chest(2, "hb11", "m_70"),
        307: KH2Chest(3, "hb11", "m_70"),
        # Heartless Manufactory
        311: KH2Chest(0, "hb12", "m_70"),
        # Restoration Site
        309: KH2Chest(0, "hb18", "m_70"),
        507: KH2Chest(1, "hb18", "m_70"),
        # CoR Depths
        563: KH2Chest(0, "hb21", "m_70"),
        564: KH2Chest(1, "hb21", "m_70"),
        566: KH2Chest(2, "hb21", "m_70"),
        565: KH2Chest(3, "hb21", "m_70"),
        562: KH2Chest(4, "hb21", "m_70"),
        567: KH2Chest(5, "hb21", "m_70"),
        # CoR Mining Area
        568: KH2Chest(0, "hb22", "m_70"),
        569: KH2Chest(1, "hb22", "m_70"),
        570: KH2Chest(2, "hb22", "m_70"),
        571: KH2Chest(3, "hb22", "m_70"),
        572: KH2Chest(4, "hb22", "m_70"),
        573: KH2Chest(5, "hb22", "m_70"),
        # CoR Engine Chamber
        574: KH2Chest(0, "hb23", "m_70"),
        576: KH2Chest(1, "hb23", "m_70"),
        577: KH2Chest(2, "hb23", "m_70"),
        575: KH2Chest(3, "hb23", "m_70"),
        # CoR Mineshaft
        580: KH2Chest(0, "hb24", "m_70"),
        579: KH2Chest(1, "hb24", "m_70"),
        582: KH2Chest(2, "hb24", "m_70"),
        581: KH2Chest(3, "hb24", "m_70"),
        578: KH2Chest(4, "hb24", "m_70"),
        # Garden of Assemblage
        585: KH2Chest(0, "hb26", "m_70"),
        586: KH2Chest(1, "hb26", "m_70"),
        590: KH2Chest(0, "hb26", "m_71"),
        # Underworld Entrance
        242: KH2Chest(0, "he03", "m_70"),
        # Inner Chamber
        2: KH2Chest(0, "he10", "m_70"),
        243: KH2Chest(1, "he10", "m_70"),
        # Caverns Entrance
        3: KH2Chest(0, "he11", "m_70"),
        11: KH2Chest(1, "he11", "m_70"),
        504: KH2Chest(2, "he11", "m_70"),
        # The Lock
        244: KH2Chest(0, "he12", "m_70"),
        142: KH2Chest(1, "he12", "m_70"),
        5: KH2Chest(2, "he12", "m_70"),
        # Passage
        146: KH2Chest(0, "he15", "m_70"),
        7: KH2Chest(1, "he15", "m_70"),
        8: KH2Chest(2, "he15", "m_70"),
        144: KH2Chest(3, "he15", "m_70"),
        145: KH2Chest(4, "he15", "m_70"),
        # Lost Road
        9: KH2Chest(0, "he16", "m_70"),
        10: KH2Chest(1, "he16", "m_70"),
        148: KH2Chest(2, "he16", "m_70"),
        149: KH2Chest(3, "he16", "m_70"),
        # Atrium
        150: KH2Chest(0, "he17", "m_70"),
        151: KH2Chest(1, "he17", "m_70"),
        # Pride Rock
        393: KH2Chest(0, "lk00", "m_70"),
        392: KH2Chest(1, "lk00", "m_70"),
        418: KH2Chest(2, "lk00", "m_70"),
        # Wildebeest Valley
        396: KH2Chest(0, "lk03", "m_70"),
        397: KH2Chest(1, "lk03", "m_70"),
        398: KH2Chest(2, "lk03", "m_70"),
        399: KH2Chest(3, "lk03", "m_70"),
        400: KH2Chest(4, "lk03", "m_70"),
        # Elephant Graveyard
        401: KH2Chest(0, "lk05", "m_70"),
        403: KH2Chest(1, "lk05", "m_70"),
        402: KH2Chest(2, "lk05", "m_70"),
        509: KH2Chest(3, "lk05", "m_70"),
        508: KH2Chest(4, "lk05", "m_70"),
        # Gorge
        405: KH2Chest(0, "lk06", "m_70"),
        404: KH2Chest(1, "lk06", "m_70"),
        492: KH2Chest(2, "lk06", "m_70"),
        # Wastelands
        406: KH2Chest(0, "lk07", "m_70"),
        408: KH2Chest(1, "lk07", "m_70"),
        407: KH2Chest(2, "lk07", "m_70"),
        # Jungle
        409: KH2Chest(0, "lk08", "m_70"),
        410: KH2Chest(1, "lk08", "m_70"),
        411: KH2Chest(2, "lk08", "m_70"),
        # Oasis"
        412: KH2Chest(0, "lk09", "m_70"),
        493: KH2Chest(1, "lk09", "m_70"),
        413: KH2Chest(2, "lk09", "m_70"),
        # Bamboo Grove
        245: KH2Chest(0, "mu00", "m_70"),
        497: KH2Chest(1, "mu00", "m_70"),
        498: KH2Chest(2, "mu00", "m_70"),
        # Checkpoint
        21: KH2Chest(0, "mu02", "m_70"),
        121: KH2Chest(1, "mu02", "m_70"),
        # Mountain Trail
        22: KH2Chest(0, "mu03", "m_70"),
        23: KH2Chest(1, "mu03", "m_70"),
        122: KH2Chest(2, "mu03", "m_70"),
        123: KH2Chest(3, "mu03", "m_70"),
        # Village Cave
        124: KH2Chest(0, "mu05", "m_70"),
        125: KH2Chest(1, "mu05", "m_70"),
        # Ridge
        24: KH2Chest(0, "mu06", "m_70"),
        126: KH2Chest(1, "mu06", "m_70"),
        # Throne Room
        26: KH2Chest(0, "mu11", "m_70"),
        27: KH2Chest(1, "mu11", "m_70"),
        128: KH2Chest(2, "mu11", "m_70"),
        129: KH2Chest(3, "mu11", "m_70"),
        130: KH2Chest(4, "mu11", "m_70"),
        131: KH2Chest(5, "mu11", "m_70"),
        25: KH2Chest(6, "mu11", "m_70"),
        127: KH2Chest(7, "mu11", "m_70"),
        # Town Square
        209: KH2Chest(0, "nm00", "m_70"),
        210: KH2Chest(1, "nm00", "m_70"),
        # Finklestein's Lab
        211: KH2Chest(0, "nm01", "m_70"),
        # Graveyard
        53: KH2Chest(0, "nm02", "m_70"),
        212: KH2Chest(1, "nm02", "m_70"),
        # Hinterlands
        214: KH2Chest(0, "nm04", "m_70"),
        54: KH2Chest(1, "nm04", "m_70"),
        213: KH2Chest(2, "nm04", "m_70"),
        # Candy Cane Lane
        55: KH2Chest(0, "nm06", "m_70"),
        56: KH2Chest(1, "nm06", "m_70"),
        216: KH2Chest(2, "nm06", "m_70"),
        217: KH2Chest(3, "nm06", "m_70"),
        # Santa's House
        57: KH2Chest(0, "nm08", "m_70"),
        58: KH2Chest(1, "nm08", "m_70"),
        # Starry Hill
        94: KH2Chest(0, "po01", "m_70"),
        312: KH2Chest(1, "po01", "m_70"),
        # Pooh's Howse
        98: KH2Chest(0, "po02", "m_70"),
        97: KH2Chest(1, "po02", "m_70"),
        313: KH2Chest(2, "po02", "m_70"),
        # Rabbit's Howse
        100: KH2Chest(0, "po03", "m_70"),
        101: KH2Chest(1, "po03", "m_70"),
        314: KH2Chest(2, "po03", "m_70"),
        # Piglet's Howse
        105: KH2Chest(0, "po04", "m_70"),
        103: KH2Chest(1, "po04", "m_70"),
        104: KH2Chest(2, "po04", "m_70"),
        # Kanga's Howse
        106: KH2Chest(0, "po05", "m_70"),
        107: KH2Chest(1, "po05", "m_70"),
        108: KH2Chest(2, "po05", "m_70"),
        # Spooky Cave
        116: KH2Chest(0, "po09", "m_70"),
        110: KH2Chest(1, "po09", "m_70"),
        111: KH2Chest(2, "po09", "m_70"),
        112: KH2Chest(3, "po09", "m_70"),
        113: KH2Chest(4, "po09", "m_70"),
        115: KH2Chest(5, "po09", "m_70"),
        # Pit Cell
        64: KH2Chest(0, "tr00", "m_70"),
        316: KH2Chest(1, "tr00", "m_70"),
        # Canyon
        65: KH2Chest(0, "tr01", "m_70"),
        171: KH2Chest(1, "tr01", "m_70"),
        253: KH2Chest(2, "tr01", "m_70"),
        521: KH2Chest(3, "tr01", "m_70"),
        # Hallway
        50: KH2Chest(0, "tr04", "m_70"),
        49: KH2Chest(1, "tr04", "m_70"),
        # Communications Room
        499: KH2Chest(0, "tr05", "m_70"),
        255: KH2Chest(1, "tr05", "m_70"),
        # Central Computer Core
        51: KH2Chest(0, "tr08", "m_70"),
        177: KH2Chest(1, "tr08", "m_70"),
        178: KH2Chest(2, "tr08", "m_70"),
        488: KH2Chest(3, "tr08", "m_70"),
        # STT Central Station
        428: KH2Chest(0, "tt09", "m_70"),
        429: KH2Chest(1, "tt09", "m_70"),
        430: KH2Chest(2, "tt09", "m_70"),
        # STT Sunset Terrace
        434: KH2Chest(0, "tt10", "m_70"),
        435: KH2Chest(1, "tt10", "m_70"),
        436: KH2Chest(2, "tt10", "m_70"),
        437: KH2Chest(3, "tt10", "m_70"),
        # STT Mansion Foyer
        449: KH2Chest(0, "tt15", "m_70"),
        450: KH2Chest(1, "tt15", "m_70"),
        451: KH2Chest(2, "tt15", "m_70"),
        # STT Mansion Dining Room
        455: KH2Chest(0, "tt16", "m_70"),
        456: KH2Chest(1, "tt16", "m_70"),
        # STT Mansion Library
        459: KH2Chest(0, "tt17", "m_70"),
        # STT Mansion Basement
        463: KH2Chest(0, "tt22", "m_70"),
        # STT Dive to the Heart
        315: KH2Chest(0, "tt32", "m_70"),
        472: KH2Chest(0, "tt33", "m_70"),
        # TT Tram Common
        420: KH2Chest(0, "tt07", "m_71"),
        421: KH2Chest(1, "tt07", "m_71"),
        422: KH2Chest(2, "tt07", "m_71"),
        423: KH2Chest(3, "tt07", "m_71"),
        424: KH2Chest(4, "tt07", "m_71"),
        425: KH2Chest(5, "tt07", "m_71"),
        484: KH2Chest(6, "tt07", "m_71"),
        # TT Central Station
        431: KH2Chest(0, "tt09", "m_71"),
        433: KH2Chest(1, "tt09", "m_71"),
        432: KH2Chest(2, "tt09", "m_71"),
        # TT Sunset Terrace
        438: KH2Chest(0, "tt10", "m_71"),
        439: KH2Chest(1, "tt10", "m_71"),
        440: KH2Chest(2, "tt10", "m_71"),
        441: KH2Chest(3, "tt10", "m_71"),
        # TT Woods
        442: KH2Chest(0, "tt13", "m_71"),
        443: KH2Chest(1, "tt13", "m_71"),
        444: KH2Chest(2, "tt13", "m_71"),
        # TT Old Mansion
        447: KH2Chest(0, "tt14", "m_71"),
        448: KH2Chest(1, "tt14", "m_71"),
        # TT Mansion Foyer
        452: KH2Chest(0, "tt15", "m_71"),
        453: KH2Chest(1, "tt15", "m_71"),
        454: KH2Chest(2, "tt15", "m_71"),
        # TT Mansion Dining Room
        457: KH2Chest(0, "tt16", "m_71"),
        458: KH2Chest(1, "tt16", "m_71"),
        # TT Mansion Library
        460: KH2Chest(0, "tt17", "m_71"),
        # TT Mansion Basement
        464: KH2Chest(0, "tt22", "m_71"),
        # TT Yensid Tower
        465: KH2Chest(0, "tt25", "m_71"),
        466: KH2Chest(1, "tt25", "m_71"),
        522: KH2Chest(2, "tt25", "m_71"),
        # TT Yensid Tower Entryway
        467: KH2Chest(0, "tt26", "m_71"),
        468: KH2Chest(1, "tt26", "m_71"),
        # TT Sorcerer's Loft
        469: KH2Chest(0, "tt27", "m_71"),
        # TT Tower Wardrobe
        470: KH2Chest(0, "tt28", "m_71"),
        # TT Tunnelway
        477: KH2Chest(0, "tt36", "m_71"),
        478: KH2Chest(1, "tt36", "m_71"),
        # TT Underground Concourse
        479: KH2Chest(0, "tt37", "m_71"),
        480: KH2Chest(1, "tt37", "m_71"),
        481: KH2Chest(2, "tt37", "m_71"),
        482: KH2Chest(3, "tt37", "m_71"),
        # Cornerstone Hill
        12: KH2Chest(0, "wi00", "m_70"),
        79: KH2Chest(1, "wi00", "m_70"),
        # Pier
        81: KH2Chest(0, "wi01", "m_70"),
        82: KH2Chest(1, "wi01", "m_70"),
        # Wharf
        83: KH2Chest(0, "wi02", "m_70"),
        84: KH2Chest(1, "wi02", "m_70"),
        85: KH2Chest(2, "wi02", "m_70")}


def chest_visual_id(location_types: list[locationType], item_type: itemType) -> int:
    chest_type_id = 4000
    # world determinations
    if locationType.PL in location_types:
        chest_type_id += 40
    elif locationType.TT in location_types or locationType.STT in location_types:
        chest_type_id += 20
    # item type adds a dynamic offset
    if item_type in [itemType.GROWTH_ABILITY, itemType.ACTION_ABILITY, itemType.SUPPORT_ABILITY]:
        chest_type_id += 1
    elif item_type == itemType.FORM:
        chest_type_id += 2
    elif item_type in [itemType.FIRE, itemType.BLIZZARD, itemType.THUNDER, itemType.CURE, itemType.MAGNET, itemType.REFLECT]:
        chest_type_id += 3
    elif item_type == itemType.TORN_PAGE:
        chest_type_id += 4
    elif item_type == itemType.REPORT:
        chest_type_id += 5
    elif item_type in [itemType.GAUGE, itemType.SLOT, itemType.MUNNY_POUCH]:
        chest_type_id += 6
    elif item_type == itemType.SUMMON:
        chest_type_id += 7
    elif item_type in [itemType.STORYUNLOCK, itemType.MANUFACTORYUNLOCK, itemType.TROPHY, itemType.OCSTONE]:
        chest_type_id += 8
    elif item_type in [itemType.KEYBLADE, itemType.SHIELD, itemType.STAFF, itemType.ACCESSORY, itemType.ARMOR]:
        chest_type_id += 9
    elif item_type in [itemType.PROOF_OF_CONNECTION, itemType.PROOF_OF_PEACE, itemType.PROOF_OF_NONEXISTENCE, itemType.PROMISE_CHARM]:
        chest_type_id += 10
    return chest_type_id
