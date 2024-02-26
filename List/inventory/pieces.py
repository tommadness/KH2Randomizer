from dataclasses import dataclass, field

from List.configDict import itemType
from List.inventory.item import InventoryItem


@dataclass(frozen=True)
class Piece(InventoryItem):
    id: int
    name: str
    type: itemType = field(init=False, default=itemType.PIECE)


Awakening1 = Piece(1001, "Awakening 1")
Awakening2 = Piece(1002, "Awakening 2")
Awakening3 = Piece(1003, "Awakening 3")
Awakening4 = Piece(1004, "Awakening 4")
Awakening5 = Piece(1005, "Awakening 5")
Awakening6 = Piece(1006, "Awakening 6")
Awakening7 = Piece(1007, "Awakening 7")
Awakening8 = Piece(1008, "Awakening 8")
Awakening9 = Piece(1009, "Awakening 9")
Awakening10 = Piece(1010, "Awakening 10")
Awakening11 = Piece(1011, "Awakening 11")
Awakening12 = Piece(1012, "Awakening 12")


def all_awakening_pieces() -> list[Piece]:
    return [Awakening1,Awakening2,Awakening3,Awakening4,Awakening5,Awakening6,
            Awakening7,Awakening8,Awakening9,Awakening10,Awakening11,Awakening12]

Heart1 = Piece(1013, "Heart 1")
Heart2 = Piece(1014, "Heart 2")
Heart3 = Piece(1015, "Heart 3")
Heart4 = Piece(1016, "Heart 4")
Heart5 = Piece(1017, "Heart 5")
Heart6 = Piece(1018, "Heart 6")
Heart7 = Piece(1019, "Heart 7")
Heart8 = Piece(1020, "Heart 8")
Heart9 = Piece(1021, "Heart 9")
Heart10 = Piece(1022, "Heart 10")
Heart11 = Piece(1023, "Heart 11")
Heart12 = Piece(1024, "Heart 12")

def all_heart_pieces() -> list[Piece]:
    return [Heart1,Heart2,Heart3,Heart4,Heart5,Heart6,
            Heart7,Heart8,Heart9,Heart10,Heart11,Heart12]

Duality1 = Piece(1025, "Duality 1")
Duality2 = Piece(1026, "Duality 2")
Duality3 = Piece(1027, "Duality 3")
Duality4 = Piece(1028, "Duality 4")
Duality5 = Piece(1029, "Duality 5")
Duality6 = Piece(1030, "Duality 6")
Duality7 = Piece(1031, "Duality 7")
Duality8 = Piece(1032, "Duality 8")
Duality9 = Piece(1033, "Duality 9")
Duality10 = Piece(1034, "Duality 10")
Duality11 = Piece(1035, "Duality 11")
Duality12 = Piece(1036, "Duality 12")

def all_duality_pieces() -> list[Piece]:
    return [Duality1,Duality2,Duality3,Duality4,Duality5,Duality6,
            Duality7,Duality8,Duality9,Duality10,Duality11,Duality12]

Frontier1 = Piece(1037, "Frontier 1")
Frontier2 = Piece(1038, "Frontier 2")
Frontier3 = Piece(1039, "Frontier 3")
Frontier4 = Piece(1040, "Frontier 4")
Frontier5 = Piece(1041, "Frontier 5")
Frontier6 = Piece(1042, "Frontier 6")
Frontier7 = Piece(1043, "Frontier 7")
Frontier8 = Piece(1044, "Frontier 8")
Frontier9 = Piece(1045, "Frontier 9")
Frontier10 = Piece(1046, "Frontier 10")
Frontier11 = Piece(1047, "Frontier 11")
Frontier12 = Piece(1048, "Frontier 12")

def all_frontier_pieces() -> list[Piece]:
    return [Frontier1,Frontier2,Frontier3,Frontier4,Frontier5,Frontier6,
            Frontier7,Frontier8,Frontier9,Frontier10,Frontier11,Frontier12]

Daylight1 = Piece(1049, "Daylight 1")
Daylight2 = Piece(1050, "Daylight 2")
Daylight3 = Piece(1051, "Daylight 3")
Daylight4 = Piece(1052, "Daylight 4")
Daylight5 = Piece(1053, "Daylight 5")
Daylight6 = Piece(1054, "Daylight 6")
Daylight7 = Piece(1055, "Daylight 7")
Daylight8 = Piece(1056, "Daylight 8")
Daylight9 = Piece(1057, "Daylight 9")
Daylight10 = Piece(1058, "Daylight 10")
Daylight11 = Piece(1059, "Daylight 11")
Daylight12 = Piece(1060, "Daylight 12")
Daylight13 = Piece(1061, "Daylight 13")
Daylight14 = Piece(1062, "Daylight 14")
Daylight15 = Piece(1063, "Daylight 15")
Daylight16 = Piece(1064, "Daylight 16")
Daylight17 = Piece(1065, "Daylight 17")
Daylight18 = Piece(1066, "Daylight 18")
Daylight19 = Piece(1067, "Daylight 19")
Daylight20 = Piece(1068, "Daylight 20")
Daylight21 = Piece(1069, "Daylight 21")
Daylight22 = Piece(1070, "Daylight 22")
Daylight23 = Piece(1071, "Daylight 23")
Daylight24 = Piece(1072, "Daylight 24")
Daylight25 = Piece(1073, "Daylight 25")
Daylight26 = Piece(1074, "Daylight 26")
Daylight27 = Piece(1075, "Daylight 27")
Daylight28 = Piece(1076, "Daylight 28")
Daylight29 = Piece(1077, "Daylight 29")
Daylight30 = Piece(1078, "Daylight 30")
Daylight31 = Piece(1079, "Daylight 31")
Daylight32 = Piece(1080, "Daylight 32")
Daylight33 = Piece(1081, "Daylight 33")
Daylight34 = Piece(1082, "Daylight 34")
Daylight35 = Piece(1083, "Daylight 35")
Daylight36 = Piece(1084, "Daylight 36")
Daylight37 = Piece(1085, "Daylight 37")
Daylight38 = Piece(1086, "Daylight 38")
Daylight39 = Piece(1087, "Daylight 39")
Daylight40 = Piece(1088, "Daylight 40")
Daylight41 = Piece(1089, "Daylight 41")
Daylight42 = Piece(1090, "Daylight 42")
Daylight43 = Piece(1091, "Daylight 43")
Daylight44 = Piece(1092, "Daylight 44")
Daylight45 = Piece(1093, "Daylight 45")
Daylight46 = Piece(1094, "Daylight 46")
Daylight47 = Piece(1095, "Daylight 47")
Daylight48 = Piece(1096, "Daylight 48")


