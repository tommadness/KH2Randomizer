import io
import json
import yaml
import zipfile
from itertools import accumulate
from Class.exceptions import BossEnemyException

from Class.itemClass import ItemEncoder, itemRarity
from Class.modYml import modYml
from List.ItemList import Items
from List.LvupStats import DreamWeaponOffsets
from List.configDict import itemType, locationCategory, locationType
from Module.RandomizerSettings import RandomizerSettings
from Module.hints import Hints
from Module.newRandomize import Randomizer, SynthesisRecipe
from Module.randomBGM import RandomBGM
from Module.randomCmdMenu import RandomCmdMenu
from Module.resources import resource_path
from Module.spoilerLog import itemSpoilerDictionary, levelStatsDictionary


def noop(self, *args, **kw):
    pass


def number_to_bytes(item):
    # for byte1, find the most significant bits from the item Id
    itemByte1 = item>>8
    # for byte0, isolate the least significant bits from the item Id
    itemByte0 = item & 0x00FF
    return itemByte0,itemByte1

# def bytes_to_number(byte0, byte1=0):
#     return int(byte0)+int(byte1<<8)

# id_to_enemy_name = {}

# id_to_enemy_name[1] = "Soldier"
# id_to_enemy_name[2] = "Shadow"
# id_to_enemy_name[3] = "Large Body"
# id_to_enemy_name[4] = "Armored Knight"
# id_to_enemy_name[5] = "Surveillance Robot"
# id_to_enemy_name[6] = "Dusk"
# id_to_enemy_name[7] = "Trick Ghost"
# id_to_enemy_name[8] = "Rabid Dog"
# id_to_enemy_name[9] = "Hook Bat"
# id_to_enemy_name[10] = "Minute Bomb"
# id_to_enemy_name[11] = "Assault Rider"
# id_to_enemy_name[12] = "Hammer Frame"
# id_to_enemy_name[13] = "Aeroplane"
# id_to_enemy_name[14] = ""
# id_to_enemy_name[15] = "Samurai"
# id_to_enemy_name[16] = ""
# id_to_enemy_name[17] = "Rapid Thruster"
# id_to_enemy_name[18] = "Bolt Tower"
# id_to_enemy_name[19] = ""
# id_to_enemy_name[22] = "Dragoon"
# id_to_enemy_name[23] = "Assassin"
# id_to_enemy_name[24] = "Sniper"
# id_to_enemy_name[25] = "Dancer"
# id_to_enemy_name[26] = "Berserker"
# id_to_enemy_name[27] = "Gambler"
# id_to_enemy_name[28] = "Sorcerer"
# id_to_enemy_name[29] = "Creeper"
# id_to_enemy_name[30] = "Nightwalker"
# id_to_enemy_name[32] = "Fortuneteller"
# id_to_enemy_name[33] = "Luna Bandit" #silver rock
# id_to_enemy_name[34] = "Hot Rod"
# id_to_enemy_name[35] = "Cannon Gun" # tornado step
# id_to_enemy_name[36] = "Living Bone"
# id_to_enemy_name[37] = "Devastator"
# id_to_enemy_name[38] = "Lance Soldier"
# id_to_enemy_name[39] = "Driller Mole"
# id_to_enemy_name[40] = "Shaman"
# id_to_enemy_name[41] = "Neoshadow"
# id_to_enemy_name[42] = "Magnum Loader"
# id_to_enemy_name[43] = "Morning Star"
# id_to_enemy_name[44] = "Tornado Step" #Cannon Gun
# id_to_enemy_name[45] = "Gargoyle Knight"
# id_to_enemy_name[46] = "Gargoyle Warrior"
# id_to_enemy_name[47] = "Silver Rock" #Luna Bandit
# id_to_enemy_name[48] = "Wight Knight"
# id_to_enemy_name[49] = "Emerald Blues"
# id_to_enemy_name[50] = "Crimson Jazz"
# id_to_enemy_name[51] = "Crescendo"
# id_to_enemy_name[52] = "Creeper Plant"
# id_to_enemy_name[53] = ""
# id_to_enemy_name[54] = ""
# id_to_enemy_name[55] = ""
# id_to_enemy_name[56] = ""
# id_to_enemy_name[60] = ""
# id_to_enemy_name[61] = ""
# id_to_enemy_name[62] = ""
# id_to_enemy_name[63] = "Air Pirate"
# id_to_enemy_name[64] = "Fat Bandit"
# id_to_enemy_name[65] = "Fiery Globe"
# id_to_enemy_name[66] = "Icy Cube"
# id_to_enemy_name[69] = "Aerial Knocker"
# id_to_enemy_name[70] = ""
# id_to_enemy_name[71] = ""
# id_to_enemy_name[72] = "" # Dusk Roxas Prologue
# id_to_enemy_name[73] = "Strafer"
# id_to_enemy_name[74] = ""
# id_to_enemy_name[75] = ""
# id_to_enemy_name[76] = ""
# id_to_enemy_name[77] = ""
# id_to_enemy_name[78] = ""
# id_to_enemy_name[79] = ""
# id_to_enemy_name[80] = ""
# id_to_enemy_name[81] = ""
# id_to_enemy_name[82] = "Illuminator"
# id_to_enemy_name[83] = ""
# id_to_enemy_name[84] = ""
# id_to_enemy_name[85] = ""
# id_to_enemy_name[86] = ""
# id_to_enemy_name[87] = "Undead Pirate A"
# id_to_enemy_name[88] = "Undead Pirate B"
# id_to_enemy_name[89] = "Undead Pirate C"
# id_to_enemy_name[90] = ""
# id_to_enemy_name[91] = ""
# id_to_enemy_name[92] = ""
# id_to_enemy_name[93] = ""
# id_to_enemy_name[94] = ""
# id_to_enemy_name[95] = ""
# id_to_enemy_name[96] = "Bookmaster"
# id_to_enemy_name[97] = "Quickplay (Aladdin)"
# id_to_enemy_name[98] = "Quickplay (Sora)"
# id_to_enemy_name[99] = "Speedster End"
# id_to_enemy_name[100] = "Speedster Start"
# id_to_enemy_name[102] = ""
# id_to_enemy_name[103] = ""
# id_to_enemy_name[104] = ""
# id_to_enemy_name[105] = ""
# id_to_enemy_name[106] = ""
# id_to_enemy_name[107] = ""
# id_to_enemy_name[108] = ""
# id_to_enemy_name[109] = ""
# id_to_enemy_name[111] = ""
# id_to_enemy_name[112] = "Graveyard/Toy Soldier"
# id_to_enemy_name[114] = ""
# id_to_enemy_name[115] = "Lance Soldier?"
# id_to_enemy_name[116] = ""
# id_to_enemy_name[117] = ""
# id_to_enemy_name[118] = "Lance Soldier RC"
# id_to_enemy_name[119] = ""
# id_to_enemy_name[120] = "STT Dusk"
# id_to_enemy_name[121] = "Creeper Day 6"
# id_to_enemy_name[122] = ""
# id_to_enemy_name[123] = "Creeper Plant RC"
# id_to_enemy_name[125] = "Crescendo RC"
# id_to_enemy_name[126] = "Gambler RC"
# id_to_enemy_name[127] = ""
# id_to_enemy_name[128] = ""
# id_to_enemy_name[129] = ""
# id_to_enemy_name[130] = "Assassin Day 6"
# id_to_enemy_name[131] = ""
# id_to_enemy_name[132] = ""
# id_to_enemy_name[133] = ""
# id_to_enemy_name[134] = ""
# id_to_enemy_name[135] = ""




