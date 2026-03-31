from PySide6.QtWidgets import QDialog, QWidget, QVBoxLayout

from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class ObjectiveSelectionDialog(QDialog):

    def __init__(self, parent: QWidget, seed_settings: SeedSettings):
        super().__init__(parent)
        self.setWindowTitle("Objective List")

        self.seed_settings = seed_settings

        submenu_layout = KH2Submenu("Possible Objectives", seed_settings)
        submenu_layout.start_column()
        submenu_layout.start_group()
        submenu_layout.add_option(settingkey.OBJECTIVE_POOL_MULTISELECT)
        submenu_layout.end_group(title="Possible Objectives")
        submenu_layout.end_column(stretch_at_end=True)
        submenu_layout.finalizeMenu()

        main = QVBoxLayout()
        main.addWidget(submenu_layout)

        self.setLayout(main)
