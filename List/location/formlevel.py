from enum import Enum
from typing import Optional

from Class.newLocationClass import KH2Location
from List.configDict import locationType
from List.inventory import ability, form as driveform, growth
from List.inventory.form import DriveForm
from List.inventory.item import InventoryItem
from List.location.graph import RequirementEdge, LocationGraphBuilder, START_NODE
from Module.itemPlacementRestriction import ItemPlacementHelpers


class CheckLocation(str, Enum):
    Valor2 = "Valor Level 2"
    Valor3 = "Valor Level 3"
    Valor4 = "Valor Level 4"
    Valor5 = "Valor Level 5"
    Valor6 = "Valor Level 6"
    Valor7 = "Valor Level 7"
    Wisdom2 = "Wisdom Level 2"
    Wisdom3 = "Wisdom Level 3"
    Wisdom4 = "Wisdom Level 4"
    Wisdom5 = "Wisdom Level 5"
    Wisdom6 = "Wisdom Level 6"
    Wisdom7 = "Wisdom Level 7"
    Limit2 = "Limit Level 2"
    Limit3 = "Limit Level 3"
    Limit4 = "Limit Level 4"
    Limit5 = "Limit Level 5"
    Limit6 = "Limit Level 6"
    Limit7 = "Limit Level 7"
    Master2 = "Master Level 2"
    Master3 = "Master Level 3"
    Master4 = "Master Level 4"
    Master5 = "Master Level 5"
    Master6 = "Master Level 6"
    Master7 = "Master Level 7"
    Final2 = "Final Level 2"
    Final3 = "Final Level 3"
    Final4 = "Final Level 4"
    Final5 = "Final Level 5"
    Final6 = "Final Level 6"
    Final7 = "Final Level 7"


def form_level(level: int, form: DriveForm, vanilla: Optional[InventoryItem] = None) -> KH2Location:
    types = [locationType.FormLevel]
    if level == 1:
        types.append(locationType.FormLevel1)

    vanilla_items: list[int] = []
    if vanilla is not None:
        vanilla_items.append(vanilla.id)

    description = f"{form.short_name} Level {level}"
    return KH2Location(level, description, form.level_category, types, VanillaItems=vanilla_items)


def make_graph(graph: LocationGraphBuilder):
    forms_with_vanilla_rewards = {
        driveform.ValorForm: {
            1: None,
            2: ability.AutoValor,
            3: growth.HighJump2,
            4: ability.ComboPlus,
            5: growth.HighJump3,
            6: ability.ComboPlus,
            7: growth.HighJumpMax
        },
        driveform.WisdomForm: {
            1: None,
            2: ability.AutoWisdom,
            3: growth.QuickRun2,
            4: ability.MpRage,
            5: growth.QuickRun3,
            6: ability.MpHaste,
            7: growth.QuickRunMax
        },
        driveform.LimitForm: {
            1: None,
            2: ability.AutoLimitForm,
            3: growth.DodgeRoll2,
            4: ability.Draw,
            5: growth.DodgeRoll3,
            6: ability.LuckyLucky,
            7: growth.DodgeRollMax
        },
        driveform.MasterForm: {
            1: None,
            2: ability.AutoMaster,
            3: growth.AerialDodge2,
            4: ability.AirComboPlus,
            5: growth.AerialDodge3,
            6: ability.AirComboPlus,
            7: growth.AerialDodgeMax
        },
        driveform.FinalForm: {
            1: None,
            2: ability.AutoFinal,
            3: growth.Glide2,
            4: ability.FormBoost,
            5: growth.Glide3,
            6: ability.FormBoost,
            7: growth.GlideMax
        }
    }

    form_helper = ItemPlacementHelpers.make_form_lambda
    settings = graph.settings
    extended_placement_logic = settings.extended_placement_logic
    if extended_placement_logic and settings.disable_final_form:
        form_helper = ItemPlacementHelpers.make_form_lambda_nightmare_no_final
    elif extended_placement_logic and settings.disable_antiform:
        form_helper = ItemPlacementHelpers.make_form_lambda_nightmare_no_anti
    elif extended_placement_logic:
        form_helper = ItemPlacementHelpers.make_form_lambda_nightmare

    for form, vanilla_rewards in forms_with_vanilla_rewards.items():
        locations: dict[int, str] = {}
        for level in range(1, 8):
            locations[level] = graph.add_location(f"{form.short_name}-{level}", [
                form_level(level, form, vanilla=vanilla_rewards[level])
            ])

        graph.add_edge(START_NODE, locations[1])
        for level in range(2, 8):
            graph.add_edge(locations[level - 1], locations[level], RequirementEdge(req=form_helper(form, level)))
