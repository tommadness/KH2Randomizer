from Class.newLocationClass import KH2Location
from List.configDict import locationType
from List.location.graph import double_bonus, item_bonus


def donald_bonuses() -> list[KH2Location]:
    return [
        item_bonus(42, "Abu Escort", locationType.Agrabah),
        item_bonus(45, "Screens", locationType.SP),
        item_bonus(28, "Demyx (Hollow Bastion)", locationType.HB),
        item_bonus(58, "Demyx (Olympus)", locationType.OC),
        item_bonus(22, "Grim Reaper 2", locationType.PR),
        double_bonus(16, "Boat Pete", locationType.DC),
        item_bonus(18, "Prison Keeper", locationType.HT),
        item_bonus(29, "Scar", locationType.PL),
        item_bonus(61, "Solar Sailor", locationType.SP),
        item_bonus(20, "Experiment", locationType.HT),
        item_bonus(62, "Boat Fight", locationType.PR),
        item_bonus(56, "Mansion", locationType.TT),
        item_bonus(2, "Posessor", locationType.BC),
        item_bonus(4, "Xaldin", locationType.BC),
    ]