# class DropRates():
#     def __init__(self,bytes):
#         self.id = bytes_to_number(bytes[0],bytes[1])
#         self.small_hp = bytes_to_number(bytes[2])
#         self.big_hp = bytes_to_number(bytes[3])
#         self.big_munny = bytes_to_number(bytes[4])
#         self.medium_munny = bytes_to_number(bytes[5])
#         self.small_munny = bytes_to_number(bytes[6])
#         self.small_mp = bytes_to_number(bytes[7])
#         self.big_mp = bytes_to_number(bytes[8])
#         self.small_drive = bytes_to_number(bytes[9])
#         self.big_drive = bytes_to_number(bytes[10])
#         self.item1 = bytes_to_number(bytes[12],bytes[13])
#         self.item1_chance = bytes_to_number(bytes[14],bytes[15])
#         self.item2 = bytes_to_number(bytes[16],bytes[17])
#         self.item2_chance = bytes_to_number(bytes[18],bytes[19])
#         self.item3 = bytes_to_number(bytes[20],bytes[21])
#         self.item3_chance = bytes_to_number(bytes[22],bytes[23])

#     def __str__(self):
#         return f"{self.id} \n HP ({self.small_hp},{self.big_hp}) \n MP ({self.small_mp},{self.big_mp}) \n Munny ({self.small_munny},{self.medium_munny},{self.big_munny}) \n Orbs ({self.small_drive},{self.big_drive}) Items: \n--- {self.item1} ({self.item1_chance/1.0}%)\n--- {self.item2} ({self.item2_chance/1.0}%)\n--- {self.item3} ({self.item3_chance/1.0}%)"


