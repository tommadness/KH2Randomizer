from dataclasses import dataclass, field
from typing import Optional

from List.configDict import itemType, locationType
from List.inventory.item import InventoryItem


@dataclass(frozen=True)
class StoryUnlock(InventoryItem):
    id: int
    name: str
    location: locationType
    visit_count: int
    type: itemType = field(init=False, default=itemType.STORYUNLOCK)


BattlefieldsOfWar = StoryUnlock(54, "Battlefields of War (Auron)", locationType.OC, visit_count=2)
SwordOfTheAncestor = StoryUnlock(55, "Sword of the Ancestor (Mulan)", locationType.LoD, visit_count=2)
BeastsClaw = StoryUnlock(59, "Beast's Claw (Beast)", locationType.BC, visit_count=2)
BoneFist = StoryUnlock(60, "Bone Fist (Jack Skellington)", locationType.HT, visit_count=2)
ProudFang = StoryUnlock(61, "Proud Fang (Simba)", locationType.PL, visit_count=2)
SkillAndCrossbones = StoryUnlock(62, "Skill and Crossbones (Jack Sparrow)", locationType.PR, visit_count=2)
Scimitar = StoryUnlock(72, "Scimitar (Aladdin)", locationType.Agrabah, visit_count=2)
WayToTheDawn = StoryUnlock(73, "Way to the Dawn (Riku)", locationType.TWTNW, visit_count=2)
IdentityDisk = StoryUnlock(74, "Identity Disk (Tron)", locationType.SP, visit_count=2)
# TournamentPoster = StoryUnlock(365, "Tournament Poster")
MembershipCard = StoryUnlock(369, "Membership Card", locationType.HB, visit_count=2)
IceCream = StoryUnlock(375, "Ice Cream", locationType.TT, visit_count=3)
# TODO(zaktherobot): leaving out picture for now, may revisit if there's no confusion that picture doesn't unlock TT2 anymore
# Picture = StoryUnlock(376, "Picture")
NaminesSketches = StoryUnlock(368, "Namine's Sketches", locationType.STT, visit_count=1)
RoyalSummons = StoryUnlock(460, "Royal Summons", locationType.DC, visit_count=2)  # Dummy 13


def all_story_unlocks() -> list[StoryUnlock]:
    return [BattlefieldsOfWar, SwordOfTheAncestor, BeastsClaw, BoneFist, ProudFang, SkillAndCrossbones, Scimitar,
            WayToTheDawn, IdentityDisk, MembershipCard, IceCream, NaminesSketches, RoyalSummons]


def all_individual_story_unlocks() -> list[StoryUnlock]:
    result: list[StoryUnlock] = []
    for unlock in all_story_unlocks():
        result.extend([unlock] * unlock.visit_count)
    return result


def story_unlock_for_location(location: locationType) -> Optional[StoryUnlock]:
    return next((unlock for unlock in all_story_unlocks() if unlock.location == location), None)
