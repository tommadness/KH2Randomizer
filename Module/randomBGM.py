import random, os, zipfile

class RandomBGM():
    def randomizeBGM(option, outZip, platform):
        if not platform == "PC":
            return ""
        if option == "Disabled":
            return ""
        
        BGMList = []
        DMCABGM = [
            "music106.win32.scd",
            "music108.win32.scd",
            "music506.win32.scd",
            "music508.win32.scd",
            "music132.win32.scd",
        ]
        
        for folderName,subfolders,filenames in os.walk("Module/BGM/{platform}".format(platform=platform)):
            for filename in filenames:
                BGMList.append(filename)

        if option == "DMCA-Safe":
            for BGM in DMCABGM:
                BGMList.remove(BGM)

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

    def getOptions():
        return ["Disabled","All Music","DMCA-Safe"]
