class KH2Item:
    def __init__(self, id, name, itemType):
        self.Id = id
        self.Name = name
        self.ItemType = itemType
        if not self.ItemType in itemTypes:
            raise Exception(self,'Not an itemType')


itemTypes = [
    "Proof",
    "MagicElement",
    "GrowthAbility",
    "ActionAbility",
    "SupportAbility",
    "TornPage",
    "Keyblade",
    "Staff",
    "Shield",
    "Armor",
    "Accessory",
    "Item",
    "Form",
    "Map",
    "Recipe",
    "Summon",
    "Report",
    "KeyItem",
    "MunnyPouch",
    "MembershipCard",
    "OCTrophy",
    "Junk"]