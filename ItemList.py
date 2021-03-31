class KH2Item:
    def __init__(self, id, name, itemType):
        self.Id = id
        self.Name = name
        self.ItemType = itemType

itemList = [
    KH2Item(593, "Proof of Connection", "Proof"),
    KH2Item(594, "Proof of Nonexistence", "Proof"),
    KH2Item(595, "Proof of Peace", "Proof"),
    KH2Item(576, "Remembrance Shard", "Junk"),
    KH2Item(577, "Remembrance Stone", "Junk"),
    KH2Item(578, "Remembrance Gem", "Junk")
]