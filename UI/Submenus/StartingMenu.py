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
        libraryOfAssemblage.setCheckState(Qt.Checked)
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

        self.addSingleItem("Membership Card")

        self.addOption("Starting Inventory",self.startingItems)

        self.finalizeMenu()

    def addSingleItem(self,item_name):
        item_id = [x for x, y in enumerate(self.items) if y[1] == item_name][0]
        item = self.startingItems.item(item_id)
        item.setSelected(True)

    def removeSingleItem(self,item_name):
        item_id = [x for x, y in enumerate(self.items) if y[1] == item_name][0]
        item = self.startingItems.item(item_id)
        item.setSelected(False)

    def removeAllItems(self):
        for item_id in range(self.startingItems.count()):
            item = self.startingItems.item(item_id)
            item.setSelected(False)

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


    def updateWidgets(self):
        self.widgetList[0].setCheckState(Qt.Checked if self.getKeyValue("critBonuses") else Qt.Unchecked)
        self.widgetList[1].setCheckState(Qt.Checked if self.getKeyValue("goa") else Qt.Unchecked)
        self.widgetList[2].setCheckState(Qt.Checked if self.getKeyValue("Schmovement") else Qt.Unchecked)
        self.widgetList[3].setCheckState(Qt.Checked if self.getKeyValue("Library of Assemblage") else Qt.Unchecked)
        tempItems = self.getKeyValue("startingInventory")[:]
        self.removeAllItems()
        for i in tempItems:
            item_name = [x[1] for x in self.items if x[0] == i][0]
            self.addSingleItem(item_name)