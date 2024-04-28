from PySide6.QtWidgets import QDialog, QWidget, QVBoxLayout

from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class ProgressionPointsDialog(QDialog):

    def __init__(self, parent: QWidget, seed_settings: SeedSettings):
        super().__init__(parent)
        self.setWindowTitle("Progression Points")

        self.seed_settings = seed_settings

        submenu_layout = KH2Submenu("Progression Points", seed_settings)
        submenu_layout.start_column()
        submenu_layout.start_group()
        submenu_layout.add_option(settingkey.PROGRESSION_POINT_SELECT)
        submenu_layout.end_group(title="Progression Points")
        submenu_layout.end_column()
        submenu_layout.finalizeMenu()

        main = QVBoxLayout()
        main.addWidget(submenu_layout)

        self.setLayout(main)
