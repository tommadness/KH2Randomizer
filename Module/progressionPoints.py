from List.configDict import locationType


class ProgressionPoints():
    def __init__(self):
        self.gen_to_tracker_location_map = {
            locationType.STT:"SimulatedTwilightTown",
            locationType.TT:"TwilightTown",
            locationType.HB:"HollowBastion",
            locationType.BC:"BeastsCastle",
            locationType.OC:"OlympusColiseum",
            locationType.Agrabah:"Agrabah",
            locationType.LoD:"LandofDragons",
            locationType.HUNDREDAW:"HundredAcreWood",
            locationType.PL:"PrideLands",
            locationType.Atlantica:"Atlantica",
            locationType.DC:"DisneyCastle",
            locationType.HT:"HalloweenTown",
            locationType.PR:"PortRoyal",
            locationType.SP:"SpaceParanoids",
            locationType.TWTNW:"TWTNW"
        }
        self.set_points()
        self.set_hint_thresholds()

    def set_hint_thresholds(self):
        self.point_thresholds = [ 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 7, 7, 7, 7, 8, 8] # max 18

    def set_points(self):
        self.points = {
            locationType.STT:[ 0, 1, 2, 0, 2, 3, 1, 6 ],
            locationType.TT:[ 0, 1, 2, 2, 3, 2, 6 ],
            locationType.HB:[ 0, 1, 1, 2, 1, 2, 2, 2, 5, 6 ],
            locationType.BC:[ 0, 2, 1, 2, 1, 3, 6 ],
            locationType.OC:[ 0, 2, 1, 2, 1, 2, 1, 2, 3, 5 ],
            locationType.Agrabah:[ 0, 1, 1, 2, 2, 3, 2, 2, 5 ],
            locationType.LoD:[ 0, 1, 1, 1, 1, 2, 1, 3, 6 ],
            locationType.HUNDREDAW:[ 0, 0, 1, 2, 2, 4 ],
            locationType.PL:[ 0, 1, 1, 2, 1, 3, 6 ],
            locationType.Atlantica:[ 0, 4, 3 ],
            locationType.DC:[ 0, 1, 1, 2, 2, 1, 3, 8 ],
            locationType.HT:[ 0, 1, 2, 1, 1, 1, 2, 3, 6 ],
            locationType.PR:[ 0, 1, 1, 2, 1, 2, 2, 1, 2, 6 ],
            locationType.SP:[ 0, 2, 2, 2, 3, 3, 6 ],
            locationType.TWTNW:[ 0, 2, 2, 2, 2, 2, 7 ]
        }

    def get_hint_thresholds(self,world_count):
        output = [x for x in self.point_thresholds if x < world_count]
        return output

    def get_points_json(self):
        output = {}
        for l in locationType:
            if l in self.points:
                output[self.gen_to_tracker_location_map[l]] = self.points[l]
        return output