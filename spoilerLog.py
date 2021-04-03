import itemClass
import locationClass

def generateSpoilerLog(locations, items):
    outString = ""
    for location in locations:
        item = next((item for item in items if item.Id == location.getReward()))
        outString += "{location} : {item}\n".format(location=location.getDescription(), item=item.Name)

    return outString