def all_daylight_pieces() -> list[Piece]:
    return [Daylight1,Daylight2,Daylight3,Daylight4,Daylight5,Daylight6,
        Daylight7,Daylight8,Daylight9,Daylight10,Daylight11,Daylight12,
        Daylight13,Daylight14,Daylight15,Daylight16,Daylight17,Daylight18,
        Daylight19,Daylight20,Daylight21,Daylight22,Daylight23,Daylight24,
        Daylight25,Daylight26,Daylight27,Daylight28,Daylight29,Daylight30,
        Daylight31,Daylight32,Daylight33,Daylight34,Daylight35,Daylight36,
        Daylight37,Daylight38,Daylight39,Daylight40,Daylight41,Daylight42,
        Daylight43,Daylight44,Daylight45,Daylight46,Daylight47,Daylight48]

Sunset1 = Piece(1097, "Sunset 1")
Sunset2 = Piece(1098, "Sunset 2")
Sunset3 = Piece(1099, "Sunset 3")
Sunset4 = Piece(1100, "Sunset 4")
Sunset5 = Piece(1101, "Sunset 5")
Sunset6 = Piece(1102, "Sunset 6")
Sunset7 = Piece(1103, "Sunset 7")
Sunset8 = Piece(1104, "Sunset 8")
Sunset9 = Piece(1105, "Sunset 9")
Sunset10 = Piece(1106, "Sunset 10")
Sunset11 = Piece(1107, "Sunset 11")
Sunset12 = Piece(1108, "Sunset 12")
Sunset13 = Piece(1109, "Sunset 13")
Sunset14 = Piece(1110, "Sunset 14")
Sunset15 = Piece(1111, "Sunset 15")
Sunset16 = Piece(1112, "Sunset 16")
Sunset17 = Piece(1113, "Sunset 17")
Sunset18 = Piece(1114, "Sunset 18")
Sunset19 = Piece(1115, "Sunset 19")
Sunset20 = Piece(1116, "Sunset 20")
Sunset21 = Piece(1117, "Sunset 21")
Sunset22 = Piece(1118, "Sunset 22")
Sunset23 = Piece(1119, "Sunset 23")
Sunset24 = Piece(1120, "Sunset 24")
Sunset25 = Piece(1121, "Sunset 25")
Sunset26 = Piece(1122, "Sunset 26")
Sunset27 = Piece(1123, "Sunset 27")
Sunset28 = Piece(1124, "Sunset 28")
Sunset29 = Piece(1125, "Sunset 29")
Sunset30 = Piece(1126, "Sunset 30")
Sunset31 = Piece(1127, "Sunset 31")
Sunset32 = Piece(1128, "Sunset 32")
Sunset33 = Piece(1129, "Sunset 33")
Sunset34 = Piece(1130, "Sunset 34")
Sunset35 = Piece(1131, "Sunset 35")
Sunset36 = Piece(1132, "Sunset 36")
Sunset37 = Piece(1133, "Sunset 37")
Sunset38 = Piece(1134, "Sunset 38")
Sunset39 = Piece(1135, "Sunset 39")
Sunset40 = Piece(1136, "Sunset 40")
Sunset41 = Piece(1137, "Sunset 41")
Sunset42 = Piece(1138, "Sunset 42")
Sunset43 = Piece(1139, "Sunset 43")
Sunset44 = Piece(1140, "Sunset 44")
Sunset45 = Piece(1141, "Sunset 45")
Sunset46 = Piece(1142, "Sunset 46")
Sunset47 = Piece(1143, "Sunset 47")
Sunset48 = Piece(1144, "Sunset 48")


def all_sunset_pieces() -> list[Piece]:
    return [Sunset1,Sunset2,Sunset3,Sunset4,Sunset5,Sunset6,
        Sunset7,Sunset8,Sunset9,Sunset10,Sunset11,Sunset12,
        Sunset13,Sunset14,Sunset15,Sunset16,Sunset17,Sunset18,
        Sunset19,Sunset20,Sunset21,Sunset22,Sunset23,Sunset24,
        Sunset25,Sunset26,Sunset27,Sunset28,Sunset29,Sunset30,
        Sunset31,Sunset32,Sunset33,Sunset34,Sunset35,Sunset36,
        Sunset37,Sunset38,Sunset39,Sunset40,Sunset41,Sunset42,
        Sunset43,Sunset44,Sunset45,Sunset46,Sunset47,Sunset48]