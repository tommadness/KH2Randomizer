
import sys
sys.path.append("..")

from List.LocationList import Locations
from List.configDict import locationType

description = """## Item Weights
Below you can find a list of all world locations and their classification of early, neutral, and late. Early checks are weighted in easier item placement difficulties, and late checks are weighted in harder item placement difficulties.

| Form Level | Weight |
|---|---|
| Level 2 | Early |
| Level 3 | Early |
| Level 4 | Neutral |
| Level 5 | Late |
| Level 6 | Late |
| Level 7 | Late |

| Sora Level | Weight |
|---|---|
| Level 1-99 | Neutral |

| Starting Items | Weight |
|---|---|
| GoA | Early |
| Crit Bonuses | Early |

"""

if __name__ == '__main__':
    with open("../helpinfo/itemweights.md","w") as outFile:
        outFile.write(description)
        treasures = Locations.getTreasureList()
        bonuses = Locations.getSoraBonusList()
        worlds = [locationType.LoD,locationType.BC,locationType.HB,locationType.TT,locationType.TWTNW,locationType.SP,locationType.Atlantica,locationType.PR,locationType.OC,locationType.Agrabah,locationType.HT,locationType.PL,locationType.DC,locationType.HUNDREDAW,locationType.STT]

        for world in worlds:
            outFile.write(f"| {world.value} | Weight |\n")
            outFile.write("| --- | --- |\n")
            for t in treasures:
                if world in t.LocationTypes:
                    weight = None
                    if t.LocationWeight == -10:
                        weight = "Early"
                    if t.LocationWeight == 1:
                        weight = "Neutral"
                    if t.LocationWeight == 10:
                        weight = "Late"
                    outFile.write(f"| {t.getDescription()} | {weight} |\n")
            for b in bonuses:
                if b.HasItem and world in b.LocationTypes:
                    weight = None
                    if b.LocationWeight == -10:
                        weight = "Early"
                    if b.LocationWeight == 1:
                        weight = "Neutral"
                    if b.LocationWeight == 10:
                        weight = "Late"
                    outFile.write(f"| {b.getDescription()} | {weight} |\n")
            outFile.write("\n")