# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QLineEdit, QPushButton, 
    QTabWidget,QVBoxLayout,QHBoxLayout,QWidget,QStackedWidget,QFileDialog,QTextEdit
)
from pathlib import Path

from PySide6.QtGui import QFont


class FirstTimeSetup(QMainWindow):
    def __init__(self):
        super().__init__()
        w = 600
        h = 400

        self.titleFont = QFont("MS Shell Dlg 2", 16)
        self.titleFont.setBold(True)

        self.setWindowTitle("First Time Setup")
        self.setFixedSize(w,h)

        self.firstPage = self.firstPage()
        self.pcsx2 = self.pcsx2Page()
        self.pc = self.pcPage()


        self.pages = QStackedWidget()

        self.pages.addWidget(self.firstPage)
        self.pages.addWidget(self.pcsx2)
        self.pages.addWidget(self.pc)

        self.setCentralWidget(self.pages)

    def firstPage(self):
        mainLayout = QVBoxLayout()
        pageTitleLabel = QLabel()
        pageTitleLabel.setText("Welcome to Kingdom Hearts 2: Final Mix Randomizer")
        pageTitleLabel.setMaximumHeight(30)
        pageTitleLabel.setFont(self.titleFont)

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

    




        # configFile = open("rando-config.yml","w")
        # configFile.write("Test")
        # configFile.close()

    def pcsx2Page(self):
        widget = QWidget()
        layout = QVBoxLayout()

        pageTitleLabel = QLabel()
        pageTitleLabel.setText("Select OpenKH Directory")
        pageTitleLabel.setFont(self.titleFont)
        pageTitleLabel.setMaximumHeight(30)

        pageContentLayout = QHBoxLayout()
        directoryBox = QLineEdit()
        directoryButton = QPushButton()
        directoryButton.setText("Choose Directory")
        directoryButton.clicked.connect(lambda: self.setPath(directoryBox, "Select OpenKH Directory"))
        pageContentLayout.addWidget(directoryBox)
        pageContentLayout.addWidget(directoryButton)

        pageContentWidget = QWidget()
        pageContentWidget.setLayout(pageContentLayout)
        pageContentWidget.setMaximumHeight(45)

        navLayout = QHBoxLayout()
        nextButton = QPushButton()
        nextButton.setText("Next >")
        nextButton.setDisabled(True)
        navLayout.addWidget(nextButton)
        navWidget = QWidget()
        navWidget.setLayout(navLayout)

        directoryBox.textChanged.connect(lambda: self.checkCorrectPath(directoryBox,"OpenKh.Tools.ModsManager.exe", nextButton))

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

    def setPath(self, textBox, title):
        path = str(QFileDialog.getExistingDirectory(self, title))
        textBox.setText(path)

    def checkCorrectPath(self, path, fileName, nextButton):
        file = Path(path.text()+"\\"+fileName)
        print(file)
        if file.is_file():

            nextButton.setDisabled(False)
