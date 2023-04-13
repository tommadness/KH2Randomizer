import random
from typing import Any

VANILLA = "vanilla"
RANDOMIZE_ONE = "rand1"
RANDOMIZE_ALL = "randAll"
AGRABAH = "al0"
BEAST_CASTLE = "bb0"
PORT_ROYAL = "ca0"
DISNEY_CASTLE = "dc0"
LINGERING_WILL = "dc1"
DESTINY_ISLANDS = "di0"
TWTNW = "eh0"
ROXAS = "eh1"
AGRABAH_ALT = "es0"
HOLLOW_BASTION = "hb0"
GARDEN_OF_ASSEMBLAGE = "hb1"
ABSENT_SILHOUETTE = "hb2"
OLYMPUS_COLISEUM = "he0"
UNDERWORLD = "he1"
PRIDE_LANDS = "lk0"
ATLANTICA = "lm0"
LAND_OF_DRAGONS = "mu0"
HALLOWEEN_TOWN = "nm0"
CHRISTMAS_TOWN = "nm1"
HUNDRED_ACRE_WOOD = "po0"
SPACE_PARANOIDS = "tr0"
TWILIGHT_TOWN = "tt0"
STATION_OF_CALLING = "tt1"
MYSTERIOUS_TOWER = "tt2"
MANSION_BASEMENT = "tt3"
WHITE_ROOM = "tt4"
MANSION = "tt5"
BETWIXT_BETWEEN = "tt6"
TIMELESS_RIVER = "wi0"
WORLD_MAP = "wm0"
KINGDOM_HEARTS_1 = "zz0"


def get_options() -> dict[str, str]:
    return {
        VANILLA: "Vanilla",
        RANDOMIZE_ONE: "Randomize (one)",
        RANDOMIZE_ALL: "Randomize (all)",
        AGRABAH: "Agrabah",
        BEAST_CASTLE: "Beast's Castle",
        PORT_ROYAL: "Port Royal",
        DISNEY_CASTLE: "Disney Castle",
        LINGERING_WILL: "Lingering Will",
        # DESTINY_ISLANDS: "Destiny Island",  # no visible difference from KH1
        TWTNW: "The World That Never Was",
        ROXAS: "Roxas Fight",  # looks like KH1 but with classic icons
        # AGRABAH_ALT: "Agrabah (alt),  # for carpet minigames? need to check for differences.
        HOLLOW_BASTION: "Hollow Bastion",
        GARDEN_OF_ASSEMBLAGE: "Garden of Assemblage",
        ABSENT_SILHOUETTE: "Absent Silhouette",
        OLYMPUS_COLISEUM: "Olympus Coliseum",
        UNDERWORLD: "The Underworld",
        PRIDE_LANDS: "Pride Lands",
        ATLANTICA: "Atlantica (PCSX2 Only)",
        LAND_OF_DRAGONS: "Land of Dragons",
        HALLOWEEN_TOWN: "Halloween Town",
        CHRISTMAS_TOWN: "Christmas Town",
        HUNDRED_ACRE_WOOD: "100 Acre Wood",
        SPACE_PARANOIDS: "Space Paranoids",
        TWILIGHT_TOWN: "Twilight Town",
        STATION_OF_CALLING: "Station of Calling",  # looks like kh1 but with classic icons.
        MYSTERIOUS_TOWER: "Mysterious Tower",
        MANSION_BASEMENT: "Mansion Basement",
        WHITE_ROOM: "The White Room",
        MANSION: "Mansion",
        BETWIXT_BETWEEN: "Betwixt & Between",
        TIMELESS_RIVER: "Timeless River",
        # WORLD_MAP: "World Map",  # no visible difference from Betwixt & Between
        KINGDOM_HEARTS_1: "Kingdom Hearts 1"
    }


def randomize_command_menus(command_menu_choice: str) -> list[dict[str, Any]]:
    if command_menu_choice == VANILLA:
        return []
    assets = []
    assets.extend(_randomize_ps2(command_menu_choice))
    assets.extend(_randomize_pc(command_menu_choice))
    return assets


def _randomize_ps2(command_menu_choice: str) -> list[dict[str, Any]]:
    menu_replacements = _compute_menu_replacements(command_menu_choice, pc=False)
    assets: list[dict[str, Any]] = []
    for old_menu, new_menu in menu_replacements.items():
        assets.append({
            "platform": "ps2",
            "name": f"field2d/jp/{old_menu}command.2dd",
            "multi": [
                {"name": f"field2d/us/{old_menu}command.2dd"}
            ],
            "method": "copy",
            "source": [
                {
                    "name": f"field2d/jp/{new_menu}command.2dd",
                    "type": "internal"
                }
            ]
        })
    return assets


def _randomize_pc(command_menu_choice: str) -> list[dict[str, Any]]:
    menu_replacements = _compute_menu_replacements(command_menu_choice, pc=True)
    assets: list[dict[str, Any]] = []
    for old_menu, new_menu in menu_replacements.items():
        if new_menu == ATLANTICA:
            # Unsupported on PC - just leave it vanilla
            continue

        for region in ["fr", "gr", "it", "sp", "us"]:
            assets.append({
                "platform": "pc",
                "name": f"field2d/{region}/{old_menu}command.2dd",
                "method": "copy",
                "source": [
                    {
                        "name": f"field2d/{region}/{new_menu}command.2dd",
                        "type": "internal"
                    }
                ]
            }),
            remastered_region = f"remastered/field2d/{region}"
            cap_region = region.upper()
            assets.append({
                "platform": "pc",
                "name": f"{remastered_region}/{old_menu}command.2dd/{cap_region}_{old_menu}command_2dd0.png",
                "method": "copy",
                "source": [
                    {
                        "name": f"{remastered_region}/{new_menu}command.2dd/{cap_region}_{new_menu}command_2dd0.png",
                        "type": "internal"
                    }
                ]
            })
    return assets


def _compute_menu_replacements(command_menu_choice: str, pc: bool) -> dict[str, str]:
    unsupported = [VANILLA, RANDOMIZE_ONE, RANDOMIZE_ALL]
    if pc:
        unsupported.append(ATLANTICA)
    supported_menus = [menu for menu in get_options().keys() if menu not in unsupported]

    menu_replacements: dict[str, str] = {}
    if command_menu_choice == RANDOMIZE_ALL:
        shuffled_menus = supported_menus.copy()
        random.shuffle(shuffled_menus)
        for index, old_menu in enumerate(supported_menus):
            menu_replacements[old_menu] = shuffled_menus[index]
    elif command_menu_choice == RANDOMIZE_ONE:
        new_menu = random.choice(supported_menus)
        for old_menu in supported_menus:
            menu_replacements[old_menu] = new_menu
    else:  # A specific command menu was chosen
        for old_menu in supported_menus:
            menu_replacements[old_menu] = command_menu_choice
    return menu_replacements
