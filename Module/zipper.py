import base64
import copy
from doctest import master
import enum
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
from Module.multiworld import MultiWorldOutput
from Module.newRandomize import Randomizer, SynthesisRecipe
from Module.randomCmdMenu import RandomCmdMenu
from Module.resources import resource_path
from Module.seedEvaluation import LocationInformedSeedValidator
from Module.spoilerLog import itemSpoilerDictionary, levelStatsDictionary


def noop(self, *args, **kw):
    pass


def number_to_bytes(item):
    # for byte1, find the most significant bits from the item Id
    itemByte1 = item>>8
    # for byte0, isolate the least significant bits from the item Id
    itemByte0 = item & 0x00FF
    return itemByte0,itemByte1

def bytes_to_number(byte0, byte1=0):
    return int(byte0)+int(byte1<<8)

id_to_enemy_name = {}

id_to_enemy_name[1] = "Soldier"
id_to_enemy_name[2] = "Shadow"
id_to_enemy_name[3] = "Large Body"
id_to_enemy_name[4] = "Armored Knight"
id_to_enemy_name[5] = "Surveillance Robot"
id_to_enemy_name[6] = "Dusk"
id_to_enemy_name[7] = "Trick Ghost"
id_to_enemy_name[8] = "Rabid Dog"
id_to_enemy_name[9] = "Hook Bat"
id_to_enemy_name[10] = "Minute Bomb"
id_to_enemy_name[11] = "Assault Rider"
id_to_enemy_name[12] = "Hammer Frame"
id_to_enemy_name[13] = "Aeroplane"
id_to_enemy_name[14] = "OC Torches"
id_to_enemy_name[15] = "Samurai"
id_to_enemy_name[16] = "OC Bubbles"
id_to_enemy_name[17] = "Rapid Thruster"
id_to_enemy_name[18] = "Bolt Tower"
# id_to_enemy_name[19] = "" # mp only drops
id_to_enemy_name[22] = "Dragoon"
id_to_enemy_name[23] = "Assassin"
id_to_enemy_name[24] = "Sniper"
id_to_enemy_name[25] = "Dancer"
id_to_enemy_name[26] = "Berserker"
id_to_enemy_name[27] = "Gambler"
id_to_enemy_name[28] = "Sorcerer"
id_to_enemy_name[29] = "Creeper"
id_to_enemy_name[30] = "Nightwalker"
id_to_enemy_name[32] = "Fortuneteller"
id_to_enemy_name[33] = "Luna Bandit" #silver rock
id_to_enemy_name[34] = "Hot Rod"
id_to_enemy_name[35] = "Cannon Gun" # tornado step
id_to_enemy_name[36] = "Living Bone"
id_to_enemy_name[37] = "Devastator"
id_to_enemy_name[38] = "Lance Soldier"
id_to_enemy_name[39] = "Driller Mole"
id_to_enemy_name[40] = "Shaman"
id_to_enemy_name[41] = "Neoshadow"
id_to_enemy_name[42] = "Magnum Loader"
id_to_enemy_name[43] = "Morning Star"
id_to_enemy_name[44] = "Tornado Step" #Cannon Gun
id_to_enemy_name[45] = "Gargoyle Knight"
id_to_enemy_name[46] = "Gargoyle Warrior"
id_to_enemy_name[47] = "Silver Rock" #Luna Bandit
id_to_enemy_name[48] = "Wight Knight"
id_to_enemy_name[49] = "Emerald Blues"
id_to_enemy_name[50] = "Crimson Jazz"
id_to_enemy_name[51] = "Crescendo"
id_to_enemy_name[52] = "Creeper Plant"
id_to_enemy_name[53] = "Cerberus RC"
id_to_enemy_name[54] = "Thresholder"
id_to_enemy_name[56] = "Possessor"
id_to_enemy_name[60] = "Lock"
id_to_enemy_name[61] = "Shock"
id_to_enemy_name[62] = "Barrel"
id_to_enemy_name[63] = "Air Pirate"
id_to_enemy_name[64] = "Fat Bandit"
id_to_enemy_name[65] = "Fiery Globe"
id_to_enemy_name[66] = "Icy Cube"
id_to_enemy_name[69] = "Aerial Knocker"
id_to_enemy_name[70] = "Small Urn"
id_to_enemy_name[71] = "Big Urn"
# id_to_enemy_name[72] = "" 100% potion
id_to_enemy_name[73] = "Strafer"
# id_to_enemy_name[74] = ""
# id_to_enemy_name[75] = ""
# id_to_enemy_name[76] = ""
# id_to_enemy_name[77] = ""
# id_to_enemy_name[78] = ""
# id_to_enemy_name[79] = ""
# id_to_enemy_name[80] = ""
# id_to_enemy_name[81] = ""
id_to_enemy_name[82] = "Illuminator"
# id_to_enemy_name[83] = ""
# id_to_enemy_name[84] = ""
id_to_enemy_name[85] = "Shadow Stalker Chandelier"
id_to_enemy_name[86] = "Shadow Stalker Pillar"
id_to_enemy_name[87] = "Undead Pirate A"
id_to_enemy_name[88] = "Undead Pirate B"
id_to_enemy_name[89] = "Undead Pirate C"
id_to_enemy_name[90] = "West Wing Armor"
id_to_enemy_name[91] = "LoD Firework"
id_to_enemy_name[92] = "LoD Rocket"
id_to_enemy_name[93] = "LoD Crate"
# id_to_enemy_name[94] = ""
# id_to_enemy_name[95] = ""
id_to_enemy_name[96] = "Bookmaster"
id_to_enemy_name[97] = "Quickplay (Aladdin)"
id_to_enemy_name[98] = "Quickplay (Sora)"
id_to_enemy_name[99] = "Speedster End"
id_to_enemy_name[100] = "Speedster Start"
id_to_enemy_name[102] = "Hyabusa"
id_to_enemy_name[103] = "Abu Ice Crystal"
# id_to_enemy_name[104] = ""
# id_to_enemy_name[105] = ""
# id_to_enemy_name[106] = ""
id_to_enemy_name[107] = "Water Clone"
id_to_enemy_name[108] = "Aladdin Dash"
id_to_enemy_name[109] = "Pan Attack"
id_to_enemy_name[111] = "Stitch Ukulele"
id_to_enemy_name[112] = "Graveyard/Toy Soldier"
# id_to_enemy_name[114] = ""
id_to_enemy_name[115] = "Lance Soldier Idle Hit"
id_to_enemy_name[116] = "Lance Soldier RC Start"
id_to_enemy_name[117] = "Lance Solder Idle Hit (Double)"
id_to_enemy_name[118] = "Lance Soldier RC End"
id_to_enemy_name[119] = "Dusk (Station)"
id_to_enemy_name[120] = "Dusk (STT)"
id_to_enemy_name[121] = "Creeper (STT)"
id_to_enemy_name[122] = "Hayner (Finisher)"
id_to_enemy_name[123] = "Creeper Plant RC"
id_to_enemy_name[125] = "Crescendo RC"
id_to_enemy_name[126] = "Gambler RC"
# id_to_enemy_name[127] = ""
# id_to_enemy_name[128] = ""
id_to_enemy_name[129] = "Meg"
id_to_enemy_name[130] = "Assassin (STT)"
id_to_enemy_name[131] = "Vivi (Finisher)"
id_to_enemy_name[132] = "Setzer (Finisher)"
id_to_enemy_name[133] = "Luxord Minigame"
id_to_enemy_name[134] = "Card"
# id_to_enemy_name[135] = ""
# id_to_enemy_name[136] = ""
# id_to_enemy_name[137] = ""
id_to_enemy_name[138] = "Bulky Vendor (Stage 1/4)"
id_to_enemy_name[139] = "Bulky Vendor (Stage 2/4)"
id_to_enemy_name[140] = "Bulky Vendor (Stage 3/4)"
id_to_enemy_name[141] = "Bulky Vendor (Stage 4/4)"
id_to_enemy_name[142] = "Bulky Vendor Dying"
# id_to_enemy_name[143] = ""
id_to_enemy_name[144] = "Hydra Head"
id_to_enemy_name[145] = "Dusk (STT Day 1)"
# id_to_enemy_name[146] = ""
id_to_enemy_name[147] = "BC Box"
# id_to_enemy_name[148] = ""
id_to_enemy_name[149] = "Junk Breaking"
id_to_enemy_name[150] = "BEES"
# id_to_enemy_name[151] = ""
id_to_enemy_name[152] = "HT Hazards"
id_to_enemy_name[154] = "Junk Hitting Junk"
id_to_enemy_name[155] = "PR Net Hitting"
id_to_enemy_name[156] = "Odd Mushroom 1"
id_to_enemy_name[157] = "Odd Mushroom 2"
id_to_enemy_name[158] = "Odd Mushroom 3"
id_to_enemy_name[159] = "Odd Mushroom 4"
id_to_enemy_name[160] = "Odd Mushroom 5"
id_to_enemy_name[161] = "Even Mushroom 1"
id_to_enemy_name[162] = "Even Mushroom 2"
id_to_enemy_name[163] = "Even Mushroom 3"
id_to_enemy_name[164] = "Even Mushroom 4"
id_to_enemy_name[165] = "Even Mushroom 5"
id_to_enemy_name[166] = "Mushroom Prize 1"
id_to_enemy_name[167] = "Mushroom Prize 2"
id_to_enemy_name[168] = "Mushroom Prize 3"
id_to_enemy_name[169] = "Mushroom Prize 4"
id_to_enemy_name[170] = "Mushroom Prize 5"

