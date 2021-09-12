
import sys
sys.path.append("..")
from Class.locationClass import KH2FormLevel,KH2Treasure
from List.configDict import itemType,locationDepth,locationType
from Module.hints import Hints
from Module.modifier import SeedModifier
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
        # test putting all reports in one world, should always fail.
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
        self.sanityReportChecks(seed,hints)

    def test_spreadOutItems(self):
        for i in range(100):
            # create a seed where drives, pages, and magnets/thunders have to be hinted, and try out a bunch of different seeds and make sure we continue to get hints
            seed = self.createSeed(f"test_seed{i}",[593,594],[538,539],[595],[("Final",7)], reportDepth=None)
            hints = self.getHints(seed)
            locations_of_reports = list(set(self.getReportLocations(seed)))
            self.sanityReportChecks(seed,hints)

    def test_FirstVisit(self):
        for i in range(50):
            seed = self.createSeed(f"test_FirstVisit{i}",[],[],[],[], reportDepth=locationDepth.FirstVisit)
            hints = self.getHints(seed)
            self.sanityReportChecks(seed,hints)

    def test_SecondVisit(self):
        for i in range(50):
            seed = self.createSeed(f"test_SecondVisit{i}",[],[],[],[], reportDepth=locationDepth.SecondVisit)
            hints = self.getHints(seed)
            self.sanityReportChecks(seed,hints)

    def test_FirstBoss(self):
        for i in range(50):
            seed = self.createSeed(f"test_FirstBoss{i}",[],[],[],[], reportDepth=locationDepth.FirstBoss)
            hints = self.getHints(seed)
            self.sanityReportChecks(seed,hints)

    def test_SecondBoss(self):
        for i in range(50):
            seed = self.createSeed(f"test_SecondBoss{i}",[],[],[],[], reportDepth=locationDepth.SecondBoss)
            hints = self.getHints(seed)
            self.sanityReportChecks(seed,hints)

    def test_RegularJSmartee(self):
        for i in range(50):
            seed = self.createSeed(f"test_RegularJSmartee{i}",[],[],[],[], reportDepth=None)
            hints = self.getHints(seed)
            self.sanityReportChecks(seed,hints)


    def test_LibraryOfAssemblage(self):
        for i in range(50):
            seed = self.createSeed(f"test_LibraryOfAssemblage{i}",[],[],[],[], reportDepth=None, library=True)
            hints = self.getHints(seed)
            self.sanityReportChecks(seed,hints)

    def test_goMode(self):
        for i in range(50):
            seed = self.createSeed(f"test_goMode{i}",[],[],[],[], reportDepth=None, library=False, goMode=True )
            hints = self.getHints(seed)
            self.sanityReportChecks(seed,hints)

    def test_LibraryGoMode(self):
        for i in range(50):
            seed = self.createSeed(f"test_LibraryGoMode{i}",[],[],[],[], reportDepth=None, library=True, goMode=True )
            hints = self.getHints(seed)
            self.sanityReportChecks(seed,hints)

    def test_howManySelfHintedReportSeeds(self):
        self_hinted_count = 0
        for i in range(50):
            seed = self.createSeed(f"test_howManySelfHintedReportSeeds{i}",[],[],[],[], reportDepth=None)
            hints = self.getHints(seed,preventSelfHinted=False)
            if self.areThereSelfHintedReports(hints):
                self_hinted_count+=1
        print(self_hinted_count)



    @staticmethod
    def createSeed(seedName,treasure_items,treasure_locations,form_items,form_locations,reportDepth,library=False,goMode=False):
        randomizer = KH2Randomizer(seedName = seedName)
        randomizer.populateLocations([], reportDepth=reportDepth)
        randomizer.populateItems(promiseCharm = True, startingInventory = [SeedModifier.library(library)] + (["593","594","595"] if goMode else []), abilityListModifier=None)

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
    def sanityReportChecks(randomizer,hints):
        Tests.proofsHinted(randomizer,hints)
        Tests.proofReportsHinted(randomizer,hints)
        Tests.noSelfHintedReports(hints)
        Tests.auxHintTests(randomizer,hints)

    @staticmethod
    def proofsHinted(randomizer,hints):
        proofs = Tests.getProofLocations(randomizer)
        hinted_worlds = Tests.getHintedWorlds(hints)
        hinted_worlds.append(locationType.Critical)
        hinted_worlds.append(locationType.Free)
        for p_loc in proofs:
            assert p_loc in hinted_worlds, f"Proof was not hinted: proof location {p_loc}"

    @staticmethod
    def proofReportsHinted(randomizer,hints):
        proofs = Tests.getProofLocations(randomizer)
        hinted_worlds = Tests.getHintedWorlds(hints)
        hinted_worlds.append("Critical")
        reportLocations = Tests.getHintLocationsForLocations(hints,proofs)
        trueReportLocations = Tests.getReportLocations(randomizer)
        for r_loc in reportLocations:
            assert r_loc in hinted_worlds, f"Report in {r_loc} for a proof was not hinted when proofs are in {proofs} and proof reports are in {reportLocations}"

    @staticmethod
    def noSelfHintedReports(hints):
        hinted_worlds = Tests.getHintedWorlds(hints)
        hint_locations = Tests.getHintLocations(hints)
        for i in range(13):
            assert hinted_worlds[i] != hint_locations[i], f"A report was self hinted {hinted_worlds[i]} {hint_locations[i]}"

    @staticmethod
    def areThereSelfHintedReports(hints):
        hinted_worlds = Tests.getHintedWorlds(hints)
        hint_locations = Tests.getHintLocations(hints)
        selfHinted = False
        for i in range(13):
            selfHinted |= hinted_worlds[i] == hint_locations[i]
        return selfHinted


    @staticmethod
    def auxHintTests(randomizer,hints):
        proofs = Tests.getProofLocations(randomizer)
        hinted_worlds = Tests.getHintedWorlds(hints) + [locationType.Critical,locationType.Free]

        form_proof = False
        pooh_proof = False
        atl_proof = False
        drives = []
        pages = []
        thunders = []
        magnets = []
        if locationType.FormLevel in proofs:
            form_proof = True
            # test for drives being hinted
            drives = Tests.getForms(randomizer)
            for d in drives:
                assert d in hinted_worlds, f"A drive wasn't hinted for a drive proof \nDrives: {drives} HintedWorlds: {hinted_worlds}"
        if locationType.HUNDREDAW in proofs:
            pooh_proof = True
            # test for pages being hinted
            pages = Tests.getPages(randomizer)
            for p in pages:
                assert p in hinted_worlds, f"A page wasn't hinted for a 100 acre proof \nPages: {pages} HintedWorlds: {hinted_worlds}"
        if locationType.Atlantica in proofs:
            # okay, so based on priorities, the point where things may not get hinted comes from atlantica, 
            #       since even if all checks are in different locations
            #                       3 proofs  +   5 drives    +    5 pages      =   max 13 hints
            #       now, if the thunders and magnets go outside those worlds, we have to be flexible
            already_hinted_locations = list(set(proofs+drives+pages))

            # test for magnets and thunders being hinted
            thunders = Tests.getThunders(randomizer)
            adding_thunders = list(set(already_hinted_locations+thunders))
            if len(adding_thunders) <= 13:
                for m in thunders:
                    assert m in hinted_worlds, f"A thunder wasn't hinted for an Atlantica proof \nThunders: {thunders} HintedWorlds: {hinted_worlds}"

            magnets = Tests.getMagnets(randomizer)
            adding_magnets = list(set(adding_thunders+magnets))
            if len(adding_magnets) <= 13:
                for m in magnets:
                    assert m in hinted_worlds, f"A magnet wasn't hinted for an Atlantica proof \nMagnets: {magnets} HintedWorlds: {hinted_worlds}"

    @staticmethod
    def getReportDepths(randomizer):
        return [location.LocationDepth for location,item in randomizer._locationItems if item.ItemType==itemType.REPORT]
    @staticmethod
    def getHints(randomizer, preventSelfHinted=True):
        hints = Hints.generateHints(randomizer._locationItems, "JSmartee", randomizer.seedName, [], preventSelfHinted)
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
            loc = hints["Reports"][i]["Location"]
            if loc == "":
                loc = "Critical"
            worlds.append(loc)
        return worlds
    @staticmethod 
    def getHintLocationsForLocations(hints, locations):
        worlds = []
        for i in range(1,14):
            if hints["Reports"][i]["World"] in locations:
                loc = hints["Reports"][i]["Location"]
                if loc == "":
                    loc = "Critical"
                worlds.append(loc)
        return worlds

    @staticmethod
    def getProofLocations(randomizer):
        return [location.LocationTypes[0] for location,item in randomizer._locationItems if item.ItemType==itemType.PROOF or item.ItemType==itemType.PROOF_OF_CONNECTION or item.ItemType==itemType.PROOF_OF_PEACE]

    @staticmethod
    def getReportLocations(randomizer):
        return [location.LocationTypes[0] for location,item in randomizer._locationItems if item.ItemType==itemType.REPORT]

    @staticmethod
    def getThunders(randomizer):
        return list(set([location.LocationTypes[0] for location,item in randomizer._locationItems if item.ItemType==itemType.THUNDER]))
    @staticmethod
    def getMagnets(randomizer):
        return list(set([location.LocationTypes[0] for location,item in randomizer._locationItems if item.ItemType==itemType.MAGNET]))
    @staticmethod
    def getPages(randomizer):
        return list(set([location.LocationTypes[0] for location,item in randomizer._locationItems if item.ItemType==itemType.TORN_PAGE]))

    @staticmethod
    def getForms(randomizer):
        return list(set([location.LocationTypes[0] for location,item in randomizer._locationItems if item.ItemType==itemType.FORM]))

ut = Tests()

unittest.main()
