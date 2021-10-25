# This Python file uses the following encoding: utf-8
import sys
from PySide6 import QtGui
from PySide6 import QtWidgets
from PySide6.QtWidgets import (
    QMainWindow,
    QLabel, QLineEdit, QPushButton,
    QTextEdit,
    QVBoxLayout,QHBoxLayout,QWidget,QStackedWidget,QFileDialog, QDialog, QGridLayout
)

from pathlib import Path
import hashlib

from PySide6.QtGui import QFont


class FirstTimeSetup(QDialog):

    KH2ISOMD5 = "1BD351E1DF9FC5D783D8318010D17F03"

    def __init__(self, config):
        super().__init__()

        self.config = config


        w = 600
        h = 400

        self.titleFont = QFont("MS Shell Dlg 2", 16)
        self.titleFont.setBold(True)

        self.setWindowTitle("First Time Setup")
        self.setFixedSize(w,h)

        self.pages = QStackedWidget()
        firstPage = self.basePage(title="Welcome to Kingdom Hearts II: Final Mix Randomizer", description="Please select a game version to setup.")
        firstPage.layout().addWidget(self.validationField("OpenKH Location"))


        pcsx2Page = self.basePage(title="Setup PCSX2", description="Set location of files required for PCSX2 Randomizer")
        isoField = self.validationField("ISO Location")
        pcsx2GameDataField = self.validationField("Game Data Location")
        pcsx2Page.layout().addWidget(isoField)
        pcsx2Page.layout().addWidget(pcsx2GameDataField)

        pcPage = self.basePage(title="Setup PC", description="Set location of files required for PC Randomizer")
        pcPage.layout().addWidget(self.validationField("Game Install Location"))
        pcPage.layout().addWidget(self.validationField("Game Data Location"))

        self.pages.addWidget(firstPage)
        self.pages.addWidget(pcsx2Page)
        self.pages.addWidget(pcPage)

        pcsx2Button = QPushButton(text="PCSX2")
        pcsx2Button.clicked.connect(lambda pcsx2Page=pcsx2Page, pages=self.pages: pages.setCurrentWidget(pcsx2Page))

        pcButton = QPushButton(text="PC")
        pcButton.clicked.connect(lambda pcPage=pcPage, pages=self.pages: pages.setCurrentWidget(pcPage))

        navWidget = QWidget()
        nav = QHBoxLayout(navWidget)
        nav.addWidget(pcsx2Button)
        nav.addWidget(pcButton)
        firstPage.layout().addWidget(navWidget)





        self.pageLayout = QVBoxLayout()
        self.pageLayout.addWidget(self.pages)

        self.setLayout(self.pageLayout)

    def basePage(self, title, description):
        page = QWidget()
        layout = QVBoxLayout()
        titleLabel = QLabel(title)
        titleLabel.setFont(self.titleFont)
        titleLabel.setMaximumHeight(20)
        layout.addWidget(titleLabel)
        layout.addWidget(QLabel(description))
        page.setLayout(layout)
        return page

    def validationField(self, label, type="Folder", disabled=False):
        widget = QWidget()

        layout = QGridLayout(widget)
        layout.addWidget(QLabel(label),1,1)
        
        textBox = QLineEdit()
        textBox.setReadOnly(True)
        textBox.setMaximumHeight(20)
        textBox.setDisabled(disabled)
        textBox.setValidator(ValidatePath("BaseDailySeed.json"))
        layout.addWidget(textBox,2,1)

        button = QPushButton("Browse")
        button.setDisabled(disabled)
        if type=="Folder":
            button.clicked.connect(lambda label=label, textBox=textBox: self.selectFolder(label, textBox))
        layout.addWidget(button,2,2)

        return widget

    def selectFolder(self, title, textBox):
        path = str(QFileDialog.getExistingDirectory(self, title))
        textBox.setText(path)
        
        pass

class ValidatePath(QtGui.QValidator):
    def __init__(self, contains):
        super().__init__()
        self.contains=contains

    def validate(self, input, int):
        if Path(input).is_dir() and Path(input+"/{contains}".format(contains=self.contains)).is_file():
            return QtGui.QValidator.Acceptable
        return QtGui.QValidator.Invalid
