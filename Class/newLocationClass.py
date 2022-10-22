from List.configDict import itemType, locationType, locationDepth, locationCategory
from dataclasses import dataclass, field

@dataclass(unsafe_hash=True)
class KH2Location:
    """ Location description class for the properties of a location """
    LocationId: int
    Description: str
    LocationCategory: locationCategory
    LocationTypes: list[locationType] = field(compare=False)
    InvalidChecks: list[itemType] = field(default_factory=list,compare=False)
    VanillaItems: list[int] = field(default_factory=list,compare=False)

    def __eq__(self, obj):
        return self.LocationId==obj.LocationId and self.LocationCategory==obj.LocationCategory and self.LocationTypes==obj.LocationTypes

    def __str__(self):
        return f"{self.LocationTypes} - {self.Description}"