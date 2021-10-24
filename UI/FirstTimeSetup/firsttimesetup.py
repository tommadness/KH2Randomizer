# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import (
    QMainWindow,
    QLabel, QLineEdit, QPushButton,
    QVBoxLayout,QHBoxLayout,QWidget,QStackedWidget,QFileDialog, QDialog
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

        self.firstPage = self.firstPage()
        self.pcsx2 = self.pcsx2Page()
        self.pcsx2Iso = self.pcsx2IsoPage()
        self.pcsx2GameData = self.pcsx2GameDataPage()
        self.pc = self.pcPage()


        self.pages = QStackedWidget()

        self.pages.addWidget(self.firstPage)
        self.pages.addWidget(self.pcsx2)
        self.pages.addWidget(self.pcsx2Iso)
        self.pages.addWidget(self.pcsx2GameData)
        self.pages.addWidget(self.pc)

        self.pages.currentChanged.connect(self.setConfig)

        self.pageLayout = QVBoxLayout()
        self.pageLayout.addWidget(self.pages)

        self.setLayout(self.pageLayout)


    def firstPage(self):
        mainLayout = QVBoxLayout()
        pageTitleLabel = self.pageTitle("Welcome to Kingdom Hearts 2: Final Mix Randomizer")

        pageContentLabel = QLabel()
        pageContentLabel.setText("This will guide you through setting up the Kingdom Hearts 2: Final Mix randomizer.\nPlease select your game edition below:")
        pageContentLabel.setWordWrap(True)


        buttonWidget = QWidget()
        buttonLayout = QHBoxLayout()

        pcsx2Button = QPushButton()
        pcsx2Button.setText("PCSX2")
        pcsx2Button.clicked.connect(self.goToPcsx2Page)

        pcButton = QPushButton()
        pcButton.setText("PC")
        pcButton.clicked.connect(self.goToPcPage)

        buttonLayout.addWidget(pcsx2Button)
        buttonLayout.addWidget(pcButton)

        buttonWidget.setLayout(buttonLayout)
        buttonWidget.setMaximumHeight(50)
        mainLayout.addWidget(pageTitleLabel)
        mainLayout.addWidget(pageContentLabel)
        mainLayout.addWidget(buttonWidget)

        widget = QWidget()
        widget.setLayout(mainLayout)
        widget.setObjectName("firstPage")
        return widget

    

    def pcsx2Page(self):
        widget = QWidget()
        layout = QVBoxLayout()

        pageTitleLabel = self.pageTitle("Select OpenKH Directory")

        pageContentLayout = QHBoxLayout()
        pageContentLayout.setObjectName("content")
        directoryBox = QLineEdit()
        directoryBox.setObjectName("OpenKHDir")
        directoryButton = QPushButton()
        directoryButton.setText("Choose Directory")
        directoryButton.clicked.connect(lambda: self.setPath(directoryBox, "Select OpenKH Directory"))
        pageContentLayout.addWidget(directoryBox)
        pageContentLayout.addWidget(directoryButton)

        pageContentWidget = QWidget()
        pageContentWidget.setLayout(pageContentLayout)

        navLayout = QHBoxLayout()
        nextButton = QPushButton()
        nextButton.setText("Next >")
        nextButton.setDisabled(True)
        nextButton.clicked.connect(self.goToNextPage)
        navLayout.addSpacing(400)
        navLayout.addWidget(nextButton)

        navWidget = QWidget()
        navWidget.setLayout(navLayout)
        navWidget.setMaximumHeight(50)

        directoryBox.textChanged.connect(lambda: self.checkCorrectPath(directoryBox,"OpenKh.Tools.ModsManager.exe", nextButton, "OpenKHDir"))

        layout.addWidget(pageTitleLabel)
        layout.addWidget(pageContentWidget)
        layout.addWidget(navWidget)
        widget.setLayout(layout)

        
        return widget

    def setConfig(self):
        content = self.pages.currentWidget().findChild(QLineEdit)
        if not content is None:
            configKey = content.objectName()
            if not self.config[configKey] is None:
                content.setText(self.config[configKey])

    def pageTitle(self, text):
        pageTitleLabel = QLabel()
        pageTitleLabel.setText(text)
        pageTitleLabel.setFont(self.titleFont)
        pageTitleLabel.setMaximumHeight(30)
        return pageTitleLabel

    def pcsx2IsoPage(self):
        page = QWidget()
        pageLayout = QVBoxLayout()

        pageTitleLabel = self.pageTitle("Select Kingdom Hearts 2: Final Mix ISO")
        pageLayout.addWidget(pageTitleLabel)

        pageContentWidget = QWidget()

        pageContentLayout = QHBoxLayout()
        directoryBox = QLineEdit()
        directoryBox.setObjectName("pcsx2Iso")
        directoryButton = QPushButton()
        directoryButton.setText("Choose File")
        directoryButton.clicked.connect(lambda: self.setFile(directoryBox, "Select Kingdom Hearts II: Final Mix ISO", "*.iso"))
        #self.setConfig(directoryBox, "pcsx2Iso")
        directoryBox.textChanged.connect(lambda: self.checkCorrectFile(directoryBox,self.KH2ISOMD5, nextButton, "pcsx2Iso"))
        pageContentLayout.addWidget(directoryBox)
        pageContentLayout.addWidget(directoryButton)

        pageContentWidget.setLayout(pageContentLayout)

        pageLayout.addWidget(pageContentWidget)

        navLayout = QHBoxLayout()
        nextButton = QPushButton()
        nextButton.setText("Next >")
        nextButton.setDisabled(True)
        nextButton.clicked.connect(self.goToNextPage)
        navLayout.addSpacing(400)
        navLayout.addWidget(nextButton)

        navWidget = QWidget()
        navWidget.setLayout(navLayout)
        navWidget.setMaximumHeight(50)

        pageLayout.addWidget(navWidget)



        page.setLayout(pageLayout)


        return page

    def pcsx2GameDataPage(self):
        widget = QWidget()
        layout = QVBoxLayout()

        pageTitleLabel = self.pageTitle("Select Game Data Location")

        pageContentLayout = QHBoxLayout()
        pageContentLayout.setObjectName("content")
        directoryBox = QLineEdit()
        directoryBox.setObjectName("pcsx2GameData")
        directoryButton = QPushButton()
        directoryButton.setText("Choose Directory")
        directoryButton.clicked.connect(lambda: self.setPath(directoryBox, "Select Game Data"))
        pageContentLayout.addWidget(directoryBox)
        pageContentLayout.addWidget(directoryButton)

        pageContentWidget = QWidget()
        pageContentWidget.setLayout(pageContentLayout)

        navLayout = QHBoxLayout()
        nextButton = QPushButton()
        nextButton.setText("Close")
        nextButton.setDisabled(True)
        nextButton.clicked.connect(lambda: self.close())
        navLayout.addSpacing(400)
        navLayout.addWidget(nextButton)

        navWidget = QWidget()
        navWidget.setLayout(navLayout)
        navWidget.setMaximumHeight(50)

        directoryBox.textChanged.connect(lambda: self.checkCorrectPath(directoryBox,"03system.bin", nextButton, "pcsx2GameData"))

        layout.addWidget(pageTitleLabel)
        layout.addWidget(pageContentWidget)
        layout.addWidget(navWidget)
        widget.setLayout(layout)

        return widget

    def pcPage(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel()
        label.setText("PC")
        layout.addWidget(label)
        widget.setLayout(layout)
        return widget

    def goToPcsx2Page(self):
        self.pages.setCurrentWidget(self.pcsx2)

    def goToPcPage(self):
        self.pages.setCurrentWidget(self.pc)

    def goToNextPage(self):
        self.pages.setCurrentIndex(self.pages.currentIndex()+1)

    def setPath(self, textBox, title):
        path = str(QFileDialog.getExistingDirectory(self, title))
        textBox.setText(path)

    def setFile(self, textBox, title, filter):
        path = QFileDialog.getOpenFileName(self, title, filter=filter)[0]
        print(path)
        textBox.setText(path)

    def checkCorrectPath(self, path, fileName, nextButton,configKey):
        file = Path(path.text()+"\\"+fileName)
        print(file)
        if file.is_file():
            self.config[configKey] = str(path.text())
            nextButton.setDisabled(False)
            print(self.config)

    def checkCorrectFile(self,path,md5,nextButton,configKey):
        if configKey+"Valid" in self.config.keys() and self.config[configKey+"Valid"] == True:
            nextButton.setDisabled(False)
            return
        print(path.text())
        alert = Alert("Validating file", "Making sure this is the correct file")
        inputMD5 = hashlib.md5(open(path.text(),'rb').read()).hexdigest().upper()
        alert = None
        print(inputMD5)
        if inputMD5 == md5:
            self.config[configKey] = str(path.text())
            self.config[configKey+"Valid"] = True
            nextButton.setDisabled(False)
            print(self.config)

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