class SynthLocation():
    def __init__(self, loc, item, in_recipe: SynthesisRecipe):
        self.location = loc
        self.item = item
        self.requirements = [(0,0)]*6
        self.recipe = in_recipe
        self.unlock_rank = in_recipe.unlock_rank
        for i in range(len(self.recipe.requirements)):
            self.addReq(i,self.recipe.requirements[i].item_id,self.recipe.requirements[i].amount)

    def getStartingLocation(self):
        # header bytes + offset to the specific recipe + skip over the recipe bytes
        return 16+self.location*32+2

    def getBytes(self):
        bytes = []
        bytes = [self.unlock_rank,0] # unlock condition/rank
        item_byte0,item_byte1 = number_to_bytes(self.item)
        # add the item for this recipe
        bytes.append(item_byte0)
        bytes.append(item_byte1)
        # add the item as the upgraded version
        bytes.append(item_byte0)
        bytes.append(item_byte1)

        for req in self.requirements:
            item_byte0,item_byte1 = number_to_bytes(req[0])
            # add the item as an ingredient
            bytes.append(item_byte0)
            bytes.append(item_byte1)
            item_byte0,item_byte1 = number_to_bytes(req[1])
            # add the amount of that ingredient
            bytes.append(item_byte0)
            bytes.append(item_byte1)
        return bytes

    def addReq(self,req_number,req_item,req_amount):
        self.requirements[req_number] = (req_item,req_amount)



