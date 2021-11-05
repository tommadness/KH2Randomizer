
# import sys
# sys.path.append("..")
# from Class.locationClass import KH2FormLevel,KH2Treasure
# from List.configDict import itemType
# from Module.randomize import KH2Randomizer
# from Module.seedEvaluation import SeedValidator
# import unittest


# class Tests(unittest.TestCase):
#     def test_formOnForm(self):
#         # form on level 7 form will fail, and form on itself will fail
#         failing_seed = self.createSeed([],[],[563],[("Valor",7)])
#         failing_seed2 = self.createSeed([],[],[563],[("Limit",2)])
#         passing_seed = self.createSeed([],[],[563],[("Valor",2)])
#         assert self.validateSeed(failing_seed)==False
#         assert self.validateSeed(failing_seed2)==False
#         assert self.validateSeed(passing_seed)==True

#     def test_pageOnForms(self):
#         # page on form, with a form on starry hill will fail if page on level 7
#         failing_seed = self.createSeed([563],[312],[32],[("Valor",7)])
#         passing_seed = self.createSeed([563],[312],[32],[("Valor",2)])
#         assert self.validateSeed(failing_seed)==False
#         assert self.validateSeed(passing_seed)==True

#     def test_pageOnPages(self):
#         # page on starry hill fails, page on spooky cave passes
#         failing_seed = self.createSeed([32],[312],[],[])
#         passing_seed = self.createSeed([32],[110],[],[])
#         assert self.validateSeed(failing_seed)==False
#         assert self.validateSeed(passing_seed)==True

#     def test_thunderOnAtlantica(self):
#         # thunder on last song fails, thunder on Ursula passes
#         failing_seed = self.createSeed([23],[538],[],[])
#         passing_seed = self.createSeed([23],[287],[],[])
#         assert self.validateSeed(failing_seed)==False
#         assert self.validateSeed(passing_seed)==True

#     def test_magnetOnAtlantica(self):
#         # 2 magnets on last song fails, magnet on Ursula passes
#         failing_seed = self.createSeed([87,87],[538,279],[],[])
#         passing_seed = self.createSeed([87],[287],[],[])
#         assert self.validateSeed(failing_seed)==False
#         assert self.validateSeed(passing_seed)==True

#     def test_elementsOnAgrabah(self):
#         # all three of a single elemental magic in AG fails, if two or less, pass
#         failing_seed = self.createSeed([21,21,21],[34,486,303],[],[])
#         failing_seed2 = self.createSeed([22,22,22],[34,486,303],[],[])
#         failing_seed3 = self.createSeed([23,23,23],[34,486,303],[],[])
#         passing_seed = self.createSeed([21,21],[486,303],[],[])
#         passing_seed2 = self.createSeed([22,22],[34,303],[],[])
#         passing_seed3 = self.createSeed([23,23],[34,486],[],[])
#         assert self.validateSeed(failing_seed)==False
#         assert self.validateSeed(failing_seed2)==False
#         assert self.validateSeed(failing_seed3)==False
#         assert self.validateSeed(passing_seed)==True
#         assert self.validateSeed(passing_seed2)==True
#         assert self.validateSeed(passing_seed3)==True

#     @staticmethod
#     def createSeed(treasure_items,treasure_locations,form_items,form_locations):
#         randomizer = KH2Randomizer(seedName = "dummy_name")
#         randomizer.populateLocations([])
#         randomizer.populateItems(promiseCharm = True, startingInventory = [], abilityListModifier=None)

#         treasures = [location for location in randomizer._validLocationList if isinstance(location,KH2Treasure)]
#         formLevels = [location for location in randomizer._validLocationList if isinstance(location,KH2FormLevel)]

#         for index, t_loc_id in enumerate(treasure_locations):
#             t_location = [loc for loc in treasures if loc.Id==t_loc_id][0]
#             t_location.setReward(treasure_items[index])
#             item_obj = [obj for obj in randomizer._validItemList if obj.Id==treasure_items[index]][0]
#             randomizer._validLocationList.remove(t_location)
#             t_location.InvalidChecks.append(itemType.SYNTH)
#             randomizer._validItemList.remove(item_obj)
#             randomizer._locationItems.append((t_location, item_obj))

#         for index, f_loc_id in enumerate(form_locations):
#             f_location = [loc for loc in formLevels if loc.getFormName()==f_loc_id[0] and loc.FormLevel==f_loc_id[1]][0]
#             f_location.setReward(form_items[index])
#             item_obj = [obj for obj in randomizer._validItemList if obj.Id==form_items[index]][0]
#             randomizer._validLocationList.remove(f_location)
#             f_location.InvalidChecks.append(itemType.SYNTH)
#             randomizer._validItemList.remove(item_obj)
#             randomizer._locationItems.append((f_location, item_obj))

#         randomizer.setKeybladeAbilities()
#         randomizer.setRewards()
#         randomizer.setLevels(5,{'0':3, '1':3, '2':3, '3':3, '4':3, '5':3})
#         randomizer.setBonusStats()
#         return randomizer

#     @staticmethod
#     def validateSeed(randomizer):
#         fakeSessionDict = {}
#         fakeSessionDict["seedModifiers"] = []
#         fakeSessionDict["startingInventory"] = []
#         validator = SeedValidator(fakeSessionDict)
#         return validator.validateSeed(fakeSessionDict, randomizer)


# ut = Tests()

# unittest.main()
