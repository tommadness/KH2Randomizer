class modYml:
    def getDefaultMod():
        return {
            "title": "Randomizer Seed",
            "assets": [
                {
                    "name": "msg/jp/sys.bar",
                    "multi": [
                        {
                            "name": "msg/us/sys.bar"
                        },
                        {
                            "name": "msg/uk/sys.bar"
                        }
                    ],
                    "method": "binarc",
                    "source": [
                        {
                            "name": "sys",
                            "type": "list",
                            "method": "kh2msg",
                            "source": [
                                {
                                    "name": "sys.yml",
                                    "language": "en"
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "msg/jp/jm.bar",
                    "multi": [
                        {
                            "name": "msg/us/jm.bar"
                        },
                        {
                            "name": "msg/uk/jm.bar"
                        }
                    ],
                    "method": "binarc",
                    "source": [
                        {
                            "name": "jm",
                            "type": "list",
                            "method": "kh2msg",
                            "source": [
                                {
                                    "name": "jm.yml",
                                    "language": "en"
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "00battle.bin",
                    "method": "binarc",
                    "source": [
                        {
                            "name": "fmlv",
                            "method": "listpatch",
                            "type": "List",
                            "source": [
                                {
                                    "name": "FmlvList.yml",
                                    "type": "fmlv"
                                }
                            ]
                        },
                        {
                            "name": "lvup",
                            "method": "listpatch",
                            "type": "List",
                            "source": [
                                {
                                    "name": "LvupList.yml",
                                    "type": "lvup"
                                }
                            ]
                        },
                        {
                            "name": "bons",
                            "method": "listpatch",
                            "type": "List",
                            "source": [
                                {
                                    "name": "BonsList.yml",
                                    "type": "bons"
                                }
                            ]
                        },
                        {
                            "name": "plrp",
                            "method": "listpatch",
                            "type": "List",
                            "source": [
                                {
                                    "name": "PlrpList.yml",
                                    "type": "plrp"
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "03system.bin",
                    "method": "binarc",
                    "source": [
                        {
                            "name": "trsr",
                            "method": "listpatch",
                            "type": "List",
                            "source": [
                                {
                                    "name": "TrsrList.yml",
                                    "type": "trsr"
                                }
                            ]
                        },
                        {
                            "name": "item",
                            "method": "listpatch",
                            "type": "List",
                            "source": [
                                {
                                    "name": "ItemList.yml",
                                    "type": "item"
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    def getJMYAML():
        return [
            {
                "id": 20279,
                "en": "Defeat Xemnas at the top of the Castle"
            },
            {
                "id": 20280,
                "en": "Defeat Storm Rider"
            },
            {
                "id": 20281,
                "en": "Defeat Xaldin in the Courtyard"
            },
            {
                "id": 20282,
                "en": "Defeat Dr. Finkelstein's Experiment"
            },
            {
                "id": 20283,
                "en": "Defeat Genie Jafar"
            },
            {
                "id": 20284,
                "en": "Defeat Hades"
            },
            {
                "id": 20285,
                "en": "Defeat Groundshaker"
            },
            {
                "id": 20286,
                "en": "Fight alongside Axel in the world Between"
            },
            {
                "id": 20287,
                "en": "Defend Hollow Bastion from the Heartless Army"
            },
            {
                "id": 20288,
                "en": "Defeat Grim Reaper II"
            },
            {
                "id": 20289,
                "en": "Protect the Cornerstone of Light from Pete"
            },
            {
                "id": 20290,
                "en": "Defeat the Master Control Program"
            },
            {
                "id": 20291,
                "en": "Confront DiZ in the Mansion's Pod Room"
            }
        ]

    def getSysYAML(seedHashIcons, crit_mode = False):
        seedHashString = " ".join(["{:icon " + icon + "}" for icon in seedHashIcons])
        sys = [{"id": 17198, "en":seedHashString}]
        sys.append({"id": 19482, "en": "Important Checks Found"})
        if crit_mode:
            sys.append({"id": 17201, "en": "{:color #FF000080}Beginner (WARNING)"})
            sys.append({"id": 17202, "en": "{:color #FF000080}Standard (WARNING)"})
            sys.append({"id": 17203, "en": "{:color #FF000080}Proud (WARNING)"})
            sys.append({"id": 17204, "en": "An easier mode for beginners. \n {:color #FF000080} Crit bonuses are turned on,\n The seven random starting items will be unobtainable."})
            sys.append({"id": 17205, "en": "A balanced mode that's not too hard \n but not too easy. Best for those \n challenging this game for the first time.\n {:color #FF000080} Crit bonuses are turned on,\n The seven random starting items will be unobtainable."})
            sys.append({"id": 17206, "en": "A difficult mode with stronger enemies.\n Best for those seeking a challenge.\n {:color #FF000080} Crit bonuses are turned on,\n The seven random starting items will be unobtainable."})

        return sys
    
    def getASDataMod():
        return [{"name": "ard/hb32.ard","multi": [{"name": "ard/us/hb32.ard"}],"method":"binarc","source":[{"name":"evt","type":"areadatascript","method":"areadatascript","source":[{"name":"asdata/hb32evt.script"}]}] },
                {"name": "ard/hb33.ard","multi": [{"name": "ard/us/hb33.ard"}],"method":"binarc","source":[{"name":"evt","type":"areadatascript","method":"areadatascript","source":[{"name":"asdata/hb33evt.script"}]}] },
                {"name": "ard/hb34.ard","multi": [{"name": "ard/us/hb34.ard"}],"method":"binarc","source":[{"name":"evt","type":"areadatascript","method":"areadatascript","source":[{"name":"asdata/hb34evt.script"}]}] },
                {"name": "ard/hb38.ard","multi": [{"name": "ard/us/hb38.ard"}],"method":"binarc","source":[{"name":"evt","type":"areadatascript","method":"areadatascript","source":[{"name":"asdata/hb38evt.script"}]}] }]

    def getPuzzleMod():
        return {
                    "name": "menu/jp/jiminy.bar",
                    "multi": [
                        {
                            "name": "menu/us/jiminy.bar"
                        },
                        {
                            "name": "menu/uk/jiminy.bar"
                        },
                        {
                            "name": "menu/fm/jiminy.bar"
                        }
                    ],
                    "method": "binarc",
                    "source": [
                        {
                            "name": "puzz",
                            "type": "jimidata",
                            "method": "copy",
                            "source": [
                                {
                                    "name": "modified_puzzle.bin"
                                }
                            ]
                        }
                    ]
                }
    def getSynthMod():
        return {
                    "name": "menu/jp/mixdata.bar",
                    "multi": [
                        {
                            "name": "menu/us/mixdata.bar"
                        },
                        {
                            "name": "menu/uk/mixdata.bar"
                        },
                        {
                            "name": "menu/fm/mixdata.bar"
                        }
                    ],
                    "method": "binarc",
                    "source": [
                        {
                            "name": "reci",
                            "type": "synthesis",
                            "method": "copy",
                            "source": [
                                {
                                    "name": "modified_synth.bin"
                                }
                            ]
                        }
                    ]
                }
