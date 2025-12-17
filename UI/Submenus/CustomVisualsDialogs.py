import os
from pathlib import Path
from typing import Optional

from PIL import Image
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QDialog, QVBoxLayout, QWidget, QLabel, QScrollArea, QGridLayout, QMenuBar, QMenu, QFrame

from Module import appconfig
from Module.cosmeticsmods.endingpic import EndingPictureRandomizer
from Module.cosmeticsmods.field2d import RoomTransitionImageRandomizer, CommandMenuRandomizer
from Module.cosmeticsmods.itempic import ItempicRandomizer
from UI import configui
from UI.Submenus.SubMenu import KH2Submenu, header_styles
from UI.qtlib import clear_layout, show_alert, button


class VisualsViewerDialog(QDialog):

    def __init__(self, parent: Optional[QWidget], title: str, folder_name: str):
        super().__init__(parent)
        self.title = title
        self.folder_name = folder_name

        self.setWindowTitle(title)

        menu_bar = QMenuBar()
        file_menu = QMenu("File")
        file_menu.addAction(f"Open Custom {title} Folder", self.open_custom_visuals_folder)
        menu_bar.addMenu(file_menu)

        main = QVBoxLayout()
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(menu_bar)

        grid_scroll = QScrollArea()
        grid_widget = QWidget()
        grid_scroll.setWidget(grid_widget)
        grid_scroll.setWidgetResizable(True)

        scroll_layout = QVBoxLayout()
        self.scroll_layout = scroll_layout
        grid_widget.setLayout(scroll_layout)
        main.addWidget(grid_scroll)

        self.setLayout(main)
        self.setMinimumWidth(900)
        self.setMinimumHeight(600)

        self.refresh_layout()

    def refresh_layout(self):
        raise Exception("refresh_layout() not implemented")

    @staticmethod
    def refresh_grid(grid: QGridLayout, images: list[Path], size: QSize, columns: int, frame: bool=False):
        clear_layout(grid)

        row = 0
        column = 0
        for image_path in images:
            with Image.open(image_path) as image:
                image_label = QLabel()
                if frame:
                    image_label.setFrameShape(QFrame.Shape.StyledPanel)
                image_label.setFixedSize(size)
                image_label.setPixmap(image.resize((size.width(), size.height())).toqpixmap())
                grid.addWidget(image_label, row, column)

                column = column + 1
                if column == columns:
                    row = row + 1
                    column = 0

    def require_custom_visuals(self, grid: QGridLayout) -> bool:
        clear_layout(grid)

        if appconfig.read_custom_visuals_path() is None:
            label = QLabel(configui.CUSTOM_VISUALS_NOT_CHOSEN)
            configure_button = button("Configure", self._configure_custom_visuals)
            grid.addWidget(label, 0, 0)
            grid.addWidget(configure_button, 1, 0)
            return False
        else:
            return True

    def require_extracted_data(self, grid: QGridLayout) -> bool:
        clear_layout(grid)

        if appconfig.read_openkh_path() is None:
            label = QLabel(configui.OPENKH_LOCATION_NOT_CHOSEN)
            configure_button = button("Configure", self._configure_openkh)
            grid.addWidget(label, 0, 0)
            grid.addWidget(configure_button, 1, 0)
            return False
        elif appconfig.extracted_game_path("kh2") is None:
            label = QLabel("KH2 game data has not been extracted in OpenKH Mods Manager.")
            grid.addWidget(label, 0, 0)
            return False
        else:
            return True

    def open_custom_visuals_folder(self):
        custom_visuals_path = appconfig.read_custom_visuals_path()
        if custom_visuals_path is None:
            show_alert(configui.CUSTOM_VISUALS_NOT_CHOSEN)
            if configui.custom_visuals_folder_getter():
                self.refresh_layout()
        else:
            folder_path = custom_visuals_path / self.folder_name
            folder_path.mkdir(parents=True, exist_ok=True)
            os.startfile(folder_path)

    def _configure_custom_visuals(self):
        if configui.custom_visuals_folder_getter():
            self.refresh_layout()

    def _configure_openkh(self):
        if configui.openkh_folder_getter():
            self.refresh_layout()

