import random

class SeedModifier():
    def getOptions():
        return [
            {
                "name": "Max Logic Item Placement",
                "description": "Less restricted item placement. All checks still obtainable."
            },
            {
                "name": "Reverse Rando",
                "description": "Use when generating a Reverse Rando seed to ensure softlock protection"
            },
            {
                "name":"Glass Cannon",
                "description": "No more pesky Defense Ups in the level up stats pool"
            },
            {
                "name":"Library of Assemblage",
                "description": "Start with all the hints"
            },
            {
                "name": "Schmovement",
                "description": "Start with selected level of all growth abilities"
            },
            {
                "name": "Better Junk",
                "description": "No more synthesis materials in the junk item pool"
            },
            {
                "name": "Randomize Ability Pool",
                "description": "Pick Sora's action/support abilities at random (guaranteed to have 1 SC & 1 OM)"
            },
            {
                "name": "Start with No AP",
                "description": "Sora/Donald/Goofy start the game with 0 AP"
            },
            {
                "name": "Remove Damage Cap",
                "description": "Removes the damage cap for every enemy/boss in the game."
            },
            {
                "name": "Cups Give XP",
                "description": "Defeating enemies while in an OC Cup will give you XP and Form XP"
            }
        ]

    def randomAbilityPool(action, support):
        abilitylist = action + support
        abilitydict = {i.Name: i for i in abilitylist}
        possibleabilities = list(set([i.Name for i in abilitylist if i.Name not in ["Second Chance", "Once More"]]))
        possibleabilities.sort()
        randomabilitypool = []
        for _ in range(len(abilitylist)-2):
            choice = random.choice(possibleabilities)
            randomabilitypool.append(abilitydict[choice])
            # Limit only 1 of each action ability in the pool, to make it more interesting
            if choice in [i.Name for i in action]:
                possibleabilities.remove(choice)

        # Make sure there is one OM and one SC so the tracker behaves
        randomabilitypool.append(abilitydict["Second Chance"])
        randomabilitypool.append(abilitydict["Once More"])
        return randomabilitypool

    def randomSupportAbilityPool(action, support):
        abilitylist = support
        abilitydict = {i.Name: i for i in abilitylist}
        possibleabilities = list(set([i.Name for i in abilitylist if i.Name not in ["Second Chance", "Once More"]]))
        possibleabilities.sort()
        randomabilitypool = []
        for _ in range(len(abilitylist)-2):
            choice = random.choice(possibleabilities)
            randomabilitypool.append(abilitydict[choice])
            # Limit only 1 of each action ability in the pool, to make it more interesting
            if choice in [i.Name for i in action]:
                possibleabilities.remove(choice)

        # Make sure there is one OM and one SC so the tracker behaves
        randomabilitypool.append(abilitydict["Second Chance"])
        randomabilitypool.append(abilitydict["Once More"])
        return randomabilitypool + action

    def defaultAbilityPool(action, support):
        return action+support

    def glassCannon():
        return [{"Stat":"Str","Value": 2},{"Stat":"Mag", "Value": 2},{"Stat": "Ap", "Value": 2}]
    
    def regularStats():
        return [{"Stat":"Str","Value": 2},{"Stat":"Mag", "Value": 2},{"Stat":"Def", "Value": 1},{"Stat": "Ap", "Value": 2}]

    def library(enabled):
        if enabled:
            return [
                        226,
                        227,
                        228,
                        229,
                        230,
                        231,
                        232,
                        233,
                        234,
                        235,
                        236,
                        237,
                        238
                    ]
        return []

    def world_unlocks(enabled):
        if enabled:
            return [54,
                    55,
                    59,
                    60,
                    61,
                    62,
                    72,
                    74,
                    369,
                    375,
                    376]
        return []

    def schmovement(level_setting):
        growth_all = {}
        growth_all[0] =  [] # none
        growth_all[1] =  [94,98,102,106,564] # level 1
        growth_all[2] =  [95,99,103,107,565] # level 2
        growth_all[3] =  [96,100,104,108,566] # level 3
        growth_all[4] =  [97,101,105,109,567] # level max
        if level_setting=="Level_1":
            return growth_all[1]
        if level_setting=="Level_2":
            return growth_all[1] + growth_all[2]
        if level_setting=="Level_3":
            return growth_all[1] + growth_all[2] + growth_all[3]
        if level_setting=="Level_4":
            return growth_all[1] + growth_all[2] + growth_all[3] + growth_all[4]
        ##########
        #commented out because of a strange bug... 
        #the ability levels set after clicking Generate seed the first time
        #are always different from the levels set from the 2nd time after.
        #Example senario: generate once and get [2,1,2,0,0] as the level list. generate the seed 
        #again without changing any settings and the level list changes to [4,0,0,0,1].
        #if you continue the clicking generate seed then the level list stays as [4,0,0,0,1].
        #i don't know why it is doing this.... why does random change after the first genration? 
        ###########
        #
        #if level_setting=="Random":
        #    random_growth = []
        #    random_levels = []
        #    current = 0
        #    count = 5
        #    #split a count into separate numbers that, in total, add up to count
        #    while count > 0:
        #        n = random.randint(0, count)
        #        if n == 5:
        #            n = 4
        #        random_levels.append(n)
        #        count -= n
        #    #if the list length is less than 5 then add 0s to list until it is.
        #    while len(random_levels) < 5:
        #        random_levels.append(0)
        #    print(' '.join(map(str, random_levels)))
        #    #shuffle list to randomize which level each growth type gets
        #    random.shuffle(random_levels)
        #    #get all the abilities IDs needed for each growth and add them to a list
        #    while current < 5:
        #        if random_levels[current] == 0:
        #            current += 1
        #        elif random_levels[current] == 1:
        #            random_growth.append(growth_all[1][current])
        #            current += 1
        #        elif random_levels[current] == 2:
        #            random_growth.append(growth_all[1][current])
        #            random_growth.append(growth_all[2][current])
        #            current += 1
        #        elif random_levels[current] == 3:
        #            random_growth.append(growth_all[1][current])
        #            random_growth.append(growth_all[2][current])
        #            random_growth.append(growth_all[3][current])
        #            current += 1
        #        elif random_levels[current] == 4:
        #            random_growth.append(growth_all[1][current])
        #            random_growth.append(growth_all[2][current])
        #            random_growth.append(growth_all[3][current])
        #            random_growth.append(growth_all[4][current])
        #            current += 1
        #    return random_growth
        return []
        
    #Old version
    #def schmovement(enabled):
    #    if enabled:
    #        return [
    #            94,
    #            98,
    #            102,
    #            106,
    #            564
    #        ]
    #    return []