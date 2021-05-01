import random, os, zipfile

class RandomBGM():
    def randomizeBGM(option, outZip, platform):
        if not platform == "PC":
            return ""
        if option == "Disabled":
            return ""
        
        BGMList = [
            "music050.win32.scd",
            "music051.win32.scd",
            "music052.win32.scd",
            "music053.win32.scd",
            "music054.win32.scd",
            "music055.win32.scd",
            "music059.win32.scd",
            "music060.win32.scd",
            "music061.win32.scd",
            "music062.win32.scd",
            "music063.win32.scd",
            "music064.win32.scd",
            "music065.win32.scd",
            "music066.win32.scd",
            "music067.win32.scd",
            "music068.win32.scd",
            "music069.win32.scd",
            "music081.win32.scd",
            "music082.win32.scd",
            "music084.win32.scd",
            "music085.win32.scd",
            "music086.win32.scd",
            "music087.win32.scd",
            "music088.win32.scd",
            "music089.win32.scd",
            "music090.win32.scd",
            "music091.win32.scd",
            "music092.win32.scd",
            "music093.win32.scd",
            "music094.win32.scd",
            "music095.win32.scd",
            "music096.win32.scd",
            "music097.win32.scd",
            "music098.win32.scd",
            "music099.win32.scd",
            "music100.win32.scd",
            "music101.win32.scd",
            "music102.win32.scd",
            "music103.win32.scd",
            "music104.win32.scd",
            "music106.win32.scd",
            "music107.win32.scd",
            "music108.win32.scd",
            "music109.win32.scd",
            "music110.win32.scd",
            "music111.win32.scd",
            "music112.win32.scd",
            "music113.win32.scd",
            "music114.win32.scd",
            "music115.win32.scd",
            "music116.win32.scd",
            "music117.win32.scd",
            "music118.win32.scd",
            "music119.win32.scd",
            "music120.win32.scd",
            "music121.win32.scd",
            "music122.win32.scd",
            "music123.win32.scd",
            "music124.win32.scd",
            "music125.win32.scd",
            "music127.win32.scd",
            "music128.win32.scd",
            "music129.win32.scd",
            "music130.win32.scd",
            "music131.win32.scd",
            "music132.win32.scd",
            "music133.win32.scd",
            "music134.win32.scd",
            "music135.win32.scd",
            "music136.win32.scd",
            "music137.win32.scd",
            "music138.win32.scd",
            "music139.win32.scd",
            "music141.win32.scd",
            "music142.win32.scd",
            "music143.win32.scd",
            "music144.win32.scd",
            "music145.win32.scd",
            "music146.win32.scd",
            "music148.win32.scd",
            "music149.win32.scd",
            "music151.win32.scd",
            "music152.win32.scd",
            "music153.win32.scd",
            "music154.win32.scd",
            "music155.win32.scd",
            "music158.win32.scd",
            "music159.win32.scd",
            "music164.win32.scd",
            "music185.win32.scd",
            "music186.win32.scd",
            "music187.win32.scd",
            "music188.win32.scd",
            "music189.win32.scd",
            "music190.win32.scd",
            "music506.win32.scd",
            "music507.win32.scd",
            "music508.win32.scd",
            "music509.win32.scd",
            "music513.win32.scd",
            "music517.win32.scd",
            "music521.win32.scd",
            "music530.win32.scd",
        ]
        DMCABGM = [
            "music106.win32.scd",
            "music108.win32.scd",
            "music506.win32.scd",
            "music508.win32.scd",
            "music132.win32.scd",
        ]

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
                "source": [{"name": "bgm\\{newBGM}".format(newBGM = shuffledBGM[i]), "type":"internal"}]
            })
            outZip.write("Module/BGM/{platform}/{BGM}".format(platform = platform, BGM = BGMList[i]),"bgm/{BGM}".format(BGM = BGMList[i]))
        return BGMAssets

    def getOptions():
        return ["Disabled","All Music","DMCA-Safe"]
