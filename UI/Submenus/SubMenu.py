from PySide6.QtWidgets import QWidget,QLabel,QVBoxLayout,QHBoxLayout

class KH2Submenu(QWidget):
    def __init__(self):
        super().__init__()
        self.categoryData = {}
        self.menulayout = QVBoxLayout()

    def addOption(self,label_text,option):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label_text))
        layout.addWidget(option)
        self.menulayout.addLayout(layout)

    def addHeader(self,label_text):
        self.menulayout.addWidget(QLabel(f"<h3>{label_text}</h3>"))

    def finalizeMenu(self):
        self.setLayout(self.menulayout)

    def setKeyValue(self,name,value):
        self.categoryData[name]=value

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
