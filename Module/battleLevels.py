import random

from Class.exceptions import BackendException
from List.configDict import locationType, BattleLevelOption
from Module.resources import resource_path


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
        self.worlds = [None,None,locationType.TT,None,locationType.HB,locationType.BC,locationType.OC,locationType.Agrabah,
                        locationType.LoD,locationType.HUNDREDAW,locationType.PL,locationType.Atlantica,locationType.DC,locationType.DC,
                        locationType.HT,None,locationType.PR,locationType.SP,locationType.TWTNW,None,None,None,None,None]
        self.goa_btlv = True
        self.random_option = None
        self.battle_level_range = None
        btlv_file = "static/btlv.bin"

        if self.goa_btlv:
            btlv_file = "static/goa_btlv.bin"
            self.visit_flags = {}
            self.visit_flags[locationType.STT] = [(2,0x00010),(2,0x00020),(2,0x00040)]
            self.visit_flags[locationType.TT] = [(2,0x00100),(2,0x00200),(2,0x00800)]
            self.visit_flags[locationType.HB] = [(4,0x00010),(4,0x00080),(4,0x00200)]
            self.visit_flags[locationType.LoD] = [(8,0x00010),(8,0x00020)]
            self.visit_flags[locationType.BC] = [(5,0x00010),(5,0x00020)]
            self.visit_flags[locationType.OC] = [(6,0x00010),(6,0x00020)]
            self.visit_flags[locationType.DC] = [(12,0x00010),(13,0x00010),(13,0x00020)]
            self.visit_flags[locationType.PR] = [(16,0x00010),(16,0x00020)]
            self.visit_flags[locationType.Agrabah] = [(7,0x00010),(7,0x00040)]
            self.visit_flags[locationType.HT] = [(14,0x00010),(14,0x00040)]
            self.visit_flags[locationType.PL] = [(10,0x00010),(10,0x00040)]
            self.visit_flags[locationType.SP] = [(17,0x00010),(17,0x00040)]
            self.visit_flags[locationType.TWTNW] = [(18,0x00010)]
        else:
            self.visit_flags = {}
            self.visit_flags[locationType.TT] = [(2,0x040001),(2,0x140001),(2,0x140401),(2,0x141C01),(2,0x143D01),(2,0x157D79)]
            self.visit_flags[locationType.HB] = [(4,0x141C01),(4,0x147D09),(4,0x15FD79)]
            self.visit_flags[locationType.LoD] = [(8,0x141C01),(8,0x147D19)]
            self.visit_flags[locationType.BC] = [(5,0x141C01),(5,0x147D19)]
            self.visit_flags[locationType.OC] = [(6,0x141C01),(6,0x147D19)]
            self.visit_flags[locationType.DC] = [(12,0x141D01),(13,0x141D01)]
            self.visit_flags[locationType.PR] = [(16,0x141C01),(16,0x147D19)]
            self.visit_flags[locationType.Agrabah] = [(7,0x141D01),(7,0x147D19)]
            self.visit_flags[locationType.HT] = [(14,0x141D01),(14,0x147D19)]
            self.visit_flags[locationType.PL] = [(10,0x141D01),(10,0x15FDF9)]
            self.visit_flags[locationType.SP] = [(17,0x147D01),(17,0x15FD79)]
            self.visit_flags[locationType.TWTNW] = [(18,0x157D79)]
        
        with open(resource_path(btlv_file), "rb") as btlvBar:
            self.binaryContent = bytearray(btlvBar.read())
        self._make_btlv_vanilla()
    
    def use_setting(self, setting_name: str, battle_level_offset: int = None, battle_level_range: int = None):
        self.random_option = setting_name
        self.battle_level_range = battle_level_range
        self.random_option = self.random_option.upper()
        if self.random_option == BattleLevelOption.NORMAL.name:
            self._make_btlv_vanilla()
        elif self.random_option == BattleLevelOption.SHUFFLE.name:
            self._make_btlv_vanilla()
            self._shuffle_btlv()
        elif self.random_option == BattleLevelOption.OFFSET.name:
            if battle_level_offset is None:
                raise BackendException("Trying to offset battle levels without a provided offset")
            self._make_btlv_vanilla()
            self._offset_btlv(battle_level_offset)
        elif self.random_option == BattleLevelOption.RANDOM_WITHIN_RANGE.name:
            self._make_btlv_vanilla()
            self._variance_btlv()
        elif self.random_option == BattleLevelOption.RANDOM_MAX_50.name:
            self._pure_random_btlv()
        elif self.random_option == BattleLevelOption.SCALE_TO_50.name:
            self._make_btlv_vanilla()
            self._scale_btlv(50)
        else:
            raise BackendException("Invalid battle level setting")

    def get_spoiler(self):
        output_json = {}
        for world in self.visit_flags:
            output_json[world] = self.get_battle_levels(world)
        return output_json

    def get_battle_levels(self, world: locationType):
        list_ret = [self._interpret_flags(x) for x in self.visit_flags[world]]
        return list_ret
        
    def write_modifications(self, outZip):
        for x in range(20):
            offset = 8+32*x
            for y in range(8,32):
                self.binaryContent[offset+y] = number_to_bytes(self.flags[x][y-8])[0]
        outZip.writestr("modified_btlv.bin",self.binaryContent)

    def _interpret_flags(self, flags_entry):
        battle_level_sum = 0
        flag_index=0
        skip_9 = self.goa_btlv
        world_index = flags_entry[0]
        flags_entry = flags_entry[1]
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

    def _make_btlv_vanilla(self):
        self.random_option = None
        self.flags = []
        for x in range(20):
            offset = 8+32*x
            self.flags.append([])
            for y in range(8,32):
                self.flags[-1].append(bytes_to_number(self.binaryContent[offset+y]))
    
    def _variance_btlv(self):
        level_range = self.battle_level_range
        if level_range is None:
            raise BackendException("Trying to range battle levels without a provided range")
        elif level_range == 0:
            return
        for world, visit_flag_list in self.visit_flags.items():
            current_btlvs = self.get_battle_levels(world)
            for visit_number in range(len(visit_flag_list)):
                btlv_change = random.randint(-level_range, level_range)
                self._set_battle_level(world,visit_flag_list[visit_number][0],visit_number,current_btlvs[visit_number]+btlv_change)

    def _pure_random_btlv(self):
        for world,visit_flag_list in self.visit_flags.items():
            for visit_number in range(len(visit_flag_list)):
                btlv_change = random.randint(1,50)
                self._set_battle_level(world,visit_flag_list[visit_number][0],visit_number,btlv_change)

    def _shuffle_btlv(self):
        battle_level_list = []
        for world, visit_flag_list in self.visit_flags.items():
            battle_level_list += self.get_battle_levels(world)

        random.shuffle(battle_level_list)

        for world, visit_flag_list in self.visit_flags.items():
            for visit_number in range(len(visit_flag_list)):
                new_level = battle_level_list.pop()
                self._set_battle_level(world, visit_flag_list[visit_number][0], visit_number, new_level)

    def _scale_btlv(self,scaled_level):
        for world,visit_flag_list in self.visit_flags.items():
            current_btlvs = self.get_battle_levels(world)
            for visit_number in range(len(visit_flag_list)):
                new_level = int((current_btlvs[visit_number]*1.0/current_btlvs[-1])*scaled_level)
                self._set_battle_level(world,visit_flag_list[visit_number][0],visit_number,new_level)

    def _offset_btlv(self,btlv_change):
        for world,visit_flag_list in self.visit_flags.items():
            current_btlvs = self.get_battle_levels(world)
            for visit_number in range(len(visit_flag_list)):
                self._set_battle_level(world,visit_flag_list[visit_number][0],visit_number,current_btlvs[visit_number]+btlv_change)

    def _set_battle_level(self,world,world_index,visit_number,new_level):
        new_level = min(max(new_level,1),99)
        current_btlvs = self.get_battle_levels(world)
        prev_visit_flags = (world_index,0x040000)
        prev_btlv = 1
        if visit_number > 0:
            prev_btlv = current_btlvs[visit_number-1]
            prev_visit_flags = self.visit_flags[world][visit_number-1]
            # if prev_btlv > new_level:
            #     raise BackendException("Trying to set battle level to less than previous visit")
        current_visit_flags = self.visit_flags[world][visit_number]
        if not self.goa_btlv and prev_visit_flags[0] == current_visit_flags[0]:
            delta_btlv = new_level-prev_btlv
            changed_flags = current_visit_flags[1] ^ prev_visit_flags[1]
            self._set_level(world_index,(current_visit_flags[0],changed_flags),delta_btlv)
        else:
            self._set_level(world_index,current_visit_flags,new_level)

        return new_level

        
    def _set_level(self, world_index, flags_to_set, number_to_set):
        flag_index=0
        skip_9 = self.goa_btlv
        added_number = False
        world_index = flags_to_set[0]
        flags_to_set = flags_to_set[1]
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
