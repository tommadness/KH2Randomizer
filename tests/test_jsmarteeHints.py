
import sys
sys.path.append("..")
from Class.locationClass import KH2FormLevel,KH2Treasure
from List.configDict import itemType,locationDepth,locationType
from Module.hints import Hints
from Module.randomize import KH2Randomizer
import unittest


class Tests(unittest.TestCase):
    def test_FirstVisit(self):
        for i in range(30):
            seed = self.createSeed(f"test_seed{i}",[],[],[],[], reportDepth=locationDepth.FirstVisit)
            depths = self.getReportDepths(seed)
            assert locationDepth.SecondVisit not in depths
            assert locationDepth.SecondBoss not in depths
            assert locationDepth.DataFight not in depths
    def test_SecondVisit(self):
        for i in range(30):
            seed = self.createSeed(f"test_seed{i}",[],[],[],[], reportDepth=locationDepth.SecondVisit)
            depths = self.getReportDepths(seed)
            assert locationDepth.DataFight not in depths
    def test_FirstBosses(self):
        for i in range(30):
            seed = self.createSeed(f"test_seed{i}",[],[],[],[], reportDepth=locationDepth.FirstBoss)
            depths = self.getReportDepths(seed)
            assert locationDepth.FirstVisit not in depths
            assert locationDepth.SecondVisit not in depths
            assert locationDepth.SecondBoss not in depths
            assert locationDepth.DataFight not in depths
    def test_SecondBosses(self):
        for i in range(30):
            seed = self.createSeed(f"test_seed{i}",[],[],[],[], reportDepth=locationDepth.SecondBoss)
            depths = self.getReportDepths(seed)
            assert locationDepth.FirstVisit not in depths
            assert locationDepth.SecondVisit not in depths
            assert locationDepth.FirstBoss not in depths
            assert locationDepth.DataFight not in depths

    def test_AllReportsInOneWorld(self):
        # test putting all reports in one world, should fail.
        # All reports in LoD, proofs in AG, DC, and OC
        seed = self.createSeed("test_seed",[226,227,228,229,230,231,232,233,234,235,236,237,238,593,594,595],[245,497,498,350,417,21,121,22,23,122,123,124,125,353,16,7],[],[], reportDepth=None)
        hints = self.getHints(seed)
        assert hints is None

        # All reports in LoD, proofs in LoD, DC, and OC
        seed = self.createSeed("test_seed",[226,227,228,229,230,231,232,233,234,235,236,237,238,593,594,595],[245,497,498,350,417,21,121,22,23,122,123,124,125,131,16,7],[],[], reportDepth=None)
        hints = self.getHints(seed)
        assert hints is None

    def test_AllButOneReportInOneWorld(self):
        # All but one report in LoD, one report in DC, proofs in AG, DC, and OC
        seed = self.createSeed("test_seed",[226,227,228,229,230,231,232,233,234,235,236,237,238,593,594,595],[17,497,498,350,417,21,121,22,23,122,123,124,125,353,16,7],[],[], reportDepth=None)
        hints = self.getHints(seed)
        assert hints is not None
        assert locationType.LoD in self.getHintedWorlds(hints)
        assert locationType.DC in self.getHintedWorlds(hints)
        assert locationType.Agrabah in self.getHintedWorlds(hints)
        assert locationType.OC in self.getHintedWorlds(hints)
        assert self.getHintLocations(hints).count(locationType.LoD)==12
        assert self.getHintLocations(hints).count(locationType.DC)==1

    def test_spreadOutItems(self):
        for i in range(100):
            # create a seed where drives, pages, and magnets/thunders have to be hinted, and try out a bunch of different seeds and make sure we continue to get hints
            seed = self.createSeed(f"test_seed{i}",[593,594],[538,539],[595],[("Final",7)], reportDepth=None)
            hints = self.getHints(seed)
            assert hints is not None

    @staticmethod
    def createSeed(seedName,treasure_items,treasure_locations,form_items,form_locations,reportDepth):
        randomizer = KH2Randomizer(seedName = seedName)
        randomizer.populateLocations([], reportDepth=reportDepth)
        randomizer.populateItems(promiseCharm = True, startingInventory = [], abilityListModifier=None)

        treasures = [location for location in randomizer._validLocationList if isinstance(location,KH2Treasure)]
        formLevels = [location for location in randomizer._validLocationList if isinstance(location,KH2FormLevel)]

        for index, t_loc_id in enumerate(treasure_locations):
            t_location = [loc for loc in treasures if loc.Id==t_loc_id][0]
            t_location.setReward(treasure_items[index])
            item_obj = [obj for obj in randomizer._validItemList if obj.Id==treasure_items[index]][0]
            randomizer._validLocationList.remove(t_location)
            t_location.InvalidChecks.append(itemType.JUNK)
            randomizer._validItemList.remove(item_obj)
            randomizer._locationItems.append((t_location, item_obj))

        for index, f_loc_id in enumerate(form_locations):
            f_location = [loc for loc in formLevels if loc.getFormName()==f_loc_id[0] and loc.FormLevel==f_loc_id[1]][0]
            f_location.setReward(form_items[index])
            item_obj = [obj for obj in randomizer._validItemList if obj.Id==form_items[index]][0]
            randomizer._validLocationList.remove(f_location)
            f_location.InvalidChecks.append(itemType.JUNK)
            randomizer._validItemList.remove(item_obj)
            randomizer._locationItems.append((f_location, item_obj))

        randomizer.setKeybladeAbilities()
        randomizer.setRewards(reportDepth=reportDepth)
        randomizer.setLevels(5,{'0':3, '1':3, '2':3, '3':3, '4':3, '5':3})
        randomizer.setBonusStats()
        return randomizer

    @staticmethod
    def getReportDepths(randomizer):
        return [location.LocationDepth for location,item in randomizer._locationItems if item.ItemType==itemType.REPORT]
    @staticmethod
    def getHints(randomizer):
        hints = Hints.generateHints(randomizer._locationItems, "JSmartee", randomizer.seedName, [])
        if type(hints) is not dict:
            return None
        return hints
    @staticmethod
    def getHintedWorlds(hints):
        worlds = []
        for i in range(1,14):
            worlds.append(hints["Reports"][i]["World"])
        return worlds
    @staticmethod
    def getHintLocations(hints):
        worlds = []
        for i in range(1,14):
            worlds.append(hints["Reports"][i]["Location"])
        return worlds

    @staticmethod
    def getReportLocations(randomizer):
        return [location.LocationTypes[0] for location,item in randomizer._locationItems if item.ItemType==itemType.REPORT]


    @staticmethod
    def getProofLocations(randomizer):
        return [location.LocationTypes[0] for location,item in randomizer._locationItems if item.ItemType==itemType.PROOF or item.ItemType==itemType.PROOF_OF_CONNECTION or item.ItemType==itemType.PROOF_OF_PEACE]

    @staticmethod
    def getFormLocations(randomizer):
        return [location.LocationTypes[0] for location,item in randomizer._locationItems if item.ItemType==itemType.FORM]

    @staticmethod
    def getPageLocations(randomizer):
        return [location.LocationTypes[0] for location,item in randomizer._locationItems if item.ItemType==itemType.TORN_PAGE]

    @staticmethod
    def getMagnetThunderLocations(randomizer):
        return [location.LocationTypes[0] for location,item in randomizer._locationItems if item.ItemType==itemType.MAGNET or item.ItemType==itemType.THUNDER]


ut = Tests()

unittest.main()
