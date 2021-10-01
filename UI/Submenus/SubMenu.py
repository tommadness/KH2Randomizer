from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget,QLabel,QVBoxLayout,QHBoxLayout,QGridLayout

from PySide6.QtWidgets import QPushButton,QCheckBox,QComboBox,QSpinBox,QDoubleSpinBox,QListWidget,QRadioButton

class KH2Submenu(QWidget):
    def __init__(self,in_layout="vertical"):
        super().__init__()
        self.categoryData = {}
        self.flagOptions = {}
        self.widgetList = []
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
        self.widgetList.append(option)
        if grid_pos is not None:
            self.menulayout.addLayout(layout, grid_pos[0], grid_pos[1], alignment=Qt.AlignCenter)
        else:
            self.menulayout.addLayout(layout)

    def addFlagOption(self,option,data_entry):
        if isinstance(option,QPushButton):
            self.flagOptions[data_entry] = {"type":"bool"}
        elif isinstance(option,QCheckBox):
            self.flagOptions[data_entry] = {"type":"bool"}
        elif isinstance(option,QComboBox):
            self.flagOptions[data_entry] = {"type":"select","options":[option.itemText(i) for i in range(option.count())]}
        elif isinstance(option,QSpinBox):
            self.flagOptions[data_entry] = {"type":"spin","min":option.minimum(),"max":option.maximum(),"step":option.singleStep()}
        elif isinstance(option,QDoubleSpinBox):
            self.flagOptions[data_entry] = {"type":"spin","min":option.minimum(),"max":option.maximum(),"step":option.singleStep()}
        elif isinstance(option,QListWidget):
            self.flagOptions[data_entry] = {"type":"multiselect","options":[option.item(i).text() for i in range(option.count())]}
        elif isinstance(option,QRadioButton):
            self.flagOptions[data_entry] = {"type":"bool"}
        else:
            print(f"Error creating flag options for {self.name} {data_entry}")

    def addHeader(self,label_text):
        self.menulayout.addWidget(QLabel(f"<h3>{label_text}</h3>"))

    def finalizeMenu(self):
        self.setLayout(self.menulayout)

    def setKeyValue(self,name,value):
        self.categoryData[name]=value

    def getKeyValue(self,name):
        return self.categoryData[name]

    def getName(self):
        return self.name

    def getData(self):
        return self.categoryData

    def updateWidgets(self):
        pass

    def setData(self,inData):
        for key in inData:
            if key in self.categoryData:
                self.setKeyValue(key,inData[key])
            else:
                print(f"Trying to assign {key} to the {self.name} submenu category")
        self.updateWidgets()

    def getFlagOptions(self):
        return self.flagOptions

