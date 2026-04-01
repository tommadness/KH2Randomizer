import copy

from PySide6.QtWidgets import QDialog, QWidget, QVBoxLayout, QPushButton

from Class import settingkey
from Class.seedSettings import SeedSettings
from List import ObjectiveList
from List.configDict import ObjectivePoolOption
from UI.Submenus.SubMenu import KH2Submenu


class ObjectiveSelectionDialog(QDialog):

    def __init__(self, parent: QWidget, seed_settings: SeedSettings):
        super().__init__(parent)
        self.setWindowTitle("Objective List")

        self.seed_settings = seed_settings

        self.submenu_layout = KH2Submenu("Possible Objectives", seed_settings)
        self.submenu_layout.start_column()
        objective_groups_layout = QVBoxLayout()
        objective_groups_widget = QWidget()
        objective_groups_widget.setProperty('cssClass', 'layoutWidget')
        objective_groups_widget.setLayout(objective_groups_layout)
        #
        def make_objective_lambda(o: ObjectivePoolOption):
            return lambda : self.select_subset(o)
        for o in ObjectivePoolOption:
            button = QPushButton(o.value)
            objective_groups_layout.addWidget(button)
            button.clicked.connect(make_objective_lambda(o))

        self.submenu_layout._add_option_widget("","",objective_groups_widget)
        self.submenu_layout.end_column(stretch_at_end=True)
        self.submenu_layout.start_column()
        self.submenu_layout.start_group()
        self.submenu_layout.add_option(settingkey.OBJECTIVE_POOL_MULTISELECT)
        self.submenu_layout.end_group(title="Possible Objectives")
        self.submenu_layout.end_column(stretch_at_end=True)
        self.submenu_layout.finalizeMenu()

        main = QVBoxLayout()
        main.addWidget(self.submenu_layout)

        self.setLayout(main)

    def select_subset(self, pool_option: ObjectivePoolOption):
        full_objective_list = ObjectiveList.get_full_objective_list()
        if pool_option == ObjectivePoolOption.BOSSES.value:
            full_objective_list = [o for o in full_objective_list if o.Type == ObjectiveList.ObjectiveType.BOSS]
        elif pool_option == ObjectivePoolOption.NOBOSSES.value:
            full_objective_list = [o for o in full_objective_list if o.Type == ObjectiveList.ObjectiveType.WORLDPROGRESS or o.Type == ObjectiveList.ObjectiveType.FIGHT]
        elif pool_option == ObjectivePoolOption.HITLIST.value:
            full_objective_list = [o for o in full_objective_list if o.Difficulty==ObjectiveList.ObjectiveDifficulty.LATEST ]
        elif pool_option == ObjectivePoolOption.LASTSTORY.value:
            full_objective_list = ObjectiveList.get_last_story_objectives()

        setting,widget = self.submenu_layout.widgets_and_settings_by_name[settingkey.OBJECTIVE_POOL_MULTISELECT]
        for selected in setting.choice_keys:
            in_objective_pool = any([selected == obj.Name for obj in full_objective_list])
            index = setting.choice_keys.index(selected)
            widget.item(index).setSelected(in_objective_pool)


