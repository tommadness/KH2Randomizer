from Class.locationClass import KH2StartingItem

class StartingInventory:
    def generateStartingInventory(inventory, itemsToAdd):
        for item in itemsToAdd:
            inventory.setReward(int(item))


    def getOptions():
        return {
            "moduleName": "Sora's Starting Inventory",
            "options":{
                "Abilities": [
                    {138: "Scan"},
                    {404: "No Experience"},
                    {158: "Aerial Recovery"},
                    {82: "Guard"}

                ],
                "Items": [
                    {537: "Hades Cup Trophy"},
                    {369: "Membership Card"}
                ],
                "Proofs": [
                    {593: "Proof of Connection"},
                    {594: "Proof of Nonexistence"},
                    {595: "Proof of Peace"},
                    {524: "Promise Charm"}
                ]
            }
        }

    def getIdConverter():
        return {
            '138':"Scan",
            '537':"Hades Cup Trophy",
            '369':"Membership Card",
            '404':"No Experience",
            '158':"Aerial Recovery",
            '82':"Guard",
            '593':"Proof of Connection",
            '594':"Proof of Nonexistence",
            '595':"Proof of Peace",
            '524':"Promise Charm"
        }