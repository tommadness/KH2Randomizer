from Class import settingkey
from Class.seedSettings import SeedSettings
from List.configDict import FinalDoorRequirement
from UI.Submenus.SubMenu import KH2Submenu


class ItemPlacementMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Rules/Placement', settings=settings)
        self.disable_signal = False

        self.start_column()
        self.start_group()
        self.add_option(settingkey.FINAL_DOOR_REQUIREMENT)
        self.add_option(settingkey.OBJECTIVE_RANDO_NUM_REQUIRED)
        self.add_option(settingkey.OBJECTIVE_RANDO_NUM_AVAILABLE)
        self.add_option(settingkey.OBJECTIVE_RANDO_PROGRESS)
        self.add_option(settingkey.OBJECTIVE_RANDO_BOSSES)
        self.add_option(settingkey.EMBLEM_NUM_REQUIRED)
        self.add_option(settingkey.EMBLEM_NUM_AVAILABLE)
        self.end_group("Final Door Requirement")
        self.start_group()
        self.add_option(settingkey.ACCESSIBILITY)
        self.add_option(settingkey.SOFTLOCK_CHECKING)
        self.add_option(settingkey.NIGHTMARE_LOGIC)
        self.end_group('Where Items Can Go')
        self.end_column()

        self.start_column()
        self.start_group()
        self.add_option(settingkey.STORY_UNLOCK_DEPTH)
        self.add_option(settingkey.REPORT_DEPTH)
        self.add_option(settingkey.PROOF_DEPTH)
        self.add_option(settingkey.PROMISE_CHARM_DEPTH)
        self.add_option(settingkey.YEET_THE_BEAR)
        self.end_group('Guaranteed Restrictions')
        self.start_group()
        self.add_option(settingkey.WEIGHTED_FORMS)
        self.add_option(settingkey.WEIGHTED_UNLOCKS)
        self.add_option(settingkey.WEIGHTED_MAGIC)
        self.add_option(settingkey.WEIGHTED_PAGES)
        self.add_option(settingkey.WEIGHTED_SUMMONS)
        self.add_option(settingkey.WEIGHTED_REPORTS)
        self.add_option(settingkey.WEIGHTED_PROOFS)
        self.add_option(settingkey.WEIGHTED_PROMISE_CHARM)
        self.end_group('Item Placement Biases')
        self.end_column()

        self.start_column()
        self.start_group()
        self.add_option(settingkey.CHAIN_LOGIC)
        self.add_option(settingkey.CHAIN_LOGIC_LENGTH)
        self.add_option(settingkey.MAX_CHAIN_LOGIC_LENGTH)
        self.end_group('Chain Logic')
        self.end_column()

        self.finalizeMenu()

        settings.observe(settingkey.ENABLE_PROMISE_CHARM, self.promise_charm_enabled)
        settings.observe(settingkey.CHAIN_LOGIC, self.chain_logic)
        settings.observe(settingkey.FINAL_DOOR_REQUIREMENT, self._final_door_requirement_changed)

    def promise_charm_enabled(self):
        promise_charm_toggle = self.settings.get(settingkey.ENABLE_PROMISE_CHARM)
        _, widget = self.widgets_and_settings_by_name[settingkey.PROMISE_CHARM_DEPTH]
        if not self.disable_signal:
            widget.setEnabled(promise_charm_toggle)

    def chain_logic(self):
        enabled = self.settings.get(settingkey.CHAIN_LOGIC)
        self.set_option_visibility(settingkey.CHAIN_LOGIC_LENGTH, enabled)
        self.set_option_visibility(settingkey.MAX_CHAIN_LOGIC_LENGTH, enabled)

    def _final_door_requirement_changed(self):
        requirement = FinalDoorRequirement[self.settings.get(settingkey.FINAL_DOOR_REQUIREMENT)]
        objectives_enabled = requirement is FinalDoorRequirement.OBJECTIVES
        emblems_enabled = requirement is FinalDoorRequirement.EMBLEMS
        self.set_option_visibility(settingkey.OBJECTIVE_RANDO_NUM_AVAILABLE, objectives_enabled)
        self.set_option_visibility(settingkey.OBJECTIVE_RANDO_NUM_REQUIRED, objectives_enabled)
        self.set_option_visibility(settingkey.OBJECTIVE_RANDO_PROGRESS, objectives_enabled)
        self.set_option_visibility(settingkey.OBJECTIVE_RANDO_BOSSES, objectives_enabled)
        self.set_option_visibility(settingkey.EMBLEM_NUM_AVAILABLE, emblems_enabled)
        self.set_option_visibility(settingkey.EMBLEM_NUM_REQUIRED, emblems_enabled)

    def disable_widgets(self):
        self.disable_signal = True
        super().disable_widgets()
