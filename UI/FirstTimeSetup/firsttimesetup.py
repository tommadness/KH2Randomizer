# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QLineEdit, QPushButton, 
    QTabWidget,QVBoxLayout,QHBoxLayout,QWidget
)

from PySide6.QtGui import QFont


class FirstTimeSetup(QMainWindow):
    def __init__(self):
        super().__init__()
        w = 600
        h = 400

        titleFont = QFont("MS Shell Dlg 2", 16)
        titleFont.setBold(True)

        self.setWindowTitle("First Time Setup")
        self.setFixedSize(w,h)

        mainLayout = QVBoxLayout()
        pageTitleLabel = QLabel()
        pageTitleLabel.setText("Welcome to Kingdom Hearts 2: Final Mix Randomizer")
        pageTitleLabel.setMaximumHeight(30)
        pageTitleLabel.setFont(titleFont)

        pageContentLabel = QLabel()
        pageContentLabel.setText("This will guide you through setting up the Kingdom Hearts 2: Final Mix randomizer.\nPlease select your game edition below:")
        pageContentLabel.setWordWrap(True)


        buttonWidget = QWidget()
        buttonLayout = QHBoxLayout()
        pcsx2Button = QPushButton()
        pcsx2Button.setText("PCSX2")
        pcButton = QPushButton()
        pcButton.setText("PC")

        buttonLayout.addWidget(pcsx2Button)
        buttonLayout.addWidget(pcButton)

        buttonWidget.setLayout(buttonLayout)
        buttonWidget.setMaximumHeight(50)


        widget = QWidget()

        mainLayout.addWidget(pageTitleLabel)
        mainLayout.addWidget(pageContentLabel)
        mainLayout.addWidget(buttonWidget)

        widget.setLayout(mainLayout)

        self.setCentralWidget(widget)




        # configFile = open("rando-config.yml","w")
        # configFile.write("Test")
        # configFile.close()

