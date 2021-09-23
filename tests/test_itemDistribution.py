
import sys
sys.path.append("..")
from Module.randomize import KH2Randomizer
from Module.seedEvaluation import SeedValidator,SeedMetricsNumDatas,SeedMetricsNumCritExtra,SeedMetricsGenDataFrame
import unittest,datetime,json,os


class Tests(unittest.TestCase):
    def test_dataDistribution(self):
        avgLateChecks = {}
        metricCalculator = SeedMetricsNumDatas()
        numSeeds = 50
        for diff in ["Super Easy","Easy","Normal","Hard","Very Hard","Insane"]:
            avgLateChecks[diff] = 0.0
            for i in range(numSeeds):
                randomizer = self.create_difficulty_seed(diff+str(i),diff)
                results = metricCalculator.metrics(randomizer)
                avgLateChecks[diff]+=results

            avgLateChecks[diff] /= numSeeds
        assert avgLateChecks["Super Easy"] <= avgLateChecks["Easy"]
        assert avgLateChecks["Easy"] <= avgLateChecks["Normal"]
        assert avgLateChecks["Normal"] <= avgLateChecks["Hard"]
        assert avgLateChecks["Hard"] <= avgLateChecks["Very Hard"]
        assert avgLateChecks["Very Hard"] <= avgLateChecks["Insane"]

    def test_critChecks(self):
        avgLateChecks = {}
        metricCalculator = SeedMetricsNumCritExtra()
        numSeeds = 50
        for diff in ["Super Easy","Easy","Normal","Hard","Very Hard","Insane"]:
            print(f"Start evaluating {diff}")
            avgLateChecks[diff] = 0.0
            for i in range(numSeeds):
                randomizer = self.create_difficulty_seed(diff+str(i),diff)
                results = metricCalculator.metrics(randomizer)
                avgLateChecks[diff]+=results

            avgLateChecks[diff] /= numSeeds
            print(avgLateChecks[diff])
        assert avgLateChecks["Super Easy"] >= avgLateChecks["Easy"]
        assert avgLateChecks["Easy"] >= avgLateChecks["Normal"]
        assert avgLateChecks["Normal"] >= avgLateChecks["Hard"]
        assert avgLateChecks["Hard"] >= avgLateChecks["Very Hard"]
        assert avgLateChecks["Very Hard"] >= avgLateChecks["Insane"]


    # def test_allLocations(self):
    #     data = {}
    #     metricCalculator = SeedMetricsGenDataFrame()
    #     numSeeds = 100
    #     for diff in ["Super Easy","Easy","Normal","Hard","Very Hard","Insane"]:
    #         print(f"Start evaluating {diff}")
    #         data[diff] = []
    #         for i in range(numSeeds):
    #             randomizer = self.create_difficulty_seed(diff+str(i),diff)
    #             results = metricCalculator.metrics(randomizer)
    #             data[diff]+=results
    #     development_mode = os.environ.get("DEVELOPMENT_MODE")
    #     if development_mode:
    #         development_mode_path = os.environ.get("DEVELOPMENT_MODE_PATH")
    #         if development_mode_path:
    #             today = str(datetime.datetime.now())
    #             today=today.replace(" ","-")
    #             today=today.replace(":","-")
    #             today=today.replace(".","-")
    #             with open(development_mode_path+"\\"+today+".txt",'w') as file:
    #                 file.write(json.dumps(data))
    #         return


    @staticmethod
    def create_difficulty_seed(seedName,difficulty):
        fakeSessionDict = {}
        fakeSessionDict["seedModifiers"] = []
        fakeSessionDict["startingInventory"] = []
        fakeSessionDict["itemPlacementDifficulty"] = difficulty
        validator = SeedValidator(fakeSessionDict)
        attemptNumber=0
        while True:
            attemptNumber+=1
            randomizer = KH2Randomizer(seedName = seedName+"-"+str(attemptNumber))
            randomizer.populateLocations([],  maxItemLogic = True, item_difficulty=difficulty)
            randomizer.populateItems(promiseCharm = True, startingInventory = [], abilityListModifier=None)
            randomizer.setKeybladeAbilities()
            randomizer.setRewards()
            randomizer.setLevels(5,{'0':3, '1':3, '2':3, '3':3, '4':3, '5':3})
            randomizer.setBonusStats()
            if validator.validateSeed(fakeSessionDict, randomizer):
                return randomizer



ut = Tests()

unittest.main()
