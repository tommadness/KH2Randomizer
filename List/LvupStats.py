from collections import namedtuple

ShieldStaff = namedtuple("ShieldStaff",["shield","staff"])

# Indexing other dream weapon level up reward locations based on sword
class DreamWeaponOffsets:
    def __init__(self):
        self.max_level_50 = {}
        self.max_level_99 = {}
        for i in range(1,100):
            self.max_level_50[i] = None
            self.max_level_99[i] = None
    
        self.max_level_50[2] = ShieldStaff(4,10)
        self.max_level_50[4] = ShieldStaff(10,2)
        self.max_level_50[7] = ShieldStaff(7,7)
        self.max_level_50[9] = ShieldStaff(14,23)
        self.max_level_50[10] = ShieldStaff(2,4)
        self.max_level_50[12] = ShieldStaff(12,12)
        self.max_level_50[14] = ShieldStaff(23,9)
        self.max_level_50[15] = ShieldStaff(17,34)
        self.max_level_50[17] = ShieldStaff(34,15)
        self.max_level_50[20] = ShieldStaff(28,41)
        self.max_level_50[23] = ShieldStaff(9,14)
        self.max_level_50[25] = ShieldStaff(32,46)
        self.max_level_50[28] = ShieldStaff(41,20)
        self.max_level_50[30] = ShieldStaff(39,50)
        self.max_level_50[32] = ShieldStaff(46,25)
        self.max_level_50[34] = ShieldStaff(15,17)
        self.max_level_50[36] = ShieldStaff(44,48)
        self.max_level_50[39] = ShieldStaff(50,30)
        self.max_level_50[41] = ShieldStaff(20,28)
        self.max_level_50[44] = ShieldStaff(48,36)
        self.max_level_50[46] = ShieldStaff(25,32)
        self.max_level_50[48] = ShieldStaff(36,44)
        self.max_level_50[50] = ShieldStaff(30,39)

        self.max_level_99[7] = ShieldStaff(9,17)
        self.max_level_99[9] = ShieldStaff(17,7)
        self.max_level_99[12] = ShieldStaff(12,12)
        self.max_level_99[15] = ShieldStaff(23,33)
        self.max_level_99[17] = ShieldStaff(7,9)
        self.max_level_99[20] = ShieldStaff(20,20)
        self.max_level_99[23] = ShieldStaff(33,15)
        self.max_level_99[25] = ShieldStaff(28,47)
        self.max_level_99[28] = ShieldStaff(47,25)
        self.max_level_99[31] = ShieldStaff(39,59)
        self.max_level_99[33] = ShieldStaff(15,23)
        self.max_level_99[36] = ShieldStaff(44,73)
        self.max_level_99[39] = ShieldStaff(59,31)
        self.max_level_99[41] = ShieldStaff(53,99)
        self.max_level_99[44] = ShieldStaff(73,36)
        self.max_level_99[47] = ShieldStaff(25,28)
        self.max_level_99[49] = ShieldStaff(65,85)
        self.max_level_99[53] = ShieldStaff(99,41)
        self.max_level_99[59] = ShieldStaff(31,39)
        self.max_level_99[65] = ShieldStaff(85,49)
        self.max_level_99[73] = ShieldStaff(36,44)
        self.max_level_99[85] = ShieldStaff(49,65)
        self.max_level_99[99] = ShieldStaff(41,53)

        self.sword_to_shield_50 = {}
        self.sword_to_staff_50 = {}
        self.sword_to_shield_99 = {}
        self.sword_to_staff_99 = {}
        for i in range(1,100):
            mapping_50 = self.max_level_50[i]
            mapping_99 = self.max_level_99[i]
            if mapping_50 is not None:
                self.sword_to_shield_50[i] = mapping_50.shield
                self.sword_to_staff_50[i] = mapping_50.staff
            else:
                self.sword_to_shield_50[i] = i
                self.sword_to_staff_50[i] = i
            if mapping_99 is not None:
                self.sword_to_shield_99[i] = mapping_99.shield
                self.sword_to_staff_99[i] = mapping_99.staff
            else:
                self.sword_to_shield_99[i] = i
                self.sword_to_staff_99[i] = i

    def get_shield_level(self,max_level,sword_level):
        if max_level==50:
            return self.sword_to_shield_50[sword_level]
        elif max_level==99:
            return self.sword_to_shield_99[sword_level]
        else:
            raise ValueError(f"Tried accessing a level progression with max level {max_level}")

    def get_staff_level(self,max_level,sword_level):
        if max_level==50:
            return self.sword_to_staff_50[sword_level]
        elif max_level==99:
            return self.sword_to_staff_99[sword_level]
        else:
            raise ValueError(f"Tried accessing a level progression with max level {max_level}")


        