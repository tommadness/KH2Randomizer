from Class.exceptions import BackendException
from Module.resources import resource_path
from List.configDict import locationType

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
        self.worlds = [locationType.STT,None,locationType.TT,None,locationType.HB,locationType.BC,locationType.OC,locationType.Agrabah,
                        locationType.LoD,locationType.HUNDREDAW,locationType.PL,locationType.Atlantica,locationType.DC,locationType.DC,
                        locationType.HT,None,locationType.PR,locationType.SP,locationType.TWTNW,None,None,None,None,None]
        self.visit_flags = {}
        self.visit_flags[locationType.STT] = [0x140401]
        self.visit_flags[locationType.TT] = [0x141C01,0x143D01,0x157D79]
        self.visit_flags[locationType.HB] = [0x141C01,0x147D09]
        self.visit_flags[locationType.LoD] = [0x141C01,0x147D19]
        self.visit_flags[locationType.BC] = [0x141C01,0x147D19]
        self.visit_flags[locationType.OC] = [0x141C01,0x147D19]
        self.visit_flags[locationType.DC] = [0x141D01]
        self.visit_flags[locationType.PR] = [0x141C01,0x147D19]
        self.visit_flags[locationType.Agrabah] = [0x141D01,0x147D19]
        self.visit_flags[locationType.HT] = [0x141D01,0x147D19]
        self.visit_flags[locationType.PL] = [0x141D01,0x15FDF9]
        self.visit_flags[locationType.SP] = [0x147D01,0x15FD79]
        self.visit_flags[locationType.TWTNW] = [0x157D79]
        
        with open(resource_path("static/btlv.bin"), "rb") as btlvBar:
            self.binaryContent = bytearray(btlvBar.read())
        self._make_btlv_vanilla()
    
    def use_setting(self,setting_name, battle_level_offset : int = None):
        if setting_name == "Normal":
            self._make_btlv_vanilla()
        elif setting_name == "Offset":
            if battle_level_offset is None:
                raise BackendException("Trying to offset battle levels without a provided offset")
            self._make_btlv_vanilla()
            self._change_btlv(battle_level_offset)
        else:
            raise BackendException("Invalid battle level setting")

    def get_battle_levels(self, world: locationType):
        list_ret = [self._interpret_flags(world,x) for x in self.visit_flags[world]]
        return list_ret
        
    def write_modifications(self,outZip):
        for x in range(20):
            offset = 8+32*x
            for y in range(8,32):
                self.binaryContent[offset+y] = number_to_bytes(self.flags[x][y-8])[0]
        outZip.writestr("modified_btlv.bin",self.binaryContent)


    def _make_btlv_vanilla(self):
        self.flags = []
        for x in range(20):
            offset = 8+32*x
            self.flags.append([])
            for y in range(8,32):
                self.flags[-1].append(bytes_to_number(self.binaryContent[offset+y]))
    
    def _change_btlv(self,btlv_change):
        for world,visit_flag_list in self.visit_flags.items():
            current_btlvs = self.get_battle_levels(world)
            for visit_number in range(len(visit_flag_list)):
                self._set_battle_level(world,visit_number,current_btlvs[visit_number]+btlv_change)

    def _set_battle_level(self,world,visit_number,new_level):
        new_level = min(max(new_level,1),99)
        current_btlvs = self.get_battle_levels(world)
        prev_visit_flags = 0x040000
        prev_btlv = 1
        if visit_number > 0:
            prev_btlv = current_btlvs[visit_number-1]
            prev_visit_flags = self.visit_flags[world][visit_number-1]
            if prev_btlv > new_level:
                raise BackendException("Trying to set battle level to less than previous visit")
        delta_btlv = new_level-prev_btlv
        current_visit_flags = self.visit_flags[world][visit_number]
        changed_flags = current_visit_flags ^ prev_visit_flags
        self._set_level(world,changed_flags,delta_btlv)
        return new_level

    def _interpret_flags(self, world: locationType, flags_entry):
        world_index = self.worlds.index(world)
        battle_level_sum = 0
        flag_index=0
        skip_9 = False
        while flags_entry > 0:
            if not skip_9 and flag_index==9:
                skip_9 = True
                flags_entry = flags_entry>>1
                continue
            if flags_entry % 2 == 1:
                battle_level_sum+=self.flags[flag_index][world_index]
            flag_index+=1
            flags_entry = flags_entry>>1
        return battle_level_sum
        
    def _set_level(self, world: locationType, flags_to_set, number_to_set):
        world_index = self.worlds.index(world)
        flag_index=0
        skip_9 = False
        added_number = False
        while flags_to_set > 0:
            if not skip_9 and flag_index==9:
                skip_9 = True
                flags_to_set = flags_to_set>>1
                continue
            if flags_to_set % 2 == 1:
                self.flags[flag_index][world_index] = 0 if added_number else number_to_set
                added_number = True
            flag_index+=1
            flags_to_set = flags_to_set>>1
