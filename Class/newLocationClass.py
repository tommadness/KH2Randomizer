from List.configDict import itemType, locationType, locationDepth, locationCategory
from dataclasses import dataclass, field

@dataclass
class KH2Location:
    """ Location description class for the properties of a location """
    LocationId: int
    Description: str
    LocationCategory: locationCategory
    LocationTypes: list[locationType]
    InvalidChecks: list[itemType] = field(default_factory=list)
    LocationWeight: int = 1
    LocationDepth: locationDepth = locationDepth.FirstVisit

