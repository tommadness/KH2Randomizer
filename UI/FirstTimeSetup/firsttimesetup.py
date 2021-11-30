# This Python file uses the following encoding: utf-8
import sys
from PySide6 import QtGui, QtCore
from PySide6 import QtWidgets
from PySide6.QtWidgets import (
    QDialogButtonBox,
    QMainWindow,
    QLabel, QLineEdit, QPushButton,
    QTextEdit,
    QVBoxLayout,QHBoxLayout,QWidget,QStackedWidget,QFileDialog, QDialog, QGridLayout
)

from pathlib import Path
import hashlib

from Class.downloader import Downloader

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

        navWidget = QWidget()
        nav = QHBoxLayout(navWidget)
        pcsx2Button = QPushButton(text="PCSX2")
        pcButton = QPushButton(text="PC")
        nav.addWidget(pcsx2Button)
        nav.addWidget(pcButton)

        firstPage.layout().addWidget(self.validationField("OpenKH Location", validFileName="OpenKh.Tools.ModsManager.exe", download=Downloader.openKHDownload))




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

        pcsx2Button.clicked.connect(lambda pcsx2Page=pcsx2Page, pages=self.pages: pages.setCurrentWidget(pcsx2Page))

        pcButton.clicked.connect(lambda pcPage=pcPage, pages=self.pages: pages.setCurrentWidget(pcPage))


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

    def validationField(self, label, onValid=lambda: print("Lambda Not Passed"), validFileName=None, type="Folder", disabled=False, download=None):
        widget = QWidget()

        layout = QGridLayout(widget)
        layout.addWidget(QLabel(label),1,1)
        
        textBox = QLineEdit()
        textBox.setReadOnly(True)
        textBox.setMaximumHeight(20)
        textBox.setDisabled(disabled)
        textBox.setValidator(ValidatePath(validFileName, download=download))
        layout.addWidget(textBox,2,1)

        button = QPushButton("Browse")
        button.setDisabled(disabled)
        if type=="Folder":
            button.clicked.connect(lambda label=label, textBox=textBox: self.selectFolder(label, textBox))
        layout.addWidget(button,2,2)
        textBox.editingFinished.connect(lambda: onValid())

        return widget

    def selectFolder(self, title, textBox):
        path = str(QFileDialog.getExistingDirectory(self, title))
        textBox.setText(path)
        
        pass


class ValidatePath(QtGui.QValidator):
    def __init__(self, contains, download=None):
        super().__init__()
        self.contains = contains
        self.download = download
        self.downloadPrompted = False

    def validate(self, input, int):
        if Path(input).is_dir() and Path(input+"/{contains}".format(contains=self.contains)).is_file():
            return QtGui.QValidator.Acceptable

        if not self.downloadPrompted and not self.download == None:
            dialog = QDialog()
            dialog.setWindowTitle("Download")
            layout = QVBoxLayout()
            label = QLabel("{downloadName} will be downloaded to\r\n{input}".format(input=input, downloadName=self.download["name"]))
            label.setWordWrap(True)
            buttonBox = QDialogButtonBox(QDialogButtonBox.Ok, QtCore.Qt.Horizontal)
            buttonBox.addButton(QDialogButtonBox.Cancel)
            buttonBox.accepted.connect(lambda: dialog.accept())
            buttonBox.rejected.connect(lambda: dialog.reject())
            layout.addWidget(label)
            layout.addWidget(buttonBox)
            dialog.setLayout(layout)
            dialog.setFixedSize(400,100)
            self.downloadPrompted = True

            if dialog.exec():
                try:
                    Downloader(self.download["url"]).downloadZip(input)
                except:
                    print("Download Failed")
                    return QtGui.QValidator.Invalid
                return QtGui.QValidator.Acceptable
            else:
                return QtGui.QValidator.Invalid

        else:
            return QtGui.QValidator.Invalid

