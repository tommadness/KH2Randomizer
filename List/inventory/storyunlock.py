from dataclasses import dataclass, field

from List.configDict import itemType
from List.inventory.item import InventoryItem


@dataclass(frozen=True)
class StoryUnlock(InventoryItem):
    id: int
    name: str
    type: itemType = field(init=False, default=itemType.STORYUNLOCK)


BattlefieldsOfWar = StoryUnlock(54, "Battlefields of War (Auron)")
SwordOfTheAncestor = StoryUnlock(55, "Sword of the Ancestor (Mulan)")
BeastsClaw = StoryUnlock(59, "Beast's Claw (Beast)")
BoneFist = StoryUnlock(60, "Bone Fist (Jack Skellington)")
ProudFang = StoryUnlock(61, "Proud Fang (Simba)")
SkillAndCrossbones = StoryUnlock(62, "Skill and Crossbones (Jack Sparrow)")
Scimitar = StoryUnlock(72, "Scimitar (Aladdin)")
WayToTheDawn = StoryUnlock(73, "Way to the Dawn (Riku)")
IdentityDisk = StoryUnlock(74, "Identity Disk (Tron)")
# TournamentPoster = StoryUnlock(365, "Tournament Poster")
MembershipCard = StoryUnlock(369, "Membership Card")
IceCream = StoryUnlock(375, "Ice Cream")
# TODO(zaktherobot): leaving out picture for now, may revisit if there's no confusion that picture doesn't unlock TT2 anymore
# Picture = StoryUnlock(376, "Picture")
NaminesSketches = StoryUnlock(368, "Namine's Sketches")
DisneyCastleKey = StoryUnlock(460, "Disney Castle Key")  # Dummy 13


def all_story_unlocks() -> list[StoryUnlock]:
    return [BattlefieldsOfWar, SwordOfTheAncestor, BeastsClaw, BoneFist, ProudFang, SkillAndCrossbones, Scimitar,
            WayToTheDawn, IdentityDisk, MembershipCard, IceCream, NaminesSketches, DisneyCastleKey]
