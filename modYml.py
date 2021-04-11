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