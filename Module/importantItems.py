
def getSCOM():
    return [ 415,416 ]

def getImportantChecks():
    return [593,594,595, # proofs
            21,22,23,24,87,88, #magic
            26,27,29,31,563, # forms
            32, #pages
            159,160,25,383, #summons
            524 #promise charm
    ] + getSCOM()

def getReports():
    return [226,227,228,229,230,231,232,233,234,235,236,237,238]

def getUsefulAbilities():
    return [539, #Combo Master
            393, #Finishing Plus
            394, #Negative Combo
            401, #Exp boost
            541, #Light & Dark
            270, #Aerial Spiral
            271, #Hori Slash
            264, #Slide Dash
            559, #Flash Step
            265, #Guard Break
            266, #Explosion
            560, #Aerial Dive
            561, #Magnet Burst
            198 #Trinity Limit
            ]
            
# subjective list of useful items used in item placement weighting
def getUsefulItems():
    return [535,362, #Munny Pouches
     ] + getUsefulAbilities()


def getUsefulNightmarePassiveAbilities():
    return [ 390, # combo boost
             391, # air combo boost
             395, # berserk charge
             398, # form boost
             405, # draw
             540, # drive converter
        ]

def getUsefulNightmareActiveAbilities():
    return [ 385, # Auto valor
             386, # auto wisdom 
             387, # auto master
             388, # auto final
             568, # auto limit form
        ]
