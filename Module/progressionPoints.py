from List.configDict import locationType


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
            locationType.TWTNW:"TWTNW"
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
            "OlympusColiseum":[ "Olympus Coliseum Enter", "Cerberus", "Phil's Urns", "Demyx", "Pete", "Hydra", "Auron Statue", "Hades", "AS Zexion" ],
            "DisneyCastle":[ "Disney Castle Enter", "Minnie Escort", "Old Pete", "Timeless River Windows", "Boat Pete", "Pete", "AS Marluxia", "Lingering Will" ],
            "PortRoyal":[ "Port Royal Enter", "Town Fight", "1 Minute Fight", "PR 2 Medallions", "Boat Barrels", "Barbossa", "Grim Reaper 1", "First Medallion Gambler", "Grim Reaper 2", "Data Luxord" ],
            "Agrabah":[ "Agrabah Enter", "Abu Minigame", "Chasm of Challenges", "Treasure Room", "Twin Lords", "Carpet Magic", "Genie Jafar", "AS Lexaeus" ],
            "HalloweenTown":[ "Halloween Town Enter", "Candy Cane Lane Fight", "Prison Keeper", "Oogie Boogie", "Lock, Shock, Barrel", "Presents Minigame", "Experiment", "AS Vexen"],
            "PrideLands":[ "Pride Lands Enter", "Talking to Simba", "Hyenas 1", "Scar", "Hyenas 2", "Groundshaker", "Data Saix" ],
            "SpaceParanoids":[ "Space Paranoids Enter", "Screens", "Hostile Program", "Solar Sailer Fight", "MCP", "AS Larxene" ],
            "HundredAcreWood":[ "Pooh's Howse Enter", "Piglet's Howse Enter", "Rabbit's Howse Enter", "Kanga's Howse Enter", "Spooky Cave Enter", "Starry Hill Enter" ],
            "Atlantica":[ "Atlantica Enter", "Ursula's Revenge", "A New Day is Dawning" ],
            "TWTNW":[ "TWTNW Enter", "Roxas", "Xigbar", "Luxord", "Saix", "Xemnas 1", "Data Xemnas" ]
        }
        return human_readable_labels[self.gen_to_tracker_location_map[world]][index]
    def set_cp_for_world(self,world:locationType,index:int, value:int):
        self.points[world][index] = value

    def initialize_point_thresholds(self):
        self.point_thresholds = [ 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 7, 7, 7, 7, 8, 8] # max 18 (17 worlds + creations)

    def initialize_points(self):
        self.points = {
            locationType.Level:[ 0, 1, 1, 1, 1 ],
            locationType.FormLevel:[ 0,0,1,1,1,1 ],
            locationType.STT:[ 0, 1, 2, 0, 2, 3, 1, 6 ],
            locationType.TT:[ 0, 1, 2, 2, 3, 2, 6 ],
            locationType.HB:[ 0, 1, 1, 2, 1, 2, 2, 2, 5, 6 ],
            locationType.BC:[ 0, 2, 1, 2, 1, 3, 6 ],
            locationType.OC:[ 0, 1, 2, 1, 2, 1, 2, 3, 5 ],
            locationType.Agrabah:[ 1, 1, 2, 2, 3, 2, 2, 5 ],
            locationType.LoD:[ 0, 1, 1, 1, 1, 2, 1, 3, 6 ],
            locationType.HUNDREDAW:[ 0, 0, 1, 2, 2, 4 ],
            locationType.PL:[ 0, 1, 1, 2, 1, 3, 6 ],
            locationType.Atlantica:[ 0, 4, 3 ],
            locationType.DC:[ 0, 1, 1, 2, 2, 1, 3, 7 ],
            locationType.HT:[ 1, 2, 1, 1, 1, 2, 3, 6 ],
            locationType.PR:[ 0, 1, 1, 2, 1, 2, 2, 1, 2, 6 ],
            locationType.SP:[ 2, 2, 2, 3, 3, 6 ],
            locationType.TWTNW:[ 0, 2, 2, 2, 2, 2, 7 ]
        }
        entry_count = 0

        for _,i in self.points.items():
            entry_count+=len(i)
        range_end = 4-entry_count%4
        if range_end==4:
            range_end=0
        self.points["ZZZZZZZZZZZZZZZZ"] = [0 for x in range(range_end)] # adding some padding at the end of the file

    def get_compressed(self):
        def int_to_hex_digits(num):
            hex_string = "{0:#0{1}x}".format(num,5)
            return hex_string[2:]
        character_list = ""
        keys = list(self.points.keys())
        # keys.sort()
        current_number_sum = 0
        current_number_index = 0
        compare_list = []
        for k in keys:
            for i in range(len(self.points[k])):
                current_number = self.points[k][i]
                compare_list.append(current_number)
                if current_number_index==0:
                    current_number_sum=(current_number<<9)
                elif current_number_index==1:
                    current_number_sum+=(current_number<<6)
                elif current_number_index==2:
                    current_number_sum+=(current_number<<3)
                elif current_number_index==3:
                    current_number_sum+=current_number
                    character_list+=int_to_hex_digits(current_number_sum)
                    current_number_sum=0
                current_number_index = (current_number_index + 1)%4
        threshold_characters=""
        for p in self.point_thresholds:
            threshold_characters+=str(p)
        return threshold_characters+character_list

    def set_uncompressed(self,compressed_string):
        for p in range(len(self.point_thresholds)):
            self.set_point_threshold(p,int(compressed_string[p]))
        compressed_string = compressed_string[18:]

        def hex_digits_to_ints(char1,char2,char3):
            full_string = "0x"+char1+char2+char3
            full_int = int(full_string,16)
            #chop into the 4 ints
            int1 = full_int>>9
            int2 = (full_int&511)>>6
            int3 = (full_int&63)>>3
            int4 = (full_int&7)
            return [int1,int2,int3,int4]
        keys = list(self.points.keys())
        # keys.sort()
        current_group_index = 0
        current_number_group = None
        current_number_index = 0
        compare_list = []
        for k in keys:
            for i in range(len(self.points[k])):
                if current_number_index==0:
                    current_string = compressed_string[current_group_index*3:current_group_index*3+3]
                    current_group_index+=1
                    current_number_group = hex_digits_to_ints(current_string[0],current_string[1],current_string[2])
                self.points[k][i] = current_number_group[current_number_index]
                compare_list.append(self.points[k][i])
                current_number_index = (current_number_index + 1)%4
        return True

    def get_point_threshold(self,index):
        return self.point_thresholds[index]
    
    def set_point_threshold(self,index,value):
        self.point_thresholds[index] = value

    def get_hint_thresholds(self,world_count):
        output = [x for x in self.point_thresholds if x < world_count]
        return output

    def get_points_json(self):
        output = {}
        for l in locationType:
            if l in self.points:
                output[self.gen_to_tracker_location_map[l]] = self.points[l]
        return output