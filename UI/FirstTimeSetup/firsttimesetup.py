# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QLineEdit, QPushButton, 
    QTabWidget,QVBoxLayout,QHBoxLayout,QWidget
)


class FirstTimeSetup(QMainWindow):
    def __init__(self):
        super().__init__()
        w = 600
        h = 400
        self.setWindowTitle("First Time Setup")
        self.setFixedSize(w,h)
        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        configFile = open("rando-config.yml","w")
        configFile.write("Test")
        configFile.close()

