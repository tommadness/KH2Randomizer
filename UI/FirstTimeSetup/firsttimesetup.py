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
import yaml

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
        
        pcsx2Page = self.basePage(title="Setup PCSX2", description="Set location of files required for PCSX2 Randomizer")
        pcsx2Page.layout().addWidget(self.validationField("OpenKH Location",type="Folder"))
        pcsx2Page.layout().addWidget(self.validationField("ISO Location", disabled=True))
        pcsx2Page.layout().addWidget(self.validationField("Game Data Location", disabled=True))

        pcPage = self.basePage(title="Setup PC", description="Set location of files required for PC Randomizer")
        pcPage.layout().addWidget(self.validationField("OpenKH Location",type="Folder"))
        pcPage.layout().addWidget(self.validationField("Game Install Location", disabled=True))
        pcPage.layout().addWidget(self.validationField("Game Data Location", disabled=True))

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

    def validationField(self, label, type="Folder", validate=lambda: print("Changed"), disabled=False):
        widget = QWidget()

        layout = QGridLayout(widget)
        layout.addWidget(QLabel(label),1,1)
        
        textBox = QLineEdit()
        textBox.setMaximumHeight(20)
        textBox.setDisabled(disabled)
        textBox.textChanged.connect(lambda: validate())
        layout.addWidget(textBox,2,1)

        button = QPushButton("Browse")
        button.setDisabled(disabled)
        if type=="Folder":
            button.clicked.connect(lambda label=label, textBox=textBox: self.selectFolder(label, textBox))
        layout.addWidget(button,2,2)

        return widget

    def validatePath(self, path, validFile, onSuccess, onFailure):
        
        pass

    def validateFile(self,path,md5, onSuccess, onFailure):
        pass

    def selectFolder(self, title, textBox):
        path = str(QFileDialog.getExistingDirectory(self, title))
        textBox.setText(path)
        
        pass

class Alert(QMainWindow):
    def __init__(self, title, message):
        super().__init__()
        self.setWindowTitle(title)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(message))
        self.setLayout(layout)
        self.show()

    def closeEvent(self, event):
        event.ignore()

