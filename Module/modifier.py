class SeedModifier():
    def getOptions():
        return [
            {
                "name":"Glass Cannon",
                "description": "No more pesky Defense Ups in the level up stats pool"
            }
        ]

    def glassCannon(enabled):
        if enabled:
            return [{"Stat":"Str","Value": 2},{"Stat":"Mag", "Value": 2},{"Stat": "Ap", "Value": 2}]
        return None
