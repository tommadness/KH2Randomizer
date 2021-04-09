import itemClass
import locationClass



def generateSpoilerLog(locationItems):
    outString = ""
    for location,item in locationItems:
        outString += "{location} : {item}\n".format(location=location.getDescription(), item=item.Name)
    return outString