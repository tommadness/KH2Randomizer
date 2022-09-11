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
        if "Second Chance" in abilitydict:
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
        if "Second Chance" in abilitydict:
            randomabilitypool.append(abilitydict["Second Chance"])
            randomabilitypool.append(abilitydict["Once More"])
        return randomabilitypool + action

    def defaultAbilityPool(action, support):
        return action+support

    def glassCannon():
        return [{"Stat":"Str","Value": 2},{"Stat":"Mag", "Value": 2},{"Stat": "Ap", "Value": 2}]
    
    def regularStats():
        return [{"Stat":"Mag", "Value": 2},{"Stat":"Str","Value": 2},{"Stat":"Def", "Value": 1},{"Stat": "Ap", "Value": 2}]

    def library(number_reports):
        reports = [
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
        return reports[0:number_reports]

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
        return []

    def random_schmovement():
        growth_all = {}
        growth_all[0] =  [] # none
        growth_all[1] =  [94,98,102,106,564] # level 1
        growth_all[2] =  [95,99,103,107,565] # level 2
        growth_all[3] =  [96,100,104,108,566] # level 3
        growth_all[4] =  [97,101,105,109,567] # level max
        random_growth = []
        random_levels = [0,0,0,0,0]

        iter = 0
        while iter < 5:
            picked = random.randint(0,4)
            if random_levels[picked]!=4:
                random_levels[picked]+=1
                iter+=1
        #get all the abilities IDs needed for each growth and add them to a list
        for current in range(5):
            [random_growth.append(growth_all[i][current]) for i in range(1,random_levels[current]+1)]
        return random_growth
