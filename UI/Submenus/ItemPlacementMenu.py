from Submenus.SubMenu import KH2Submenu
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox,QRadioButton,QButtonGroup,QComboBox

class ItemPlacementMenu(KH2Submenu):
    def __init__(self):
        super().__init__()
        self.name="Item Placement Options"

        promiseCharm = QCheckBox()
        promiseCharm.stateChanged.connect(lambda state : self.setKeyValue("PromiseCharm",state==Qt.Checked))
        promiseCharm.setCheckState(Qt.Checked)
        promiseCharm.setCheckState(Qt.Unchecked)
        self.addOption("Enable Promise Charm",promiseCharm)

        itemDifficulty = QComboBox()
        itemDifficulty.addItems(["Super Easy","Easy","Normal","Hard","Very Hard","Insane","Nightmare"])
        itemDifficulty.currentTextChanged.connect(lambda txt : self.setKeyValue("itemPlacementDifficulty",txt))
        itemDifficulty.setCurrentIndex(2)
        self.addOption("Item Placement Difficulty",itemDifficulty)

        maxLogic = QCheckBox()
        maxLogic.stateChanged.connect(lambda state : self.setKeyValue("Max Logic Item Placement",state==Qt.Checked))
        maxLogic.setCheckState(Qt.Checked)
        maxLogic.setCheckState(Qt.Unchecked)
        self.addOption("Max Logic Item Placement",maxLogic)

        reverseRando = QCheckBox()
        reverseRando.stateChanged.connect(lambda state : self.setKeyValue("Reverse Rando",state==Qt.Checked))
        reverseRando.setCheckState(Qt.Checked)
        reverseRando.setCheckState(Qt.Unchecked)
        self.addOption("Reverse Rando",reverseRando)

        self.addHeader("Ability Pool")

        defaultAbilities = QRadioButton()
        defaultAbilities.toggled.connect(lambda : self.setKeyValue("Randomize Ability Pool",randomAbilities.isChecked()))
        self.addOption("Default Abilities",defaultAbilities)

        randomAbilities = QRadioButton()
        self.addOption("Randomize Ability Pool",randomAbilities)
        randomAbilities.toggled.connect(lambda : self.setKeyValue("Randomize Ability Pool",randomAbilities.isChecked()))

        abilityGroup = QButtonGroup()
        abilityGroup.addButton(defaultAbilities)
        abilityGroup.addButton(randomAbilities)

        defaultAbilities.toggle()


        self.finalizeMenu()

    def updateWidgets(self):
        self.widgetList[0].setCheckState(Qt.Checked if self.getKeyValue("PromiseCharm") else Qt.Unchecked)
        self.widgetList[1].setCurrentText(self.getKeyValue("itemPlacementDifficulty"))
        self.widgetList[2].setCheckState(Qt.Checked if self.getKeyValue("Max Logic Item Placement") else Qt.Unchecked)
        self.widgetList[3].setCheckState(Qt.Checked if self.getKeyValue("Reverse Rando") else Qt.Unchecked)

        if self.getKeyValue("Randomize Ability Pool"):
            self.widgetList[5].toggle()
        else:
            self.widgetList[4].toggle()


