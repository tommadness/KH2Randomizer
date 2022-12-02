from Module.resources import resource_path
from List.configDict import itemType, locationCategory, locationType

def number_to_bytes(item):
    # for byte1, find the most significant bits from the item Id
    itemByte1 = item>>8
    # for byte0, isolate the least significant bits from the item Id
    itemByte0 = item & 0x00FF
    return itemByte0,itemByte1

def bytes_to_number(byte0, byte1=0):
    return int(byte0)+int(byte1<<8)

class BtlvViewer():
    def __init__(self):            
        self.worlds = [locationType.STT,None,locationType.TT,None,locationType.HB,locationType.BC,locationType.OC,locationType.Agrabah,locationType.LoD,locationType.HUNDREDAW,locationType.PL,locationType.Atlantica,locationType.DC,locationType.DC,locationType.HT,None,locationType.PR,locationType.SP,locationType.TWTNW,None,None,None,None,None]
        with open(resource_path("static/btlv.bin"), "rb") as btlvBar:
            self.binaryContent = bytearray(btlvBar.read())
            self.flags = []
            for x in range(20):
                offset = 8+32*x
                self.flags.append([])
                for y in range(8,32):
                    self.flags[-1].append(bytes_to_number(self.binaryContent[offset+y]))

    def get_battle_levels(self, world: locationType):
        #stt 1,2,18
        #tt  4,10,11,12,13,16,18,20
        pass
    def write_modifications(self,outZip):
        for x in range(20):
            offset = 8+32*x
            for y in range(8,32):
                self.binaryContent[offset+y] = number_to_bytes(self.flags[x][y-8])[0]
        outZip.writestr("modified_btlv.bin",self.binaryContent)