import os
from pathlib import Path
import subprocess
import sys

from PySide6 import QtGui
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QListWidget, QPushButton, QPlainTextEdit

from Module.resources import resource_path
from UI import theme
from UI.GithubInfo.releaseInfo import GithubReleaseInfo, KH2RandomizerGithubReleases

class KH2RandoUpdater(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KH2 Randomizer Seed Generator Updater")
        self.setWindowIcon(QIcon(resource_path("Module/icon.png")))
        releases = KH2RandomizerGithubReleases()
        self.updates = releases.get_update_infos()
        grid = QGridLayout()
        if len(self.updates)==0:
            label = QLabel("No new updates. You are up to date.")
            grid.addWidget(label,0,0)
        else:
            # loop through updates, putting most up to date at the top
            self.update_list_widget = QListWidget(self)
            self.patch_notes = QPlainTextEdit(self)
            for update_info in self.updates:
                self.update_list_widget.addItem(str(update_info.version))
            self.update_list_widget.itemSelectionChanged.connect(self.update_patch_notes)
            self.update_list_widget.setCurrentRow(0)

            download_button = QPushButton("Download Selected Update")
            download_button.clicked.connect(self.download_selected_update)

            grid.addWidget(self.update_list_widget, 0, 0)
            grid.addWidget(self.patch_notes, 0, 1)
            grid.addWidget(download_button, 1, 0)

        widget = QWidget()
        widget.setLayout(grid)
        self.setCentralWidget(widget)
    
    def update_patch_notes(self):
        for index in self.update_list_widget.selectedIndexes():
            self.patch_notes.setPlainText(self.updates[index.row()].notes)
    
    def download_selected_update(self):
        for index in self.update_list_widget.selectedIndexes():
            update_info : GithubReleaseInfo = self.updates[index.row()]
            result = update_info.download_release()
            if result:
                process = subprocess.Popen("KH2 Randomizer.exe")
                sys.exit()
    


if __name__=="__main__":
    app = QApplication([])
    QtGui.QFontDatabase.addApplicationFont(resource_path('static/KHMenu.otf'))
    window = KH2RandoUpdater()
    stylesheet = app.styleSheet()
    with open(resource_path('UI/stylesheet.css')) as file:
        css_resources = {
            "background-primary": theme.BackgroundPrimary,
            "background-dark": theme.BackgroundDark,
            "link-color": theme.LinkColor,
            "selection-color": theme.SelectionColor,
            "selection-border-color": theme.SelectionBorderColor,
            "ability-on": Path(resource_path("static/icons/misc/ability-on.png")).as_posix(),
            "down-arrow": Path(resource_path("static/icons/misc/arrow-down.png")).as_posix(),
            "up-arrow": Path(resource_path("static/icons/misc/arrow-up.png")).as_posix(),
        }
        app.setStyleSheet((stylesheet + file.read().format(**os.environ)) % css_resources)
    window.show()
    sys.exit(app.exec())
