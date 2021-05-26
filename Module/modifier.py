class SeedModifier():
    def getOptions():
        return [
            {
                "name":"Glass Cannon",
                "description": "No more pesky Defense Ups in the level up stats pool"
            },
            {
                "name":"Library of Assemblage",
                "description": "Start with all the hints"
            },
            {
                "name": "Schmovement",
                "description": "Start with level 1 of all growth abilities"
            },
            {
                "name": "Better Junk",
                "description": "No more synthesis materials in the junk item pool"
            },
            {
                "name": "StatSanity",
                "description": "Bonus Level stats are mixed into the pool"
            }
        ]

    def glassCannon(enabled):
        if enabled:
            return [{"Stat":"Str","Value": 2},{"Stat":"Mag", "Value": 2},{"Stat": "Ap", "Value": 2}]
        return None

    def library(enabled):
        if enabled:
            return [
                        "226",
                        "227",
                        "228",
                        "229",
                        "230",
                        "231",
                        "232",
                        "233",
                        "234",
                        "235",
                        "236",
                        "237",
                        "238"
                    ]
        return []

    def schmovement(enabled):
        if enabled:
            return [
                "94",
                "98",
                "102",
                "106",
                "564"
            ]
        return []