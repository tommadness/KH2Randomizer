from typing import Optional

from PySide6.QtGui import QPixmap, QIcon, Qt
from PySide6.QtWidgets import QDialog, QWidget, QVBoxLayout, QLabel

from Module.resources import resource_path
from Module.version import LOCAL_UI_VERSION
from UI import theme


class AboutDialog(QDialog):

    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent)

        self.setWindowTitle("About")
        self.setWindowIcon(QIcon(resource_path("Module/icon.png")))

        header_label = QLabel()
        header_label.setPixmap(QPixmap(resource_path("static/icons/misc/randomizer-header.png")))

        aboutText = f'''
        Kingdom Hearts II Randomizer Seed Generator<br>
        Version {LOCAL_UI_VERSION}<br>
        Created by Equations19, Thundrio, Tommadness, and ZakTheRobot<br><br>

        Thank you to all contributors, testers, and advocates.<br><br><br>


        Randomizer Information<br><br>
        <a href="https://tommadness.github.io/KH2Randomizer" style="color: {theme.LinkColor}">Website</a><br>
        <a href="https://github.com/tommadness/KH2Randomizer" style="color: {theme.LinkColor}">GitHub</a><br>
        <a href="https://discord.gg/KH2FMRando" style="color: {theme.LinkColor}">Discord</a><br>
        <a href="https://github.com/tommadness/KH2Randomizer#acknowledgements" style="color: {theme.LinkColor}">Acknowledgements</a><br><br>
        '''
        message = QLabel(aboutText)
        message.setTextFormat(Qt.RichText)
        message.setTextInteractionFlags(Qt.TextBrowserInteraction)
        message.setOpenExternalLinks(True)

        layout = QVBoxLayout()
        layout.addWidget(header_label, alignment=Qt.AlignHCenter)
        layout.addWidget(message)
        self.setLayout(layout)
