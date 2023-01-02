from List.configDict import locationType
from Module import encoding


class ProgressionPoints():
    def __init__(self):
        self.gen_to_tracker_location_map = {
            locationType.Level:"Levels",
            locationType.FormLevel:"Drives",
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
            locationType.TWTNW:"TWTNW",
            locationType.CoR:"CavernofRemembrance"
        }
        self.initialize_points()
        self.initialize_point_thresholds()

    def get_world_options(self):
        return list(self.gen_to_tracker_location_map.keys())
    def get_num_cp_for_world(self,world:locationType):
        return len(self.points[world])
    def get_cp_for_world(self,world:locationType,index:int):
        return self.points[world][index]
    def get_cp_label_for_world(self,world:locationType,index:int):
        human_readable_labels = {
            "Levels":["Level 10", "Level 20", "Level 30", "Level 40", "Level 50"],
            "Drives":["Drive Level 2", "Drive Level 3", "Drive Level 4", "Drive Level 5", "Drive Level 6", "Drive Level 7"],
            "SimulatedTwilightTown":[ "STT Enter", "Olette Munny Pouch", "Twilight Thron", "Axel 1", "Setzer", "Mansion Computer Room", "Axel 2", "Data Roxas" ],
            "TwilightTown":[ "Twilight Town Enter", "Station Dusk Fight", "Mysterious Tower", "Sandlot Fight", "Mansion Fight", "Betwixt and Between", "Data Axel" ],
            "HollowBastion":[ "Hollow Bastion Enter", "Bailey Fight", "Ansem's Study Computer", "Corridors Fight", "Dancers Fight", "Demyx", "Final Fantasy Fights", "1000 Heartless", "Sephiroth", "Data Demyx" ],
            "LandofDragons":[ "Land of Dragons Enter", "Mission 3", "Mountain Trail", "Cave Fight", "Summit Fight", "Shan Yu", "Antechamber Nobodies", "Stormrider", "Data Xigbar" ],
            "BeastsCastle":[ "Beast's Castle Enter", "Thresholder", "Beast's Room", "Dark Thorn", "Ballroom Dragoons Fight", "Xaldin", "Data Xaldin" ],
            "OlympusColiseum":[ "Olympus Coliseum Enter", "Cerberus", "Phil's Urns", "Demyx", "Pete", "Hydra", "Auron Statue", "Hades", "AS Zexion", "Data Zexion" ],
            "DisneyCastle":[ "Disney Castle Enter", "Minnie Escort", "Old Pete", "Timeless River Windows", "Boat Pete", "Pete", "AS Marluxia", "Data Marluxia", "Lingering Will" ],
            "PortRoyal":[ "Port Royal Enter", "Town Fight", "1 Minute Fight", "Boat Medallion", "Boat Barrels", "Barbossa", "Grim Reaper 1", "First Medallion Gambler", "Grim Reaper 2", "Data Luxord" ],
            "Agrabah":[ "Agrabah Enter", "Abu Minigame", "Chasm of Challenges", "Treasure Room", "Twin Lords", "Carpet Magic", "Genie Jafar", "AS Lexaeus", "Data Lexaeus" ],
            "HalloweenTown":[ "Halloween Town Enter", "Candy Cane Lane Fight", "Prison Keeper", "Oogie Boogie", "Lock, Shock, Barrel", "Presents Minigame", "Experiment", "AS Vexen", "Data Vexen" ],
            "PrideLands":[ "Pride Lands Enter", "Talking to Simba", "Hyenas 1", "Scar", "Hyenas 2", "Groundshaker", "Data Saix" ],
            "SpaceParanoids":[ "Space Paranoids Enter", "Screens", "Hostile Program", "Solar Sailer Fight", "MCP", "AS Larxene", "Data Larxene" ],
            "HundredAcreWood":[ "Pooh's Howse Enter", "Piglet's Howse Enter", "Rabbit's Howse Enter", "Kanga's Howse Enter", "Spooky Cave Enter", "Starry Hill Enter" ],
            "Atlantica":[ "Atlantica Enter", "Ursula's Revenge", "A New Day is Dawning" ],
            "TWTNW":[ "TWTNW Enter", "Roxas", "Xigbar", "Luxord", "Saix", "Xemnas 1", "Data Xemnas" ],
            "CavernofRemembrance":[ "CoR Enter", "First Fight", "Steam Valves", "Second Fight", "Transport to Remembrance" ]
        }
        return human_readable_labels[self.gen_to_tracker_location_map[world]][index]
    def set_cp_for_world(self,world:locationType,index:int, value:int):
        self.points[world][index] = value

    def initialize_point_thresholds(self):
        self.point_thresholds = [ 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8] # max 18 (17 worlds + creations)

    def initialize_points(self):
        self.points = {
            locationType.Level:[ 0, 0, 1, 1, 2 ],
            locationType.FormLevel:[ 0, 0, 0, 1, 1, 1 ],
            locationType.STT:[ 0, 1, 2, 1, 1, 1, 1, 6 ],
            locationType.TT:[ 0, 1, 1, 2, 2, 2, 6 ],
            locationType.HB:[ 0, 1, 0, 2, 1, 2, 2, 2, 5, 6 ],
            locationType.BC:[ 0, 2, 1, 2, 1, 3, 6 ],
            locationType.OC:[ 0, 2, 0, 2, 0, 2, 2, 3, 3, 6 ],
            locationType.Agrabah:[ 0, 1, 1, 1, 2, 1, 3, 4, 6 ],
            locationType.LoD:[ 0, 1, 1, 1, 1, 2, 0, 3, 6 ],
            locationType.HUNDREDAW:[ 0, 0, 1, 2, 2, 4 ],
            locationType.PL:[ 0, 1, 1, 2, 1, 3, 6 ],
            locationType.Atlantica:[  0, 5, 3 ],
            locationType.DC:[ 0, 1, 1, 2, 1, 2, 5, 6, 7 ],
            locationType.HT:[ 0, 1, 2, 2, 1, 1, 3, 3, 6 ],
            locationType.PR:[ 0, 1, 1, 0, 1, 2, 1, 1, 3, 6 ],
            locationType.SP:[ 0, 1, 2, 2, 2, 4, 6 ],
            locationType.TWTNW:[ 0, 2, 3, 2, 2, 2, 7 ],
            locationType.CoR:[0, 4, 0, 4, 7]
        }

    def get_compressed(self) -> str:
        keys = list(self.points.keys())

        threshold_characters = ''
        for p in self.point_thresholds:
            threshold_characters += str(p)

        points_characters = ''
        for k in keys:
            for i in range(len(self.points[k])):
                points_characters += str(self.points[k][i])

        threshold_result = encoding.v2r(int(threshold_characters))
        points_result = encoding.v2r(int(points_characters))
        result = threshold_result + '+' + points_result

        return result

    def set_uncompressed(self, compressed_string: str):
        keys = list(self.points.keys())

        split_strings = compressed_string.split('+')

        threshold_count = len(self.point_thresholds)
        decoded_threshold = str(encoding.r2v(split_strings[0]))
        threshold_characters = self._prepend_zeroes(decoded_threshold, expected_length=threshold_count)
        for i in range(threshold_count):
            self.set_point_threshold(i, int(threshold_characters[i]))

        points_expected_length = 0
        for k in keys:
            points_expected_length = points_expected_length + len(self.points[k])
        decoded_points = str(encoding.r2v(split_strings[1]))
        points_characters = self._prepend_zeroes(decoded_points, expected_length=points_expected_length)

        current_index = 0
        for k in keys:
            location_points: list[int] = self.points[k]
            for i in range(len(location_points)):
                location_points[i] = int(points_characters[current_index])
                current_index += 1

        return True

    def get_point_threshold(self,index):
        return self.point_thresholds[index]
    
    def set_point_threshold(self,index,value):
        self.point_thresholds[index] = value

    def get_hint_thresholds(self,world_count):
        output = [self.point_thresholds[x] for x in range(len(self.point_thresholds)) if x < world_count]
        return output

    def get_points_json(self):
        output = {}
        for l in locationType:
            if l in self.points:
                output[self.gen_to_tracker_location_map[l]] = self.points[l]
        return output

    @staticmethod
    def _prepend_zeroes(value: str, expected_length: int) -> str:
        difference = expected_length - len(value)
        return ('0' * difference) + value
