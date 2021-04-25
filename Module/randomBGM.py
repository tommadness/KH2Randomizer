import random, os, zipfile

class RandomBGM():
    def randomizeBGM(outZip, platform):
        if not platform == "PC":
            return ""

        BGMList = []
        for folderName,subfolders,filenames in os.walk("Module/BGM/{platform}".format(platform=platform)):
            for filename in filenames:
                BGMList.append(filename)
        shuffledBGM = BGMList[:]
        random.shuffle(shuffledBGM)
        BGMAssets = []
        for i in range(len(BGMList)):
            BGMAssets.append({
                "name": "bgm\\{original}".format(original=BGMList[i]),
                "method": "copy",
                "source": [{"name": "bgm\\{newBGM}".format(newBGM = shuffledBGM[i])}]
            })
            outZip.write("Module/BGM/{platform}/{BGM}".format(platform = platform, BGM = BGMList[i]),"bgm/{BGM}".format(BGM = BGMList[i]))
        return BGMAssets
