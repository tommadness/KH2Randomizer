# Indexing other dream weapon level up reward locations based on sword
#   returns tuples of 


from collections import namedtuple

ShieldStaff = namedtuple("ShieldStaff",["shield","staff"])

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
        self.max_level_50[36] = ShieldStaff()
        self.max_level_50[39] = ShieldStaff()
        self.max_level_50[41] = ShieldStaff()
        self.max_level_50[44] = ShieldStaff()
        self.max_level_50[46] = ShieldStaff()
        self.max_level_50[48] = ShieldStaff()
        self.max_level_50[50] = ShieldStaff()

        