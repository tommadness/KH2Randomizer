from Class.newLocationClass import KH2Location
from List.configDict import locationType
from List.location.graph import double_bonus, item_bonus


def goofy_bonuses() -> list[KH2Location]:
    return [
        double_bonus(21, "Barbossa", locationType.PR),
        item_bonus(59, "Grim Reaper 1", locationType.PR),
        item_bonus(31, "Hostile Program", locationType.SP),
        item_bonus(49, "Hyenas 1", locationType.PL),
        item_bonus(50, "Hyenas 2", locationType.PL),
        item_bonus(40, "Lock/Shock/Barrel", locationType.HT),
        item_bonus(19, "Oogie Boogie", locationType.HT),
        item_bonus(6, "Pete (Olympus)", locationType.OC),
        item_bonus(17, "Pete (Wharf)", locationType.DC),
        item_bonus(9, "Shan-Yu", locationType.LoD),
        item_bonus(10, "Storm Rider", locationType.LoD),
        item_bonus(12, "Beast", locationType.BC),
        item_bonus(39, "Interceptor Barrels", locationType.PR),
        item_bonus(46, "Treasure Room Heartless", locationType.Agrabah),
        item_bonus(66, "Zexion", [locationType.OC, locationType.AS]),
    ]