class SeedZip():
    def __init__(self,settings: RandomizerSettings, randomizer: Randomizer, hints, cosmetics_data):
        self.formattedTrsr = {}
        self.formattedLvup = {"Sora":{}}
        self.formattedBons = {}
        self.formattedFmlv = {}
        self.formattedItem = {"Stats":[]}
        self.formattedPlrp = []
        self.spoiler_log = None

        self.assignTreasures(randomizer)
        self.assignLevels(settings,randomizer)
        self.assignSoraBonuses(randomizer)
        self.assignDonaldBonuses(randomizer)
        self.assignGoofyBonuses(randomizer)
        self.assignFormLevels(randomizer)
        self.assignWeaponStats(randomizer)
        self.assignStartingItems(settings, randomizer)
        self.createZip(settings, randomizer, hints, cosmetics_data)

    def createZip(self, settings: RandomizerSettings, randomizer : Randomizer, hints, cosmetics_data):

        # with open(resource_path("static/drops.bin"), "rb") as dropsbar:
        #     binaryContent = bytearray(dropsbar.read())
        #     for i in range(0,184):
        #         start_index = 8+24*i
        #         rates = DropRates(binaryContent[start_index:start_index+24])
        #         print(rates)

        mod = modYml.getDefaultMod()
        sys = modYml.getSysYAML(settings.seedHashIcons,settings.crit_mode)

        data = io.BytesIO()
        with zipfile.ZipFile(data,"w") as outZip:
            yaml.emitter.Emitter.process_tag = noop

            self.createPuzzleAssets(settings, randomizer, mod, outZip)
            self.createSynthAssets(settings, randomizer, mod, outZip)
            self.createASDataAssets(settings, mod, outZip)
            self.createRetryAssets(settings, mod, outZip)
            self.createSkipCarpetAssets(settings, mod, outZip)
            self.createMapSkipAssets(settings, mod, outZip)

            outZip.writestr("TrsrList.yml", yaml.dump(self.formattedTrsr, line_break="\r\n"))
            outZip.writestr("BonsList.yml", yaml.dump(self.formattedBons, line_break="\r\n"))
            outZip.writestr("LvupList.yml", yaml.dump(self.formattedLvup, line_break="\r\n"))
            outZip.writestr("FmlvList.yml", yaml.dump(self.formattedFmlv, line_break="\r\n"))
            outZip.writestr("ItemList.yml", yaml.dump(self.formattedItem, line_break="\r\n"))
            outZip.writestr("PlrpList.yml", yaml.dump(self.formattedPlrp, line_break="\r\n"))
            outZip.writestr("sys.yml", yaml.dump(sys, line_break="\r\n"))
            outZip.writestr("jm.yml", yaml.dump(modYml.getJMYAML(), line_break="\r\n"))

            if hints is not None:
                Hints.writeHints(hints, "HintFile", outZip)

            cmdMenuChoice = cosmetics_data["cmdMenuChoice"]
            platform = cosmetics_data["platform"]
            randomBGMOptions = cosmetics_data["randomBGM"]
            tourney_gen = cosmetics_data["tourney"]

            def _shouldRunKHBR():
                if not settings.enemy_options.get("boss", False) in [False, "Disabled"]:
                    return True
                if not settings.enemy_options.get("enemy", False) in [False, "Disabled"]:
                    return True
                if settings.enemy_options.get("remove_damage_cap", False):
                    return True
                if settings.enemy_options.get("cups_give_xp", False):
                    return True

            enemySpoilers = None
            enemySpoilersJSON = {}
            if _shouldRunKHBR():
                try:
                    if platform == "PC":
                        settings.enemy_options["memory_expansion"] = True
                    else:
                        settings.enemy_options["memory_expansion"] = False
                    
                    from khbr.randomizer import Randomizer as khbr
                    enemySpoilers = khbr().generateToZip("kh2", settings.enemy_options, mod, outZip)
                    lines = enemySpoilers.split("\n")

                    current_key = ""
                    for line in lines:
                        if '\t' in line:
                            modded_line = line.replace('\t','')
                            enemies = modded_line.split(" became ")
                            # this is adding to the current list
                            new_entry = {}
                            new_entry["original"] = enemies[0]
                            new_entry["new"] = enemies[1]
                            enemySpoilersJSON[current_key].append(new_entry)
                        elif line!="":
                            current_key = line
                            enemySpoilersJSON[current_key] = []
                except Exception as e:
                    raise BossEnemyException(f"Boss/enemy module had an unexpected error {e}. Try different a different seed or different settings.")

            self.createBetterSTTAssets(settings, mod, outZip)
            
            if settings.spoiler_log or tourney_gen:
                if not tourney_gen:
                    mod["title"] += " w/ Spoiler"
                with open(resource_path("static/spoilerlog.html")) as spoiler_site:
                    html_template = spoiler_site.read().replace("SEED_NAME_STRING",settings.random_seed) \
                                                       .replace("LEVEL_STATS_JSON",json.dumps(levelStatsDictionary(randomizer.levelStats))) \
                                                       .replace("FORM_EXP_JSON",json.dumps({"Summon": {"multiplier": settings.summon_exp_multiplier, "values": list(accumulate(settings.summon_exp))},
                                                                                            "Valor": {"multiplier": settings.valor_exp_multiplier, "values": list(accumulate(settings.valor_exp))},
                                                                                            "Wisdom": {"multiplier": settings.wisdom_exp_multiplier, "values": list(accumulate(settings.wisdom_exp))},
                                                                                            "Limit": {"multiplier": settings.limit_exp_multiplier, "values": list(accumulate(settings.limit_exp))},
                                                                                            "Master": {"multiplier": settings.master_exp_multiplier, "values": list(accumulate(settings.master_exp))},
                                                                                            "Final": {"multiplier": settings.final_exp_multiplier, "values": list(accumulate(settings.final_exp))},})) \
                                                       .replace("DEPTH_VALUES_JSON",json.dumps(randomizer.location_weights.weights)) \
                                                       .replace("SETTINGS_JSON",json.dumps(settings.full_ui_settings)) \
                                                       .replace("SORA_ITEM_JSON",json.dumps(itemSpoilerDictionary(randomizer.assignedItems,randomizer.location_weights), indent=4, cls=ItemEncoder)) \
                                                       .replace("DONALD_ITEM_JSON",json.dumps(itemSpoilerDictionary(randomizer.assignedDonaldItems), indent=4, cls=ItemEncoder))\
                                                       .replace("GOOFY_ITEM_JSON",json.dumps(itemSpoilerDictionary(randomizer.assignedGoofyItems), indent=4, cls=ItemEncoder))\
                                                       .replace("BOSS_ENEMY_JSON",json.dumps(enemySpoilersJSON))
                    html_template = html_template.replace("PromiseCharm","Promise Charm")
                    if not tourney_gen:
                        outZip.writestr("spoilerlog.html",html_template)
                    self.spoiler_log = html_template
                    outZip.write(resource_path("static/KHMenu.otf"), "KHMenu.otf")
                if enemySpoilers:
                    outZip.writestr("enemyspoilers.txt", enemySpoilers)


            mod["assets"] += RandomCmdMenu.randomizeCmdMenus(cmdMenuChoice, outZip, platform)
            mod["assets"] += RandomBGM.randomizeBGM(randomBGMOptions, platform)

            outZip.write(resource_path("Module/icon.png"), "icon.png")
            outZip.writestr("mod.yml", yaml.dump(mod, line_break="\r\n"))
            outZip.close()
        data.seek(0)
        self.outputZip = data

    def createASDataAssets(self,settings,mod,outZip):
        if settings.as_data_split:
            mod["assets"] += modYml.getASDataMod()
            outZip.write(resource_path("static/as_data_split/hb32evt.script"), "asdata/hb32evt.script")
            outZip.write(resource_path("static/as_data_split/hb33evt.script"), "asdata/hb33evt.script")
            outZip.write(resource_path("static/as_data_split/hb34evt.script"), "asdata/hb34evt.script")
            outZip.write(resource_path("static/as_data_split/hb38evt.script"), "asdata/hb38evt.script")

    def createBetterSTTAssets(self,settings,mod,outZip):
        boss_enabled = not settings.enemy_options.get("boss", False) in [False, "Disabled"]
        if settings.roxas_abilities_enabled:
            mod["assets"] += modYml.getBetterSTTMod(boss_enabled)[0]
            for x in mod["assets"]:
                if x["name"]=="03system.bin":
                    x["source"]+=modYml.getBetterSTTMod(boss_enabled)[1]
            outZip.write(resource_path("static/better_stt/cmd.list"), "better_stt/cmd.list")
            outZip.write(resource_path("static/better_stt/trinity_zz.bar"), "better_stt/trinity_zz.bar")
            outZip.write(resource_path("static/better_stt/B_EX100.mset"), "better_stt/B_EX100.mset")
            outZip.write(resource_path("static/better_stt/F_TT010.mset"), "better_stt/F_TT010.mset")
            outZip.write(resource_path("static/better_stt/P_EX110.mset"), "better_stt/P_EX110.mset")
            outZip.write(resource_path("static/better_stt/W_EX010_RX.mset"), "better_stt/W_EX010_RX.mset")
            outZip.write(resource_path("static/better_stt/ObjList_Better_STT.yml"), "better_stt/ObjList_Better_STT.yml")
            if boss_enabled:
                outZip.write(resource_path("static/better_stt/B_EX100_SR.mset"), "better_stt/B_EX100_SR.mset")
    
    def createRetryAssets(self,settings,mod,outZip):
        for fight in settings.retries:
            mod["assets"] += [modYml.getRetryMod(fight)]
            asset_name = modYml.getRetryMod(fight)["source"][0]["source"][0]["name"]
            outZip.write(resource_path("static/"+asset_name),asset_name)


    def createSkipCarpetAssets(self,settings,mod,outZip):
        if settings.skip_carpet_escape:
            mod["assets"] += [modYml.getSkipCarpetEscapeMod()]
            outZip.write(resource_path("static/skip_carpet_escape.script"), "skip_carpet_escape.script")

    def createMapSkipAssets(self,settings,mod,outZip):
        if settings.pr_map_skip:
            mod["assets"] += modYml.getMapSkipMod()
            outZip.write(resource_path("static/map_skip/ca.yml"), "map_skip/ca.yml")
            outZip.write(resource_path("static/map_skip/libretto-ca.bar"), "map_skip/libretto-ca.bar")


    def createPuzzleAssets(self, settings, randomizer, mod, outZip):
        if locationType.Puzzle not in settings.disabledLocations:
            mod["assets"] += [modYml.getPuzzleMod()]
            assignedPuzzles = self.getAssignmentSubsetFromType(randomizer.assignedItems,[locationType.Puzzle])
            with open(resource_path("static/puzzle.bin"), "rb") as puzzleBar:
                binaryContent = bytearray(puzzleBar.read())
                for puzz in assignedPuzzles:
                    byte0 = 20+puzz.location.LocationId*16
                    byte1 = 20+puzz.location.LocationId*16+1
                    item = puzz.item.Id
                        
                    itemByte0, itemByte1 = number_to_bytes(item)
                    binaryContent[byte0] = itemByte0
                    binaryContent[byte1] = itemByte1
                outZip.writestr("modified_puzzle.bin",binaryContent)

    def createSynthAssets(self, settings, randomizer, mod, outZip):
        if locationType.SYNTH in settings.disabledLocations:
            return
        
        assignedSynth = self.getAssignmentSubsetFromType(randomizer.assignedItems,[locationType.SYNTH])

        synth_items = []
        for assignment in assignedSynth:
            synth_items.append(SynthLocation(assignment.location.LocationId,assignment.item.Id,[r for r in randomizer.synthesis_recipes if r.location==assignment.location][0]))

        # if locationType.Puzzle not in settings.disabledLocations:
        mod["assets"] += [modYml.getSynthMod()]
        # assignedPuzzles = self.getAssignmentSubsetFromType(randomizer.assignedItems,[locationType.Puzzle])
        with open(resource_path("static/synthesis.bin"), "rb") as synthbar:
            binaryContent = bytearray(synthbar.read())
            for synth_loc in synth_items:

                starting_byte = synth_loc.getStartingLocation()
                data = synth_loc.getBytes()

                for iter,item in enumerate(data):
                    binaryContent[starting_byte+iter] = 0xFF & item
        
            outZip.writestr("modified_synth.bin",binaryContent)

        with open(resource_path("static/synthesis_reqs.bin"), "rb") as synthbar:
            binaryContent = bytearray(synthbar.read())
            free_dev1 = number_to_bytes(3)
            free_dev2 = number_to_bytes(6)
            binaryContent[36] = free_dev1[0]
            binaryContent[37] = free_dev1[1]
            binaryContent[72] = free_dev2[0]
            binaryContent[73] = free_dev2[1]

            outZip.writestr("modified_synth_reqs.bin",binaryContent)

    def assignStartingItems(self, settings, randomizer):
        def padItems(itemList):
            while(len(itemList)<32):
                itemList.append(0)

        masterItemList = Items.getItemList()
        reports = [i.Id for i in masterItemList if i.ItemType==itemType.REPORT]
        story_unlocks = [i.Id for i in masterItemList if i.ItemType==itemType.STORYUNLOCK]

        donaldStartingItems = [1+0x8000,3+0x8000]+[l.item.Id for l in self.getAssignmentSubsetFromType(randomizer.assignedDonaldItems,[locationType.Free])] + [i for i in settings.startingItems if i in reports]
        padItems(donaldStartingItems)
        self.formattedPlrp.append({
            "Character": 2, # Donald Starting Items
            "Id": 0,
            "Hp": 20,
            "Mp": 100,
            "Ap": settings.donald_ap-5,
            "ArmorSlotMax": 1,
            "AccessorySlotMax": 2,
            "ItemSlotMax": 2,
            "Items": donaldStartingItems,
            "Padding": [0] * 52
        })

        goofyStartingItems = [1+0x8000,1+0x8000,1+0x8000,]+[l.item.Id for l in self.getAssignmentSubsetFromType(randomizer.assignedGoofyItems,[locationType.Free])] + [i for i in settings.startingItems if i in story_unlocks]
        padItems(goofyStartingItems)
        self.formattedPlrp.append({
            "Character": 3, # Goofy Starting Items
            "Id": 0,
            "Hp": 20,
            "Mp": 100,
            "Ap": settings.goofy_ap-4,
            "ArmorSlotMax": 2,
            "AccessorySlotMax": 1,
            "ItemSlotMax": 3,
            "Items": goofyStartingItems,
            "Padding": [0] * 52
        })

        all_party_handled_items = reports+story_unlocks

        soraStartingItems = [l.item.Id for l in self.getAssignmentSubsetFromType(randomizer.assignedItems,[locationType.Critical])] +  [i for i in settings.startingItems if i not in all_party_handled_items]
        padItems(soraStartingItems)
        self.formattedPlrp.append({
            "Character": 1, # Sora Starting Items (Crit)
            "Id": 7, # crit difficulty
            "Hp": 20,
            "Mp": 100,
            "Ap": settings.sora_ap,
            "ArmorSlotMax": 1,
            "AccessorySlotMax": 1,
            "ItemSlotMax": 3,
            "Items": soraStartingItems[:7],
            "Padding": [0] * 52
        })

        lionSoraItems = [32930, 32930, 32931, 32931, 33288, 33289, 33290, 33294]
        padItems(lionSoraItems)
        self.formattedPlrp.append({
            "Character": 135, # Lion Dash on Lion Sora
            "Id": 0,
            "Hp": 0,
            "Mp": 0,
            "Ap": 0,
            "ArmorSlotMax": 0,
            "AccessorySlotMax": 0,
            "ItemSlotMax": 0,
            "Items": lionSoraItems,
            "Padding": [0] * 52
        })
        
        self.formattedPlrp.append({
            "Character": 1, # Sora Starting Items (Non Crit)
            "Id": 0,
            "Hp": 20,
            "Mp": 100,
            "Ap": settings.sora_ap,
            "ArmorSlotMax": 1,
            "AccessorySlotMax": 1,
            "ItemSlotMax": 3,
            "Items": soraStartingItems[7:],
            "Padding": [0] * 52
        })


    def assignWeaponStats(self, randomizer):
        weapons = self.getAssignmentSubset(randomizer.assignedItems,[locationCategory.WEAPONSLOT]) + \
            self.getAssignmentSubset(randomizer.assignedDonaldItems,[locationCategory.WEAPONSLOT]) + \
            self.getAssignmentSubset(randomizer.assignedGoofyItems,[locationCategory.WEAPONSLOT])
        
        for weapon in weapons:
            weaponStats = [stat for stat in randomizer.weaponStats if stat.location==weapon.location][0]
            self.formattedItem["Stats"].append({
                "Id": weapon.location.LocationId,
                "Attack": weaponStats.strength,
                "Magic": weaponStats.magic,
                "Defense": 0,
                "Ability": weapon.item.Id,
                "AbilityPoints": 0,
                "Unknown08": 100,
                "FireResistance": 100,
                "IceResistance": 100,
                "LightningResistance": 100,
                "DarkResistance": 100,
                "Unknown0d": 100,
                "GeneralResistance": 100,
                "Unknown": 0
            })




    def assignFormLevels(self, randomizer):
        formDict = {0:"Summon", 1:"Valor",2:"Wisdom",3:"Limit",4:"Master",5:"Final"}
        for index,levelType in enumerate([locationCategory.SUMMONLEVEL,locationCategory.VALORLEVEL,locationCategory.WISDOMLEVEL,locationCategory.LIMITLEVEL,locationCategory.MASTERLEVEL,locationCategory.FINALLEVEL]):
            levels = self.getAssignmentSubset(randomizer.assignedItems,[levelType])
            formName = formDict[index]
            self.formattedFmlv[formName] = []
            for level_number in range(1,8):
                for lvl in levels:
                    if lvl.location.LocationId == level_number:
                        formExp = [l for l in randomizer.formLevelExp if l == lvl.location][0]
                        self.formattedFmlv[formName].append({
                            "Ability": lvl.item.Id,
                            "Experience": formExp.experience,
                            "FormId": index,
                            "FormLevel": lvl.location.LocationId,
                            "GrowthAbilityLevel": 0,
                        })

    def assignGoofyBonuses(self, randomizer):
        goofyBonuses = self.getAssignmentSubset(randomizer.assignedGoofyItems,[locationCategory.DOUBLEBONUS,locationCategory.HYBRIDBONUS,locationCategory.ITEMBONUS,locationCategory.STATBONUS])
        for bon in goofyBonuses:
            if not bon.location.LocationId in self.formattedBons.keys():
                self.formattedBons[bon.location.LocationId] = {}
            charId = 3 # Goofy id
            charName = "Goofy"
            item1 = 0
            item2 = 0
            item1 = bon.item.Id
            if bon.item2 is not None:
                item2 = bon.item2.Id
            self.formattedBons[bon.location.LocationId][charName] = {
                "RewardId": bon.location.LocationId,
                "CharacterId": charId,
                "HpIncrease": 0,
                "MpIncrease": 0,
                "DriveGaugeUpgrade": 0,
                "ItemSlotUpgrade": 0,
                "AccessorySlotUpgrade": 0,
                "ArmorSlotUpgrade": 0,
                "BonusItem1": item1,
                "BonusItem2": item2,
                "Padding": 0
            }

    def assignDonaldBonuses(self, randomizer):
        donaldBonuses = self.getAssignmentSubset(randomizer.assignedDonaldItems,[locationCategory.DOUBLEBONUS,locationCategory.HYBRIDBONUS,locationCategory.ITEMBONUS,locationCategory.STATBONUS])
        for bon in donaldBonuses:
            if not bon.location.LocationId in self.formattedBons.keys():
                self.formattedBons[bon.location.LocationId] = {}
            charId = 2 # Donald id
            charName = "Donald"
            item1 = 0
            item2 = 0
            item1 = bon.item.Id
            if bon.item2 is not None:
                item2 = bon.item2.Id
            self.formattedBons[bon.location.LocationId][charName] = {
                "RewardId": bon.location.LocationId,
                "CharacterId": charId,
                "HpIncrease": 0,
                "MpIncrease": 0,
                "DriveGaugeUpgrade": 0,
                "ItemSlotUpgrade": 0,
                "AccessorySlotUpgrade": 0,
                "ArmorSlotUpgrade": 0,
                "BonusItem1": item1,
                "BonusItem2": item2,
                "Padding": 0
            }

    def assignSoraBonuses(self, randomizer):
        soraBonuses = self.getAssignmentSubset(randomizer.assignedItems,[locationCategory.DOUBLEBONUS,locationCategory.HYBRIDBONUS,locationCategory.ITEMBONUS,locationCategory.STATBONUS])
        for bon in soraBonuses:
            if not bon.location.LocationId in self.formattedBons.keys():
                self.formattedBons[bon.location.LocationId] = {}
            charId = 1 # Sora id
            charName = "Sora"
            if locationType.STT in bon.location.LocationTypes:
                charId = 14 # roxas id
                charName = "Roxas"

            #determine if assigned item is a stat bonus, and if so, use the bonuses native stat update
            hpIncrease = 0
            mpIncrease = 0
            driveIncrease = 0
            itemIncrease = 0
            accessoryIncrease = 0
            armorIncrease = 0
            item1 = 0
            item2 = 0
            if bon.item.ItemType == itemType.SLOT or bon.item.ItemType == itemType.GAUGE:
                if bon.item.Id == 470: # HP increase
                    hpIncrease+=5
                if bon.item.Id == 471: # MP increase
                    mpIncrease+=10
                if bon.item.Id == 472: # Drive increase
                    driveIncrease+=1
                if bon.item.Id == 473: # Armor increase
                    armorIncrease+=1
                if bon.item.Id == 474: # Accessory increase
                    accessoryIncrease+=1
                if bon.item.Id == 463: # Item increase
                    itemIncrease+=1
            else:
                item1 = bon.item.Id
            if bon.item2 is not None and (bon.item2.ItemType==itemType.SLOT or bon.item2.ItemType == itemType.GAUGE):
                if bon.item2.Id == 470: # HP increase
                    hpIncrease+=5
                if bon.item2.Id == 471: # MP increase
                    mpIncrease+=10
                if bon.item2.Id == 472: # Drive increase
                    driveIncrease+=1
                if bon.item2.Id == 473: # Armor increase
                    armorIncrease+=1
                if bon.item2.Id == 474: # Accessory increase
                    accessoryIncrease+=1
                if bon.item2.Id == 463: # Item increase
                    itemIncrease+=1
            elif bon.item2 is not None:
                item2 = bon.item2.Id


            self.formattedBons[bon.location.LocationId][charName] = {
                "RewardId": bon.location.LocationId,
                "CharacterId": charId,
                "HpIncrease": hpIncrease,
                "MpIncrease": mpIncrease,
                "DriveGaugeUpgrade": driveIncrease,
                "ItemSlotUpgrade": itemIncrease,
                "AccessorySlotUpgrade": accessoryIncrease,
                "ArmorSlotUpgrade": armorIncrease,
                "BonusItem1": item1,
                "BonusItem2": item2,
                "Padding": 0
            }



    def assignLevels(self, settings: RandomizerSettings, randomizer):
        levels = self.getAssignmentSubset(randomizer.assignedItems,[locationCategory.LEVEL])

        # get the triple of items for each level
        items_for_sword_level = {}
        offsets = DreamWeaponOffsets()
        for sword_level in range(1,100):
            sword_item = 0
            shield_item = 0
            staff_item = 0
            shield_level = offsets.get_item_lookup_for_shield(settings.level_checks,sword_level) if settings.split_levels else sword_level
            staff_level = offsets.get_item_lookup_for_staff(settings.level_checks,sword_level) if settings.split_levels else sword_level
            for lvup in levels:
                if lvup.location.LocationId == sword_level:
                    sword_item = lvup.item.Id
                if lvup.location.LocationId == shield_level:
                    shield_item = lvup.item.Id
                if lvup.location.LocationId == staff_level:
                    staff_item = lvup.item.Id
            items_for_sword_level[sword_level] = (sword_item,shield_item,staff_item)


        for lvup in levels:
            levelStats = [lv for lv in randomizer.levelStats if lv.location==lvup.location][0]
            item_id = items_for_sword_level[lvup.location.LocationId]
            self.formattedLvup["Sora"][lvup.location.LocationId] = {
                "Exp": levelStats.experience,
                "Strength": levelStats.strength,
                "Magic": levelStats.magic,
                "Defense": levelStats.defense,
                "Ap": levelStats.ap,
                "SwordAbility": item_id[0],
                "ShieldAbility": item_id[1],
                "StaffAbility": item_id[2],
                "Padding": 0,
                "Character": "Sora",
                "Level": lvup.location.LocationId
            }



    def assignTreasures(self, randomizer):
        treasures = self.getAssignmentSubset(randomizer.assignedItems,[locationCategory.POPUP,locationCategory.CHEST])
        treasures = [trsr for trsr in treasures if locationType.Puzzle not in trsr.location.LocationTypes and locationType.Critical not in trsr.location.LocationTypes and locationType.SYNTH not in trsr.location.LocationTypes]

        for trsr in treasures:
            self.formattedTrsr[trsr.location.LocationId] = {"ItemId":trsr.item.Id}
    
    def getAssignmentSubset(self,assigned,categories : list[locationCategory]):
        return [assignment for assignment in assigned if any(item is assignment.location.LocationCategory for item in categories)]

    def getAssignmentSubsetFromType(self,assigned,types):
        return [assignment for assignment in assigned if any(item in assignment.location.LocationTypes for item in types)]
