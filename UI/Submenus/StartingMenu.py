from Submenus.SubMenu import KH2Submenu
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox,QListWidget 

class StartingMenu(KH2Submenu):
    def __init__(self):
        super().__init__()
        self.name="Starting Items"
        self.addHeader("Rewards in Starting Areas")

        critBonuses = QCheckBox()
        critBonuses.stateChanged.connect(lambda state : self.setKeyValue("critBonuses",state==Qt.Checked))
        critBonuses.setCheckState(Qt.Checked)
        self.addOption("Critical Bonuses",critBonuses)

        goa = QCheckBox()
        goa.stateChanged.connect(lambda state : self.setKeyValue("goa",state==Qt.Checked))
        goa.setCheckState(Qt.Checked)
        self.addOption("Garden of Assemblage",goa)

        self.addHeader("Starting Inventory Options")

        schmovement = QCheckBox()
        schmovement.stateChanged.connect(lambda state : self.setKeyValue("Schmovement",state==Qt.Checked))
        schmovement.setCheckState(Qt.Checked)
        self.addOption("Schmovement",schmovement)

        libraryOfAssemblage = QCheckBox()
        libraryOfAssemblage.stateChanged.connect(lambda state : self.setKeyValue("Library of Assemblage",state==Qt.Checked))
        libraryOfAssemblage.setCheckState(Qt.Unchecked)
        self.addOption("Library Of Assemblage",libraryOfAssemblage)


        self.items = [(138,"Scan"),(404,"No Experience"),
                (158,"Aerial Recovery"),(82,"Guard"),
                (537,"Hades Cup Trophy"),(369,"Membership Card"),
                (593,"Proof of Connection"),(594,"Proof of Nonexistence"),
                (595,"Proof of Peace"),(524,"Promise Charm")]


        self.startingItems = QListWidget()
        self.startingItems.setSelectionMode(QListWidget.SelectionMode.MultiSelection)

        for id_val,name in self.items:
            self.startingItems.addItem(name)

        self.startingItems.itemSelectionChanged.connect(self.updateStartingItems) 

        self.addRemoveSingleItem("Membership Card")

        self.addOption("Starting Inventory",self.startingItems)

        self.finalizeMenu()

    def addRemoveSingleItem(self,item_name):
        item_id = [x for x, y in enumerate(self.items) if y[1] == item_name][0]
        item = self.startingItems.item(item_id)
        item.setSelected(not item.isSelected())


    def updateStartingItems(self):
        # create a list of selected item ids
        selected = self.startingItems.selectedItems()
        itemIds = []
        for x in selected:
            itemText = x.text()
            for a,b in self.items:
                if itemText==b:
                    itemIds.append(a)
        self.setKeyValue("startingInventory",itemIds)