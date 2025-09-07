import os
from typing import Optional

from PIL import Image
from PySide6.QtCore import QSize
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QDialog, QMenuBar, QMenu, QVBoxLayout, QWidget, QGridLayout, QLabel, QScrollArea, \
    QFileDialog

from Class.seedSettings import SeedSettings
from Module import appconfig
from Module.cosmeticsmods.keyblade import KeybladeRandomizer, ReplacementKeyblade
from UI import theme, configui
from UI.Submenus.KeybladePackageDialog import KeybladePackageDialog
from UI.Submenus.SubMenu import KH2Submenu
from UI.keybladeworker import ExtractVanillaKeybladesWorker, ImportCustomKeybladesWorker
from UI.qtlib import button, clear_layout, show_alert


class ManageKeybladesDialog(QDialog):

    def __init__(self, parent: Optional[QWidget], settings: SeedSettings):
        super().__init__(parent)
        self.settings = settings

        self.setWindowTitle("Manage Keyblades")

        menu_bar = QMenuBar()
        file_menu = QMenu("File")
        file_menu.addAction("Open Custom Keyblades Folder", self._open_custom_keyblades_folder)

        import_menu = QMenu("Import")
        import_menu.addAction("Add Keyblade(s) from .kh2randokb Files", self._import_keyblades)

        create_menu = QMenu("Create")
        create_menu.addAction("Create .kh2randokb File", self._show_keyblade_packager)

        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(import_menu)
        menu_bar.addMenu(create_menu)

        main = QVBoxLayout()
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(menu_bar)

        grid_scroll = QScrollArea()
        grid_widget = QWidget()
        grid_scroll.setWidget(grid_widget)
        grid_scroll.setWidgetResizable(True)

        custom_grid = QGridLayout()
        custom_grid.setHorizontalSpacing(4)
        self.custom_grid = custom_grid

        vanilla_grid = QGridLayout()
        vanilla_grid.setHorizontalSpacing(4)
        self.vanilla_grid = vanilla_grid

        scroll_layout = QVBoxLayout()
        scroll_layout.addWidget(KH2Submenu.make_styled_frame(custom_grid, 0, "Custom"))
        scroll_layout.addWidget(KH2Submenu.make_styled_frame(vanilla_grid, 1, "In-Game"))
        scroll_layout.addStretch(stretch=1)
        grid_widget.setLayout(scroll_layout)
        main.addWidget(grid_scroll)

        self.setLayout(main)
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        self._refresh_custom_section()
        self._refresh_vanilla_section()

    def _refresh_custom_section(self):
        custom_grid = self.custom_grid
        clear_layout(custom_grid)
        if appconfig.read_custom_visuals_path() is None:
            label = QLabel(configui.CUSTOM_VISUALS_NOT_CHOSEN)
            configure_button = button("Configure", self._configure_custom_visuals)
            self.custom_grid.addWidget(label, 0, 0)
            self.custom_grid.addWidget(configure_button, 1, 0)
        else:
            self._refresh_keyblade_info(custom_grid, KeybladeRandomizer.collect_custom_keyblades())

    def _refresh_vanilla_section(self):
        vanilla_grid = self.vanilla_grid
        clear_layout(vanilla_grid)
        vanilla_keyblades = KeybladeRandomizer.collect_vanilla_keyblades()
        if not vanilla_keyblades:
            label = QLabel("Vanilla keyblades have not been extracted.")
            extract_button = button("Extract Vanilla Keyblades", self._extract_vanilla_keyblades)
            vanilla_grid.addWidget(label, 0, 0)
            vanilla_grid.addWidget(extract_button, 1, 0)
        else:
            self._refresh_keyblade_info(vanilla_grid, vanilla_keyblades)

    @staticmethod
    def _refresh_keyblade_info(grid: QGridLayout, keyblades: list[ReplacementKeyblade]):
        row = 0
        for keyblade in keyblades:
            itempic = keyblade.remastered_itempic()
            itempic_label = QLabel("")
            itempic_label.setFixedSize(QSize(48, 48))
            if itempic:
                with Image.open(itempic) as image:
                    itempic_label.setPixmap(image.resize((48, 48)).toqpixmap())

            name_label = QLabel(keyblade.name)
            author_label = QLabel(keyblade.author)

            if keyblade.source:
                source_label = QLabel(f'<a href="{keyblade.source}" style="color: {theme.LinkColor}">Source</a>')
                source_label.setTextFormat(Qt.RichText)
                source_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
                source_label.setOpenExternalLinks(True)
            else:
                source_label = QLabel("")

            grid.addWidget(itempic_label, row, 0)
            grid.addWidget(name_label, row, 1)
            grid.addWidget(author_label, row, 2)
            grid.addWidget(source_label, row, 3)

            row = row + 1

    def _open_custom_keyblades_folder(self):
        custom_visuals_path = appconfig.read_custom_visuals_path()
        if custom_visuals_path is None:
            show_alert(configui.CUSTOM_VISUALS_NOT_CHOSEN)
            if configui.custom_visuals_folder_getter():
                self._refresh_custom_section()
        else:
            keyblades_path = custom_visuals_path / KeybladeRandomizer.directory_name()
            keyblades_path.mkdir(parents=True, exist_ok=True)
            os.startfile(keyblades_path)

    def _configure_custom_visuals(self):
        if configui.custom_visuals_folder_getter():
            self._refresh_custom_section()

    def _extract_vanilla_keyblades(self):
        worker = ExtractVanillaKeybladesWorker()
        worker.finished.connect(self._refresh_vanilla_section)
        worker.start()

    def _show_keyblade_packager(self):
        KeybladePackageDialog(self, self.settings).exec()

    def _import_keyblades(self):
        file_dialog = QFileDialog(self)
        outfile_names, _ = file_dialog.getOpenFileNames(self, filter="Randomizer Keyblades (*.kh2randokb)")
        if len(outfile_names) > 0:
            worker = ImportCustomKeybladesWorker(keyblade_file_paths=outfile_names)
            worker.finished.connect(self._refresh_custom_section)
            worker.start()
        else:
            show_alert("No keyblades selected.", title="Import Keyblade(s)")
