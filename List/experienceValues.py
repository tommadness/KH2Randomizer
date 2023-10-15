from itertools import accumulate
import math


def vanillaFormExp():
    return {
        0: {1:6, 2:16, 3:25, 4: 42, 5: 63, 6: 98, 7:0}, # 250 (57 + 193) (~1:3.38)
        1: {1:80,2:160,3:280,4:448,5:560,6:672,7:0}, # 2200 (520 + 1680) (~1:3.23)
        2: {1:12, 2:24, 3:48, 4:76, 5:133, 6:157, 7:0}, #450 (84 + 366) (~1:4.36)
        3: {1:3, 2:6, 3:12, 4:19, 5:23, 6:27, 7:0}, #90 (21 + 69) (~1:3.28)
        4: {1:40, 2:80, 3:140, 4:224, 5:448, 6:668, 7:0}, #1600 (260 + 1340) (~1:5.15)
        5: {1:12, 2:24, 3:48, 4:76, 5:133, 6:157, 7:0} #450 (84 + 366) (~1:4.36)
        }

def middayFormExp():
    return {
        0: {1:8, 2:19, 3:48, 4: 25, 5: 42, 6: 58, 7:0}, # 200 (75 + 125)
        1: {1:92,2:184,3:324,4:266,5:334,6:400,7:0}, # 1600 (600 + 1000)
        2: {1:14, 2:29, 3:57, 4:41, 5:73, 6:86, 7:0}, #300 (100 + 200)
        3: {1:4, 2:8, 3:13, 4:11, 5:12, 6:12, 7:0}, #60 (25 + 35)
        4: {1:62, 2:123, 3:215, 4:134, 5:266, 6:400, 7:0}, #1200 (400 + 800)
        5: {1:14, 2:29, 3:57, 4:41, 5:73, 6:86, 7:0}, #300 (100 + 200)
        }
    

def duskFormExp():
    return {
        0: {1:9, 2:25, 3:56, 4: 24, 5: 36, 6: 50, 7:0}, # 200 (90 + 110)
        1: {1:115,2:230,3:405,4:226,5:284,6:340,7:0}, # 1600 (750 + 850)
        2: {1:20, 2:40, 3:80, 4:33, 5:58, 6:69, 7:0}, #300 (140 + 160)
        3: {1:4, 2:9, 3:15, 4:9, 5:11, 6:12, 7:0}, #60 (28 + 32)
        4: {1:85, 2:170, 3:295, 4:109, 5:216, 6:325, 7:0}, #1200 (550 + 650)
        5: {1:20, 2:40, 3:80, 4:33, 5:58, 6:69, 7:0}, #300 (140 + 160)
        }


def vanillaExp():
    soraExp = [
        0,
        40,
        100,
        184,
        296,
        440,
        620,
        840,
        1128,
        1492,
        1940,
        2480,
        3120,
        3902,
        4838,
        5940,
        7260,
        8814,
        10618,
        12688,
        15088,
        17838,
        20949,
        24433,
        28302,
        32622,
        37407,
        42671,
        48485,
        54865,
        61886,
        69566,
        77984,
        87160,
        97177,
        108057,
        119887,
        132691,
        146560,
        161520,
        177666,
        195026,
        213699,
        233715,
        255177,
        278117,
        302642,
        328786,
        356660,
        386378,
        417978,
        450378,
        483578,
        517578,
        552378,
        587978,
        624378,
        661578,
        699578,
        738378,
        777978,
        818378,
        859578,
        901578,
        944378,
        987978,
        1032378,
        1077578,
        1123578,
        1170378,
        1217978,
        1266378,
        1315578,
        1365578,
        1416378,
        1467978,
        1520378,
        1573578,
        1627578,
        1682378,
        1737978,
        1794378,
        1851578,
        1909578,
        1968378,
        2027978,
        2088378,
        2149578,
        2211578,
        2274378,
        2337978,
        2402378,
        2467578,
        2533578,
        2600378,
        2667978,
        2736378,
        2805578,
        2875578,
        2875578
    ]
    return soraExp


def createDiffs(experiences):
    diffs = []
    for i in range(len(experiences)-1):
        diffs.append(experiences[i+1]-experiences[i])
    return diffs


def getBaseExpProgression():
    vanilla = vanillaExp()[:-1]
    diffs = createDiffs(vanilla)
    diffs2 = createDiffs(diffs)
    diffs3 = createDiffs(diffs2)
    return diffs3

def create_new_values(second_deriv=20, first_deriv=40, early_offset=0, mid_offset=0, late_offset=0):

    diffs3 = getBaseExpProgression()
    for i in range(25):
        diffs3[i]+=early_offset

    for i in range(25,48):
        diffs3[i]+=mid_offset

    diffs3[48]+=late_offset

    diffs2 = [second_deriv]
    for d in diffs3:
        diffs2.append(diffs2[-1]+d)
    diffs = [first_deriv]
    for d in diffs2:
        diffs.append(diffs[-1]+d)
    completed = [0]
    for d in diffs:
        completed.append(completed[-1]+d)
    completed.append(completed[-1])

    for i in range(len(completed)-1):
        if completed[i+1]<completed[i]:
            print("Something went wrong")
    return completed

def middayExp(adjusted):
    if adjusted:
        return create_new_values(20,40,2,-25,400)
    else:
        return create_new_values(20,40,2,2,-800)

def duskExp(adjusted):
    if adjusted:
        return create_new_values(20,40,3,-50,1200)
    else:
        return create_new_values(20,40,3,3,-1100)
