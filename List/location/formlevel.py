from typing import Optional

from Class.newLocationClass import KH2Location
from List.configDict import locationType
from List.inventory import ability, form as driveform, growth
from List.inventory.form import DriveForm
from List.inventory.item import InventoryItem
from List.location.graph import RequirementEdge, LocationGraphBuilder, START_NODE
from Module.itemPlacementRestriction import ItemPlacementHelpers


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
            3: growth.HighJump1,
            4: ability.ComboPlus,
            5: growth.HighJump2,
            6: ability.ComboPlus,
            7: growth.HighJump3
        },
        driveform.WisdomForm: {
            1: None,
            2: ability.AutoWisdom,
            3: growth.QuickRun1,
            4: ability.MpRage,
            5: growth.QuickRun2,
            6: ability.MpHaste,
            7: growth.QuickRun3
        },
        driveform.LimitForm: {
            1: None,
            2: ability.AutoLimitForm,
            3: growth.DodgeRoll1,
            4: ability.Draw,
            5: growth.DodgeRoll2,
            6: ability.LuckyLucky,
            7: growth.DodgeRoll3
        },
        driveform.MasterForm: {
            1: None,
            2: ability.AutoMaster,
            3: growth.AerialDodge1,
            4: ability.AirComboPlus,
            5: growth.AerialDodge2,
            6: ability.AirComboPlus,
            7: growth.AerialDodge3
        },
        driveform.FinalForm: {
            1: None,
            2: ability.AutoFinal,
            3: growth.Glide1,
            4: ability.FormBoost,
            5: growth.Glide2,
            6: ability.FormBoost,
            7: growth.Glide3
        }
    }

    form_helper = ItemPlacementHelpers.make_form_lambda
    settings = graph.settings
    extended_placement_logic = settings.extended_placement_logic
    if extended_placement_logic and settings.disable_final_form:
        form_helper = ItemPlacementHelpers.make_form_lambda_nightmare_no_final
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
