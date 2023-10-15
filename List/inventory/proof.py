from dataclasses import dataclass

from List.configDict import itemType
from List.inventory.item import InventoryItem


@dataclass(frozen=True)
class Proof(InventoryItem):
    id: int
    name: str
    type: itemType


ProofOfConnection = Proof(593, "Proof of Connection", itemType.PROOF_OF_CONNECTION)
ProofOfNonexistence = Proof(594, "Proof of Nonexistence", itemType.PROOF_OF_NONEXISTENCE)
ProofOfPeace = Proof(595, "Proof of Peace", itemType.PROOF_OF_PEACE)


def proof_item_types() -> list[itemType]:
    return [itemType.PROOF_OF_CONNECTION, itemType.PROOF_OF_NONEXISTENCE, itemType.PROOF_OF_PEACE]