id_to_enemy_name[171] = "Befuddler"
id_to_enemy_name[172] = "Camo Cannon"
id_to_enemy_name[173] = "Aerial Viking"
id_to_enemy_name[174] = "Aerial Champ"
id_to_enemy_name[175] = "Necromancer"
id_to_enemy_name[176] = "Magic Phantom"
id_to_enemy_name[177] = "Spring Metal"
id_to_enemy_name[178] = "Runemaster"
id_to_enemy_name[179] = "Iron Hammer"
id_to_enemy_name[180] = "Lance Warrior"
id_to_enemy_name[181] = "Mad Bumper"
id_to_enemy_name[182] = "Reckless"

id_to_enemy_name[183] = "CoR Drive Orb Hit"
id_to_enemy_name[184] = "CoR Drive Orb Final Hit"
id_to_enemy_name[185] = "Valves"
id_to_enemy_name[186] = "Vexen Anti-Sora"
# id_to_enemy_name[187] = ""
id_to_enemy_name[188] = "Zexion Soothe/Herb/Heal/Mend"
id_to_enemy_name[189] = "Zexion Spirit"
id_to_enemy_name[190] = "Zexion Stamina"
id_to_enemy_name[191] = "Zexion Riches/Wealth"
id_to_enemy_name[192] = "Zexion Jackpot/Bounty"
id_to_enemy_name[193] = "Zexion Treasure/Lucky"
id_to_enemy_name[194] = "Zexion Bonus"
id_to_enemy_name[195] = "Seal Magic Break"
id_to_enemy_name[196] = "Seal Attack Break"
id_to_enemy_name[197] = "Seal Magic Break Final Hit"
id_to_enemy_name[198] = "Seal Attack Break Final Hit"


