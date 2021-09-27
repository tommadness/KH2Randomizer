from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget,QLabel,QVBoxLayout,QHBoxLayout,QGridLayout

class KH2Submenu(QWidget):
    def __init__(self,in_layout="vertical"):
        super().__init__()
        self.categoryData = {}
        if in_layout=="vertical":
            self.menulayout = QVBoxLayout()
        if in_layout=="horizontal":
            self.menulayout = QHBoxLayout()
        if in_layout=="grid":
            self.menulayout = QGridLayout()

    def addOption(self,label_text,option,option_layout="horizontal",grid_pos=None):
        if option_layout=="horizontal":
            layout = QHBoxLayout()
        if option_layout=="vertical":
            layout = QVBoxLayout()
        layout.addWidget(QLabel(label_text))
        layout.addWidget(option,alignment=Qt.AlignCenter)
        if grid_pos is not None:
            self.menulayout.addLayout(layout, grid_pos[0], grid_pos[1], alignment=Qt.AlignCenter)
        else:
            self.menulayout.addLayout(layout)

    def addHeader(self,label_text):
        self.menulayout.addWidget(QLabel(f"<h3>{label_text}</h3>"))

    def finalizeMenu(self):
        self.setLayout(self.menulayout)

    def setKeyValue(self,name,value):
        print(f"{name} : {value}")
        self.categoryData[name]=value

    def getKeyValue(self,name):
        return self.categoryData[name]

    def getName(self):
        return self.name

    def getData(self):
        return self.categoryData

    def setData(self,inData):
        for key in inData:
            if key in self.categoryData:
                self.setKeyValue(key,inData[key])
            else:
                print(f"Trying to assign {key} to the {self.name} submenu category")