class CommandMenuViewerDialog(VisualsViewerDialog):

    def __init__(self, parent: Optional[QWidget]):
        self.custom_grid = QGridLayout()
        self.custom_grid.setVerticalSpacing(16)
        self.vanilla_grid = QGridLayout()
        self.vanilla_grid.setVerticalSpacing(16)

        super().__init__(parent, "Command Menus", CommandMenuRandomizer.directory_name())

        layout = self.scroll_layout
        layout.addWidget(KH2Submenu.make_styled_frame(self.custom_grid, 0, "Custom"))
        layout.addWidget(KH2Submenu.make_styled_frame(self.vanilla_grid, 1, "In-Game"))
        layout.addStretch(1)

    def refresh_layout(self):
        size = QSize(400, 200)
        columns = 2
        frame = True

        if self.require_custom_visuals(self.custom_grid):
            self.refresh_grid(self.custom_grid, CommandMenuRandomizer.collect_custom_images(), size, columns, frame)

        if self.require_extracted_data(self.vanilla_grid):
            self.refresh_grid(self.vanilla_grid, CommandMenuRandomizer.collect_vanilla_images(), size, columns, frame)


class ItempicViewerDialog(VisualsViewerDialog):

    def __init__(self, parent: Optional[QWidget]):
        self.no_custom_visuals_grid = QGridLayout()
        self.vertical_layout = QVBoxLayout()

        super().__init__(parent, "Item Pictures", ItempicRandomizer.directory_name())

        layout = self.scroll_layout
        layout.addLayout(self.no_custom_visuals_grid)
        layout.addLayout(self.vertical_layout)
        layout.addStretch(1)

    def refresh_layout(self):
        if self.require_custom_visuals(self.no_custom_visuals_grid):
            layout = self.vertical_layout
            clear_layout(layout)

            itempics = ItempicRandomizer.collect_custom_itempic_files(categorize=True)

            category_number = 0
            for category, category_items in itempics.items():
                grid = QGridLayout()

                row = 0
                column = 0
                for itempic in category_items:
                    with Image.open(itempic) as image:
                        itempic_label = QLabel()
                        itempic_label.setFixedSize(QSize(48, 48))
                        itempic_label.setPixmap(image.resize((48, 48)).toqpixmap())
                        grid.addWidget(itempic_label, row, column)

                    column = column + 1
                    if column == 10:
                        row = row + 1
                        column = 0

                header_style = category_number % len(header_styles)
                layout.addWidget(KH2Submenu.make_styled_frame(grid, header_style, category))

                category_number = category_number + 1


class RoomTransitionViewerDialog(VisualsViewerDialog):

    def __init__(self, parent: Optional[QWidget]):
        self.custom_grid = QGridLayout()
        self.vanilla_grid = QGridLayout()

        super().__init__(parent, "Room Transitions", RoomTransitionImageRandomizer.directory_name())

        layout = self.scroll_layout
        layout.addWidget(KH2Submenu.make_styled_frame(self.custom_grid, 0, "Custom"))
        layout.addWidget(KH2Submenu.make_styled_frame(self.vanilla_grid, 1, "In-Game"))
        layout.addStretch(1)

    def refresh_layout(self):
        size = QSize(96, 96)
        columns = 5

        if self.require_custom_visuals(self.custom_grid):
            custom_images = [image for image in RoomTransitionImageRandomizer.custom_room_transition_images().values()]
            self.refresh_grid(self.custom_grid, custom_images, size, columns)

        if self.require_extracted_data(self.vanilla_grid):
            self.refresh_grid(self.vanilla_grid, RoomTransitionImageRandomizer.collect_vanilla_images(), size, columns)


class EndingPictureViewerDialog(VisualsViewerDialog):

    def __init__(self, parent: Optional[QWidget]):
        self.custom_grid = QGridLayout()
        self.vanilla_grid = QGridLayout()

        super().__init__(parent, "Ending Pictures", EndingPictureRandomizer.directory_name())

        layout = self.scroll_layout
        layout.addWidget(KH2Submenu.make_styled_frame(self.custom_grid, 0, "Custom"))
        layout.addWidget(KH2Submenu.make_styled_frame(self.vanilla_grid, 1, "In-Game"))
        layout.addStretch(1)

    def refresh_layout(self):
        size = QSize(256, 256)
        columns = 3

        if self.require_custom_visuals(self.custom_grid):
            self.refresh_grid(self.custom_grid, EndingPictureRandomizer.collect_custom_endpics(), size, columns)

        if self.require_extracted_data(self.vanilla_grid):
            self.refresh_grid(self.vanilla_grid, EndingPictureRandomizer.collect_vanilla_endpics(), size, columns)
