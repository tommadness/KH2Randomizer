from configDict import itemTypes

class KH2Item:
    def __init__(self, id, name, itemType):
        self.Id = id
        self.Name = name
        self.ItemType = itemType
        if not self.ItemType in itemTypes:
            raise Exception(self,'Not an itemType')


