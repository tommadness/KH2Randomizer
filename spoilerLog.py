import itemClass
import locationClass

def generateSpoilerLog(locations, items):
    outString = ""
    print(locations)
    print(items)
    for location in locations:
        item = [item for item in items if item.Id == location.getReward()]
        print(item)
        outString += "{location} : {item}\n".format(location=location.getDescription(), item=item[0].Name)
    return outString