class SynthList():
    def __init__(self,offset,bytes):
        self.offset = offset
        self.id = bytes_to_number(bytes[0],bytes[1])
        self.reward = bytes_to_number(bytes[2],bytes[3])
        self.reward_type = bytes_to_number(bytes[4])
        self.material_type = bytes_to_number(bytes[5])
        self.material_rank = bytes_to_number(bytes[6])
        self.condition_type = bytes_to_number(bytes[7])
        self.count_needed = bytes_to_number(bytes[8],bytes[9])
        self.unlock_event_shop = bytes_to_number(bytes[10],bytes[11])

    def __str__(self):
        if self.reward_type == 1:
            return f"{self.offset}: {self.reward} {self.condition_type} {self.count_needed}"
        else:
            return ""


class DropRates():
    def __init__(self,offset,bytes):
        self.offset = offset
        self.id = bytes_to_number(bytes[0],bytes[1])
        self.small_hp = bytes_to_number(bytes[2])
        self.big_hp = bytes_to_number(bytes[3])
        self.big_munny = bytes_to_number(bytes[4])
        self.medium_munny = bytes_to_number(bytes[5])
        self.small_munny = bytes_to_number(bytes[6])
        self.small_mp = bytes_to_number(bytes[7])
        self.big_mp = bytes_to_number(bytes[8])
        self.small_drive = bytes_to_number(bytes[9])
        self.big_drive = bytes_to_number(bytes[10])
        self.item1 = bytes_to_number(bytes[12],bytes[13])
        self.item1_chance = bytes_to_number(bytes[14],bytes[15])
        self.item2 = bytes_to_number(bytes[16],bytes[17])
        self.item2_chance = bytes_to_number(bytes[18],bytes[19])
        self.item3 = bytes_to_number(bytes[20],bytes[21])
        self.item3_chance = bytes_to_number(bytes[22],bytes[23])

    def write(self,binary_data):
        id_bytes = number_to_bytes(self.id)
        binary_data[self.offset] = id_bytes[0]
        binary_data[self.offset+1] = id_bytes[1]
        binary_data[self.offset+2] = number_to_bytes(self.small_hp)[0]
        binary_data[self.offset+3] = number_to_bytes(self.big_hp)[0]
        binary_data[self.offset+4] = number_to_bytes(self.big_munny)[0]
        binary_data[self.offset+5] = number_to_bytes(self.medium_munny)[0]
        binary_data[self.offset+6] = number_to_bytes(self.small_munny)[0]
        binary_data[self.offset+7] = number_to_bytes(self.small_mp)[0]
        binary_data[self.offset+8] = number_to_bytes(self.big_mp)[0]
        binary_data[self.offset+9] = number_to_bytes(self.small_drive)[0]
        binary_data[self.offset+10] = number_to_bytes(self.big_drive)[0]
        
        item1_bytes = number_to_bytes(self.item1)
        binary_data[self.offset+12] = item1_bytes[0]
        binary_data[self.offset+13] = item1_bytes[1]
        item1_chances_bytes = number_to_bytes(self.item1_chance)
        binary_data[self.offset+14] = item1_chances_bytes[0]
        binary_data[self.offset+15] = item1_chances_bytes[1]
        
        item2_bytes = number_to_bytes(self.item2)
        binary_data[self.offset+16] = item2_bytes[0]
        binary_data[self.offset+17] = item2_bytes[1]
        item2_chances_bytes = number_to_bytes(self.item2_chance)
        binary_data[self.offset+18] = item2_chances_bytes[0]
        binary_data[self.offset+19] = item2_chances_bytes[1]
        
        item3_bytes = number_to_bytes(self.item3)
        binary_data[self.offset+20] = item3_bytes[0]
        binary_data[self.offset+21] = item3_bytes[1]
        item3_chances_bytes = number_to_bytes(self.item3_chance)
        binary_data[self.offset+22] = item3_chances_bytes[0]
        binary_data[self.offset+23] = item3_chances_bytes[1]

    def __str__(self):
        if True: #self.item1_chance and self.id not in id_to_enemy_name:
            dummy = ""
            return f"{self.id} {(id_to_enemy_name[self.id] if self.id in id_to_enemy_name else dummy)} \n HP ({self.small_hp},{self.big_hp}) \n MP ({self.small_mp},{self.big_mp}) \n Munny ({self.small_munny},{self.medium_munny},{self.big_munny}) \n Orbs ({self.small_drive},{self.big_drive}) Items: \n--- {self.item1} ({self.item1_chance/1.0}%)\n--- {self.item2} ({self.item2_chance/1.0}%)\n--- {self.item3} ({self.item3_chance/1.0}%)"
        elif self.id in id_to_enemy_name:
            return f"{self.id} {id_to_enemy_name[self.id]}"
        else:
            return ""



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
    def __init__(self,settings: RandomizerSettings, randomizer: Randomizer, hints, cosmetics_data, multiworld : MultiWorldOutput = None):
        self.formattedTrsr = {}
        self.formattedLvup = {"Sora":{}}
        self.formattedBons = {}
        self.formattedFmlv = {}
        self.formattedItem = {"Stats":[]}
        self.formattedPlrp = []
        self.spoiler_log = None
        self.enemy_log = None

        self.assignTreasures(randomizer)
        self.assignLevels(settings,randomizer)
        self.assignSoraBonuses(randomizer)
        self.assignDonaldBonuses(randomizer)
        self.assignGoofyBonuses(randomizer)
        self.assignFormLevels(randomizer)
        self.assignWeaponStats(randomizer)
        self.assignStartingItems(settings, randomizer)
        for i in range(5):
            if self.createZip(settings, randomizer, hints, cosmetics_data, multiworld):
                return
        raise BossEnemyException(f"Boss/enemy module had an unexpected error. Try different a different seed or different settings.")

    def createZip(self, settings: RandomizerSettings, randomizer : Randomizer, hints, cosmetics_data, multiworld):

        mod = modYml.getDefaultMod()
        sys = modYml.getSysYAML(settings.seedHashIcons,settings.crit_mode)

        data = io.BytesIO()
        with zipfile.ZipFile(data,"w") as outZip:
            yaml.emitter.Emitter.process_tag = noop

            cmdMenuChoice = cosmetics_data["cmdMenuChoice"]
            platform = cosmetics_data["platform"]
            tourney_gen = cosmetics_data["tourney"]
            
            pc_seed_toggle = (platform=="PC")


            def _shouldRunKHBR():
                if not settings.enemy_options.get("boss", False) in [False, "Disabled"]:
                    return True
                if not settings.enemy_options.get("enemy", False) in [False, "Disabled"]:
                    return True
                if settings.enemy_options.get("remove_damage_cap", False):
                    return True
                if settings.enemy_options.get("cups_give_xp", False):
                    return True
                if settings.enemy_options.get("retry_data_final_xemnas", False):
                    return True
                if settings.enemy_options.get("retry_dark_thorn", False):
                    return True

                return False

            enemySpoilers = None
            enemySpoilersJSON = {}
            if _shouldRunKHBR():
                # load in known crashing combinations
                enemySpoilers = None
                enemySpoilersJSON = {}
                try:
                    if platform == "PC":
                        settings.enemy_options["memory_expansion"] = True
                    else:
                        settings.enemy_options["memory_expansion"] = False
                    
                    from khbr.randomizer import Randomizer as khbr
                    enemySpoilers = khbr().generateToZip("kh2", settings.enemy_options, mod, outZip)

                    if pc_seed_toggle:
                        # TODO: Remove this modification when khbr is changed to handle multi-languages
                        for asset in mod["assets"]:
                            if "msn/jp" in asset["name"] and ".bar" in asset["name"]:
                                asset["multi"] = []
                                for region in ["us","fr","gr","it","sp","uk"]:
                                    asset["multi"].append({'name':asset["name"].replace("jp",region)})
                            elif "ard/us" in asset["name"]:
                                asset["multi"] = []
                                for region in ["jp","fr","gr","it","sp","uk"]:
                                    asset["multi"].append({'name':asset["name"].replace("us",region)})


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
                    if enemySpoilersJSON:
                        outZip.writestr("enemies.rando", base64.b64encode(json.dumps(enemySpoilersJSON).encode('utf-8')).decode('utf-8'))
                        # for boss_replacement in enemySpoilersJSON["BOSSES"]:
                        #     print(f"{boss_replacement['original']} {boss_replacement['new']}")
                except Exception as e:
                    print(f"{e}")
                    return False
                    # raise BossEnemyException(f"Boss/enemy module had an unexpected error {e}. Try different a different seed or different settings.")

            print("Passed boss/enemy")

            if multiworld:
                outZip.writestr("multiworld.multi", json.dumps(multiworld()))

            self.createPuzzleAssets(settings, randomizer, mod, outZip, pc_seed_toggle)
            self.createSynthAssets(settings, randomizer, mod, outZip, pc_seed_toggle)
            self.createASDataAssets(settings, mod, outZip)
            self.createSkipCarpetAssets(settings, mod, outZip)
            self.createMapSkipAssets(settings, mod, outZip)
            self.createBlockingSkipAssets(settings, mod, outZip)
            self.createAtlanticaSkipAssets(settings, mod, outZip)
            self.createWardrobeSkipAssets(settings, mod, outZip)
            self.createDropRateAssets(settings, randomizer, mod, outZip)
            self.createShopRandoAssets(settings, randomizer, mod, outZip, sys)

            outZip.writestr("TrsrList.yml", yaml.dump(self.formattedTrsr, line_break="\r\n"))
            outZip.writestr("BonsList.yml", yaml.dump(self.formattedBons, line_break="\r\n"))
            outZip.writestr("LvupList.yml", yaml.dump(self.formattedLvup, line_break="\r\n"))
            outZip.writestr("FmlvList.yml", yaml.dump(self.formattedFmlv, line_break="\r\n"))
            outZip.writestr("ItemList.yml", yaml.dump(self.formattedItem, line_break="\r\n"))
            outZip.writestr("PlrpList.yml", yaml.dump(self.formattedPlrp, line_break="\r\n"))
            outZip.writestr("sys.yml", yaml.dump(sys, line_break="\r\n"))

            if hints is not None:
                Hints.writeHints(hints, "HintFile", outZip)

            self.createBetterSTTAssets(settings, mod, outZip)
            self.addCmdListModifications(settings, mod, outZip)
            
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
                                                       .replace("SORA_ITEM_JSON",json.dumps(itemSpoilerDictionary(randomizer.assignedItems,randomizer.location_weights,LocationInformedSeedValidator().validateSeed(settings, randomizer, False)), indent=4, cls=ItemEncoder)) \
                                                       .replace("DONALD_ITEM_JSON",json.dumps(itemSpoilerDictionary(randomizer.assignedDonaldItems), indent=4, cls=ItemEncoder))\
                                                       .replace("GOOFY_ITEM_JSON",json.dumps(itemSpoilerDictionary(randomizer.assignedGoofyItems), indent=4, cls=ItemEncoder))\
                                                       .replace("BOSS_ENEMY_JSON",json.dumps(enemySpoilersJSON))
                    html_template = html_template.replace("PromiseCharm","Promise Charm")
                    if not tourney_gen:
                        outZip.writestr("spoilerlog.html",html_template)
                    self.spoiler_log = html_template
                    self.enemy_log = enemySpoilers
                    outZip.write(resource_path("static/KHMenu.otf"), "KHMenu.otf")
                if enemySpoilers and not tourney_gen:
                    outZip.writestr("enemyspoilers.txt", enemySpoilers)


            mod["assets"] += RandomCmdMenu.randomizeCmdMenus(cmdMenuChoice, outZip, platform)

            outZip.write(resource_path("Module/icon.png"), "icon.png")
            outZip.writestr("mod.yml", yaml.dump(mod, line_break="\r\n"))
            outZip.close()
        data.seek(0)
        self.outputZip = data
        return True

    def addCmdListModifications(self,settings,mod,outZip):
        with open(resource_path("static/better_stt/cmd.list"), "rb") as cmdlist:
            binaryContent = bytearray(cmdlist.read())

            if not settings.roxas_abilities_enabled:
                # better stt 0x93, vanilla 0xB7
                binaryContent[0x3345] = 0xB7
                binaryContent[0x3375] = 0xB7
                binaryContent[0x33A5] = 0xB7
            if settings.disable_final_form:
                # disable final form 0x0A, vanilla 0x5
                binaryContent[0x234] = 0x0A
                binaryContent[0x6234] = 0x0A
            outZip.writestr("better_stt/cmd.list",binaryContent)

        for x in mod["assets"]:
            if x["name"]=="03system.bin":
                x["source"]+=modYml.getCmdListMod()


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
            mod["assets"] += modYml.getBetterSTTMod(boss_enabled)
            outZip.write(resource_path("static/better_stt/trinity_zz.bar"), "better_stt/trinity_zz.bar")
            outZip.write(resource_path("static/better_stt/B_EX100.mset"), "better_stt/B_EX100.mset")
            outZip.write(resource_path("static/better_stt/F_TT010.mset"), "better_stt/F_TT010.mset")
            outZip.write(resource_path("static/better_stt/P_EX110.mset"), "better_stt/P_EX110.mset")
            outZip.write(resource_path("static/better_stt/W_EX010_RX.mset"), "better_stt/W_EX010_RX.mset")
            # outZip.write(resource_path("static/better_stt/ObjList_Better_STT.yml"), "better_stt/ObjList_Better_STT.yml")
            if boss_enabled:
                outZip.write(resource_path("static/better_stt/B_EX100_SR.mset"), "better_stt/B_EX100_SR.mset")
    
    def createSkipCarpetAssets(self,settings,mod,outZip):
        if settings.skip_carpet_escape:
            mod["assets"] += [modYml.getSkipCarpetEscapeMod()]
            outZip.write(resource_path("static/skip_carpet_escape.script"), "skip_carpet_escape.script")

    def createAtlanticaSkipAssets(self,settings,mod,outZip):
        if settings.atlantica_skip:
            mod["assets"] += [modYml.getAtlanticaTutorialSkipMod()]
            outZip.write(resource_path("static/atlantica_skip.script"), "atlantica_skip.script")

    def createWardrobeSkipAssets(self,settings,mod,outZip):
        if settings.wardrobe_skip:
            mod["assets"] += [modYml.getWardrobeSkipMod()]
            outZip.write(resource_path("static/wardrobe/N_BB080_BTL.mset"), "wardrobe_skip.mset")

    def createBlockingSkipAssets(self,settings,mod,outZip):
        if settings.block_cor_skip:
            mod["assets"] += [modYml.getBlockCorSkipMod()]
            outZip.write(resource_path("static/disable_cor_skip.script"), "disable_cor_skip.script")
        if settings.block_shan_yu_skip:
            mod["assets"] += [modYml.getBlockShanYuSkipMod()]
            outZip.write(resource_path("static/disable_shan_yu_skip.script"), "disable_shan_yu_skip.script")

    def createMapSkipAssets(self,settings,mod,outZip):
        if settings.pr_map_skip:
            mod["assets"] += modYml.getMapSkipMod()
            outZip.write(resource_path("static/map_skip/ca.yml"), "map_skip/ca.yml")
            outZip.write(resource_path("static/map_skip/libretto-ca.bar"), "map_skip/libretto-ca.bar")


    def createPuzzleAssets(self, settings, randomizer, mod, outZip, pc_toggle):
        if locationType.Puzzle not in settings.disabledLocations:
            mod["assets"] += [modYml.getPuzzleMod(pc_toggle)]
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

                
    def createDropRateAssets(self, settings, randomizer, mod, outZip):
        global_jackpot = settings.global_jackpot
        global_lucky_lucky = settings.global_lucky
        fast_urns = settings.fast_urns
        rich_enemies = settings.rich_enemies
        near_unlimited_mp = settings.unlimited_mp

        if global_jackpot>0 or global_lucky_lucky>0 or fast_urns or rich_enemies or near_unlimited_mp:
            for x in mod["assets"]:
                if x["name"]=="00battle.bin":
                    x["source"].append(modYml.getDropMod())
            all_drops = {}
            testing = []
            with open(resource_path("static/drops.bin"), "rb") as dropsbar:
                binaryContent = bytearray(dropsbar.read())
                for i in range(0,184):
                    start_index = 8+24*i
                    rate = DropRates(start_index,binaryContent[start_index:start_index+24])
                    all_drops[rate.id] = rate

                    if rate.id not in id_to_enemy_name:
                        testing.append(rate.id)


            spawnable_enemy_ids = [1,2,3,4,5,6,7,8,9,10,11,12,13,15,17,18,22,23,24,25,26,27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,63,64,65,66,69,73,87,88,89,96,112,171,172,173,174,175,176,177,178,179,180,181,182]
            urn_ids = [70,71]
            stt_enemies = [119,120,121,130,145]
            struggles = [122,131,132]

            if rich_enemies: 
                for drop in all_drops.values():
                    if drop.id in spawnable_enemy_ids:
                        drop.medium_munny = max(drop.medium_munny,2)
                        drop.small_munny = max(drop.small_munny,2)
            if near_unlimited_mp: 
                for drop in all_drops.values():
                    if drop.id in spawnable_enemy_ids:
                        drop.big_mp = max(drop.big_mp,5)
                        drop.small_mp = max(drop.small_mp,5)

            if global_lucky_lucky > 0: 
                for drop in all_drops.values():
                    if drop.item1 != 0:
                        drop.item1_chance = min(drop.item1_chance + (drop.item1_chance//2)*global_lucky_lucky,100)
                    if drop.item2 != 0:
                        drop.item2_chance = min(drop.item2_chance + (drop.item2_chance//2)*global_lucky_lucky,100)
                    if drop.item3 != 0:
                        drop.item3_chance = min(drop.item3_chance + (drop.item3_chance//2)*global_lucky_lucky,100)
            if global_jackpot > 0: 
                for drop in all_drops.values():
                    drop.small_hp = min(drop.small_hp + (drop.small_hp//2)*global_jackpot,64)
                    drop.big_hp = min(drop.big_hp + (drop.big_hp//2)*global_jackpot,64)
                    drop.big_munny = min(drop.big_munny + (drop.big_munny//2)*global_jackpot,64)
                    drop.medium_munny = min(drop.medium_munny + (drop.medium_munny//2)*global_jackpot,64)
                    drop.small_munny = min(drop.small_munny + (drop.small_munny//2)*global_jackpot,64)
                    drop.small_mp = min(drop.small_mp + (drop.small_mp//2)*global_jackpot,64)
                    drop.big_mp = min(drop.big_mp + (drop.big_mp//2)*global_jackpot,64)
                    drop.small_drive = min(drop.small_drive + (drop.small_drive//2)*global_jackpot,64)
                    drop.big_drive = min(drop.big_drive + (drop.big_drive//2)*global_jackpot,64)

            if fast_urns:
                for u in urn_ids:
                    all_drops[u].big_hp = 64


            # write changes
            with open(resource_path("static/drops.bin"), "rb") as dropsbar:
                binaryContent = bytearray(dropsbar.read())
                for drop in all_drops:
                    all_drops[drop].write(binaryContent)
                outZip.writestr("modified_drops.bin",binaryContent)

    def createShopRandoAssets(self, settings, randomizer, mod, outZip, sys):
        if len(randomizer.shop_items)>0 or settings.shop_keyblades:
            for x in mod["assets"]:
                if x["name"]=="03system.bin":
                    x["source"].append(modYml.getShopMod())

            items_for_shop = []
            keyblade_item_ids = [42,43,480,481,484,485,486,487,488,489,490,491,492,493,494,495,496,497,498,499,500,543,544] if settings.shop_keyblades else []
            report_item_ids = [i.Id for i in randomizer.shop_items if i.ItemType==itemType.REPORT]#[226,227,228,229,230,231,232,233,234,235,236,237,238]
            story_unlock_ids = [i.Id for i in randomizer.shop_items if i.ItemType==itemType.STORYUNLOCK]#[54,55,59,60,61,62,72,74,369,375,376]

            remaining_items = [i for i in randomizer.shop_items if i not in keyblade_item_ids+report_item_ids+story_unlock_ids]

            if len(keyblade_item_ids)>0: 
                for i in keyblade_item_ids:
                    items_for_shop.append((i,400))

            if len(report_item_ids)>0:
                for i in report_item_ids:
                    items_for_shop.append((i,500))
                for i in range(13):
                    sys.append({"id":46778-32768+i*2,"en":f"Ansem Report {i+1}"})

            if len(story_unlock_ids)>0:
                for i in story_unlock_ids:
                    items_for_shop.append((i,4000))

            price_map = {itemRarity.COMMON:100,itemRarity.UNCOMMON:300, itemRarity.RARE:500, itemRarity.MYTHIC:1000}

            if len(remaining_items)>0:
                for i in remaining_items:
                    items_for_shop.append((i.Id,price_map[i.Rarity]))
        

            with open(resource_path("static/full_items.json"), "r") as itemjson:
                all_item_jsons = json.loads(itemjson.read())
                self.formattedItem["Items"] = []
                for x,price in items_for_shop:
                    item_json = None
                    for y in all_item_jsons["Items"]:
                        if y["Id"]==x:
                            item_json = y
                            break
                    item_json["ShopBuy"]=price
                    self.formattedItem["Items"].append(item_json)


            with open(resource_path("static/shop.bin"), "rb") as shopbar:
                binaryContent = bytearray(shopbar.read())

                byte0,byte1 = number_to_bytes(80+len(items_for_shop))
                binaryContent[10] = byte0
                binaryContent[11] = byte1

                byte0,byte1 = number_to_bytes(len(items_for_shop))

                # inventory 752
                binaryContent[754] = byte0
                binaryContent[755] = byte1
                byte0,byte1 = number_to_bytes(984)
                binaryContent[756] = byte0
                binaryContent[757] = byte1


                valid_start = bytes_to_number(binaryContent[12],binaryContent[13])
                for x in range(len(items_for_shop)):
                    product_index = 984+2*x
                    valid_item_index = valid_start + (60+x)*2
                    byte0,byte1 = number_to_bytes(items_for_shop[x][0])
                    binaryContent[product_index] = byte0
                    binaryContent[product_index+1] = byte1
                    binaryContent[valid_item_index] = byte0
                    binaryContent[valid_item_index+1] = byte1
                
                outZip.writestr("modified_shop.bin",binaryContent)

                ### code below prints out the shop information in relevant format

                # print(f"file type: {bytes_to_number(binaryContent[4],binaryContent[5])}")
                # shop_list_count = bytes_to_number(binaryContent[6],binaryContent[7])
                # print(f"shop list count: {shop_list_count}")
                # inventory_list_count = bytes_to_number(binaryContent[8],binaryContent[9])
                # print(f"inventory entry count: {inventory_list_count}")
                # product_list_count = bytes_to_number(binaryContent[10],binaryContent[11])
                # print(f"product entry count: {product_list_count}")
                # valid_start = bytes_to_number(binaryContent[12],binaryContent[13])
                # print(f"valid items offset: {valid_start}")
                
                # shop_start = 16
                # print("Shop Entries")
                # for x in range(shop_list_count):
                #     shop_index = shop_start+x*24
                #     print(f"---- Shop ID: {bytes_to_number(binaryContent[shop_index+18])}")
                #     print(f"---- Inventory Amount: {bytes_to_number(binaryContent[shop_index+16],binaryContent[shop_index+17])}")
                #     print(f"---- Inventory Offset: {bytes_to_number(binaryContent[shop_index+20],binaryContent[shop_index+21])}")
                #     print("----------")

                # inventory_start = shop_start+shop_list_count*24
                # print("Inventory Entries")
                # for x in range(inventory_list_count):
                #     inventory_index = inventory_start+x*8
                #     print(f"---- Inventory Address: {inventory_index}")
                #     print(f"---- Unlock event: {bytes_to_number(binaryContent[inventory_index],binaryContent[inventory_index+1])}")
                #     print(f"---- Product Amount: {bytes_to_number(binaryContent[inventory_index+2],binaryContent[inventory_index+3])}")
                #     print(f"---- Product Offset: {bytes_to_number(binaryContent[inventory_index+4],binaryContent[inventory_index+5])}")
                #     print("----------")

                # product_start = inventory_start+inventory_list_count*8
                # print("Product Entries")
                # for x in range(product_list_count):
                #     product_index = product_start+x*2
                #     print(f"---- Address {product_index}")
                #     print(f"---- Product (Item Id):  {bytes_to_number(binaryContent[product_index],binaryContent[product_index+1])}")

                # print("Valid Items")
                # for x in range(63):
                #     valid_index = valid_start+x*2
                #     item_id = bytes_to_number(binaryContent[valid_index],binaryContent[valid_index+1])
                #     if item_id!=0:
                #         print(f"---- Valid Item (Item Id):  {item_id}")

    def createSynthAssets(self, settings, randomizer, mod, outZip, pc_toggle):
        if locationType.SYNTH in settings.disabledLocations:
            return
        
        assignedSynth = self.getAssignmentSubsetFromType(randomizer.assignedItems,[locationType.SYNTH])

        synth_items = []
        for assignment in assignedSynth:
            synth_items.append(SynthLocation(assignment.location.LocationId,assignment.item.Id,[r for r in randomizer.synthesis_recipes if r.location==assignment.location][0]))

        # if locationType.Puzzle not in settings.disabledLocations:
        mod["assets"] += [modYml.getSynthMod(pc_toggle)]
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

            # uncomment to see some data about the synth lists
            # index=16
            # while index+12<len(binaryContent):
            #     print(SynthList(index,binaryContent[index:]))
            #     index+=12

            free_dev1 = number_to_bytes(3)
            free_dev2 = number_to_bytes(6)
            binaryContent[36] = free_dev1[0]
            binaryContent[37] = free_dev1[1]
            binaryContent[72] = free_dev2[0]
            binaryContent[73] = free_dev2[1]

            # uncomment to make all existing synth buyable conditions need 7 of that material
            # new_required_items = number_to_bytes(7)
            # start_index=376
            # for i in range(0,24):
            #     binaryContent[start_index+i*12+8] = new_required_items[0]
            #     binaryContent[start_index+i*12+9] = new_required_items[1]

            outZip.writestr("modified_synth_reqs.bin",binaryContent)

    def assignStartingItems(self, settings, randomizer):
        def padItems(itemList):
            while(len(itemList)<32):
                itemList.append(0)

        masterItemList = Items.getItemList() + Items.getActionAbilityList() + Items.getSupportAbilityList() + [Items.getTT1Jailbreak()] + [Items.getPromiseCharm()]
        reports = [i.Id for i in masterItemList if i.ItemType==itemType.REPORT]
        story_unlocks = [i.Id for i in masterItemList if i.ItemType==itemType.STORYUNLOCK]
        donald_goofy_handled_items = reports+story_unlocks
        sora_abilities = [i.Id for i in masterItemList if (i.ItemType==itemType.GROWTH_ABILITY or i.ItemType==itemType.ACTION_ABILITY or i.ItemType==itemType.SUPPORT_ABILITY)]

        riku_handled = [i.Id for i in masterItemList if i.Id not in donald_goofy_handled_items and i.Id not in sora_abilities]

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

        rikuStartingItems = [i+0x8000 for i in [1,1,1,1,3,3,438,436,187,208,411,422,414,415,416]] + [417,419] + [i for i in settings.startingItems if i in riku_handled]
        padItems(rikuStartingItems)
        self.formattedPlrp.append({
            "Character": 13, # Riku Starting Items
            "Id": 0,
            "Hp": 20,
            "Mp": 100,
            "Ap": settings.goofy_ap-4,
            "ArmorSlotMax": 2,
            "AccessorySlotMax": 1,
            "ItemSlotMax": 6,
            "Items": rikuStartingItems,
            "Padding": [0] * 52
        })

        ability_equip = 0x8000 if settings.auto_equip_abilities else 0

        soraStartingItems = [l.item.Id for l in self.getAssignmentSubsetFromType(randomizer.assignedItems,[locationType.Critical])] +  [i+ability_equip for i in settings.startingItems if i in sora_abilities]
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
