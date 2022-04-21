from Class.newLocationClass import KH2Location
from List.LvupStats import DreamWeaponOffsets
from List.configDict import itemType, locationType, locationCategory
from altgraph.Graph import Graph
# from altgraph.Dot import Dot

from Module.RandomizerSettings import RandomizerSettings
from Module.itemPlacementRestriction import ItemPlacementHelpers

class LocationNode:
    def __init__(self,in_loc=None):
        if in_loc is None:
            self.locations = []
        else:
            self.locations = in_loc

class RequirementEdge:
    def __init__(self,req=None,strict=True,battle=False):
        if req is None:
            self.requirement = lambda inv: True
        else:
            self.requirement = req
        self.strict = strict
        self.battle = battle


class Locations:

    def __init__(self, settings: RandomizerSettings, secondary_graph = False):
        self.location_graph = Graph()
        self.reverse_rando = secondary_graph
        self.nightmare = settings.itemPlacementDifficulty=="Nightmare"
        self.first_boss_nodes = []
        self.second_boss_nodes = []
        self.data_nodes = []
        self.makeLocationGraph(settings.excludedLevels,settings.split_levels,settings.level_checks)

    """A set of methods to get all the location information for Sora, Donald, and Goofy. Limited logic about item placement here"""
    def getAllSoraLocations(self):
        return self.create_list_from_nodes(self.location_graph)

    @staticmethod
    def getAllDonaldLocations():
        return Locations.DonaldBonusList()+Locations.DonaldWeaponList()+Locations.DonaldStartingItems()


    @staticmethod
    def getAllGoofyLocations():
        return Locations.GoofyBonusList()+Locations.GoofyWeaponList()+Locations.GoofyStartingItems()

    @staticmethod
    def create_list_from_nodes(graph,nodes = None):
        if nodes is None:
            nodes = graph.node_list()
        locations = []
        for n in nodes:
            locations+=graph.node_data(n).locations
        return locations

    def add_node(self,node_name,node_data):
        self.location_graph.add_node(node_name,node_data)

    def add_edge(self,node1,node2,requirement):
        self.location_graph.add_edge(node1,node2,requirement)

    def makeLocationGraph(self,excludeLevels,split_levels,max_level):
        self.makeStartingGraph()
        self.makeLoDGraph()
        self.makeAGGraph()
        self.makeDCGraph()
        self.makeHundredAcreGraph()
        self.makeOCGraph()
        self.makeBCGraph()
        self.makeSPGraph()
        self.makeHTGraph()
        self.makePRGraph()
        self.makeHBGraph()
        self.makePLGraph()
        self.makeSTTGraph()
        self.makeTTGraph()
        self.makeTWTNWGraph()
        self.makeATLGraph()
        self.makeFormGraph()
        self.makeLevelGraph(excludeLevels,split_levels,max_level)
        self.makePuzzleGraph()
        # self.makeSynthGraph()

        # dot = Dot(self.location_graph)
        # dot.style(rankdir="LR")
        # dot.save_img(file_name='graph',file_type="gif")

    # def makeSynthGraph(self):
    #     self.add_node("")


    def makePuzzleGraph(self):
        self.add_node("Awakening Puzzle",LocationNode([KH2Location(0, "Awakening (AP Boost)",  locationCategory.POPUP, LocationTypes=[locationType.Puzzle],InvalidChecks=[itemType.REPORT]),]))
        self.add_node("Heart Puzzle",LocationNode([KH2Location(1, "Heart (Serenity Crystal)", locationCategory.POPUP,  LocationTypes=[locationType.Puzzle],InvalidChecks=[itemType.REPORT]),]))
        self.add_node("Duality Puzzle",LocationNode([KH2Location(2, "Duality (Rare Document)", locationCategory.POPUP,  LocationTypes=[locationType.Puzzle],InvalidChecks=[itemType.REPORT]),]))
        self.add_node("Frontier Puzzle",LocationNode([KH2Location(3, "Frontier (Manifest Illusion)", locationCategory.POPUP,  LocationTypes=[locationType.Puzzle],InvalidChecks=[itemType.REPORT]),]))
        self.add_node("Daylight Puzzle",LocationNode([KH2Location(4, "Daylight (Executive's Ring)", locationCategory.POPUP,  LocationTypes=[locationType.Puzzle],InvalidChecks=[itemType.TORN_PAGE, itemType.REPORT]),]))
        self.add_node("Sunset Puzzle",LocationNode([KH2Location(5, "Sunset (Grand Ribbon)", locationCategory.POPUP,  LocationTypes=[locationType.Puzzle],InvalidChecks=[itemType.REPORT]),]))

        #TODO put these in their proper location in the graph
        #TODO add the proper requirements for story unlock items
        self.add_edge("Starting","Awakening Puzzle",RequirementEdge(req=ItemPlacementHelpers.need_growths))
        self.add_edge("Starting","Heart Puzzle",RequirementEdge(req=ItemPlacementHelpers.need_growths))
        self.add_edge("Starting","Duality Puzzle",RequirementEdge(req=ItemPlacementHelpers.need_growths))
        self.add_edge("Starting","Frontier Puzzle",RequirementEdge(req=ItemPlacementHelpers.need_growths))
        self.add_edge("Starting","Daylight Puzzle",RequirementEdge(req=lambda inv : ItemPlacementHelpers.need_growths(inv) and ItemPlacementHelpers.need_5_pages(inv)))
        self.add_edge("Starting","Sunset Puzzle",RequirementEdge(req=ItemPlacementHelpers.need_growths))
    
    def makeFormGraph(self):
        for i in range(1,8):
            self.add_node(f"Valor-{i}",LocationNode([KH2Location(i,f"Valor Level {i}", locationCategory.VALORLEVEL,[locationType.FormLevel] + ([locationType.FormLevel1] if i==1 else []))]))
            self.add_node(f"Wisdom-{i}",LocationNode([KH2Location(i,f"Wisdom Level {i}", locationCategory.WISDOMLEVEL,[locationType.FormLevel] + ([locationType.FormLevel1] if i==1 else []))]))
            self.add_node(f"Limit-{i}",LocationNode([KH2Location(i,f"Limit Level {i}", locationCategory.LIMITLEVEL,[locationType.FormLevel] + ([locationType.FormLevel1] if i==1 else []))]))
            self.add_node(f"Master-{i}",LocationNode([KH2Location(i,f"Master Level {i}", locationCategory.MASTERLEVEL,[locationType.FormLevel] + ([locationType.FormLevel1] if i==1 else []))]))
            self.add_node(f"Final-{i}",LocationNode([KH2Location(i,f"Final Level {i}", locationCategory.FINALLEVEL,[locationType.FormLevel] + ([locationType.FormLevel1] if i==1 else []))]))
            self.add_node(f"Summon-{i}",LocationNode([KH2Location(i,f"Summon Level {i}", locationCategory.SUMMONLEVEL,[locationType.SummonLevel])]))


            form_helper = ItemPlacementHelpers.make_form_lambda_nightmare if self.nightmare else ItemPlacementHelpers.make_form_lambda

            if i != 1:
                self.add_edge(f"Valor-{i-1}",f"Valor-{i}",RequirementEdge(req=form_helper("Valor",i)))
                self.add_edge(f"Wisdom-{i-1}",f"Wisdom-{i}",RequirementEdge(req=form_helper("Wisdom",i)))
                self.add_edge(f"Limit-{i-1}",f"Limit-{i}",RequirementEdge(req=form_helper("Limit",i)))
                self.add_edge(f"Master-{i-1}",f"Master-{i}",RequirementEdge(req=form_helper("Master",i)))
                self.add_edge(f"Final-{i-1}",f"Final-{i}",RequirementEdge(req=form_helper("Final",i)))
                self.add_edge(f"Summon-{i-1}",f"Summon-{i}",RequirementEdge())
            else:
                self.add_edge("Starting",f"Valor-{i}",RequirementEdge())
                self.add_edge("Starting",f"Wisdom-{i}",RequirementEdge())
                self.add_edge("Starting",f"Limit-{i}",RequirementEdge())
                self.add_edge("Starting",f"Master-{i}",RequirementEdge())
                self.add_edge("Starting",f"Final-{i}",RequirementEdge())
                self.add_edge("Starting",f"Summon-{i}",RequirementEdge())



    def makeLevelGraph(self,excludeLevels,split_levels,max_level):
        node_index = 0
        current_location_list = []
        double_level_reward = False
        level_offsets = DreamWeaponOffsets()
        for i in range(1,100):
            level_description =  f"Level {i}"
            if split_levels:
                shield = level_offsets.get_shield_level(max_level,i)
                staff = level_offsets.get_staff_level(max_level,i)
                if shield and staff:
                    level_description = f"Level Sw: {i} Sh: {shield} St: {staff}"
            current_location_list.append(KH2Location(i, level_description, locationCategory.LEVEL,[locationType.Level]))
            if i not in excludeLevels:
                if double_level_reward:
                    self.add_node(f"LevelGroup-{node_index}",LocationNode(current_location_list))
                    current_location_list = []
                    if node_index == 0:
                        self.add_edge("Starting",f"LevelGroup-{node_index}",RequirementEdge())
                    else:
                        self.add_edge(f"LevelGroup-{node_index-1}",f"LevelGroup-{node_index}",RequirementEdge())
                    node_index+=1
                    double_level_reward = False
                else:
                    double_level_reward = True

        self.add_node(f"LevelGroup-{node_index}",LocationNode(current_location_list))
        if node_index == 0:
            self.add_edge("Starting",f"LevelGroup-{node_index}",RequirementEdge())
        else:
            self.add_edge(f"LevelGroup-{node_index-1}",f"LevelGroup-{node_index}",RequirementEdge())
        

    def makeStartingGraph(self):
        self.add_node("Starting",LocationNode([KH2Location(i, f"Starting Item {i}", locationCategory.CHEST, [locationType.Critical]) for i in range(1,8)] + \
                                                [KH2Location(585, "Garden of Assemblage Map", locationCategory.CHEST,[locationType.Free]),
                                                KH2Location(586, "GoA Lost Illusion", locationCategory.CHEST,[locationType.Free]),
                                                KH2Location(590, "Proof of Nonexistence", locationCategory.CHEST,[locationType.Free]),
                                                ]))


    def makeLoDGraph(self):
        self.add_node("Bamboo Grove",LocationNode([KH2Location(245, "Bamboo Grove Dark Shard", locationCategory.CHEST,[locationType.LoD]),
                                         KH2Location(497, "Bamboo Grove Ether", locationCategory.CHEST,[locationType.LoD]),
                                         KH2Location(498, "Bamboo Grove Mythril Shard", locationCategory.CHEST,[locationType.LoD]),]))
        self.add_node("Encampment Area Map",LocationNode([KH2Location(350, "Encampment Area Map", locationCategory.POPUP,[locationType.LoD]),]))
        self.add_node("Mission 3",LocationNode([KH2Location(417, "Mission 3", locationCategory.POPUP,[locationType.LoD]),]))
        self.add_node("Checkpoint",LocationNode([KH2Location(21, "Checkpoint Hi-Potion", locationCategory.CHEST,[locationType.LoD]),
                                         KH2Location(121, "Checkpoint Mythril Shard", locationCategory.CHEST,[locationType.LoD]),]))
        self.add_node("Mountain Trail",LocationNode([KH2Location(22, "Mountain Trail Lightning Shard", locationCategory.CHEST,[locationType.LoD]),
                                         KH2Location(23, "Mountain Trail Recovery Recipe", locationCategory.CHEST,[locationType.LoD]),
                                         KH2Location(122, "Mountain Trail Ether", locationCategory.CHEST,[locationType.LoD]),
                                         KH2Location(123, "Mountain Trail Mythril Shard", locationCategory.CHEST,[locationType.LoD]),]))
        self.add_node("Village Cave Map Popup",LocationNode([KH2Location(495, "Village Cave Area Map", locationCategory.POPUP,[locationType.LoD]),]))
        self.add_node("Village Cave",LocationNode([KH2Location(124, "Village Cave AP Boost", locationCategory.CHEST,[locationType.LoD]),
                                         KH2Location(125, "Village Cave Dark Shard", locationCategory.CHEST,[locationType.LoD]),]))
        self.add_node("Village Cave Bonus",LocationNode([KH2Location(43, "Village Cave Bonus", locationCategory.ITEMBONUS,[locationType.LoD]),]))
        self.add_node("Ridge",LocationNode([KH2Location(24, "Ridge Frost Shard", locationCategory.CHEST,[locationType.LoD]),
                                         KH2Location(126, "Ridge AP Boost", locationCategory.CHEST,[locationType.LoD]),]))
        self.add_node("Shan-Yu",LocationNode([KH2Location(9, "Shan-Yu", locationCategory.HYBRIDBONUS,[locationType.LoD]),
                                         KH2Location(257, "Hidden Dragon", locationCategory.POPUP,[locationType.LoD]),]))
        self.add_node("Throne Room",LocationNode([KH2Location(25, "Throne Room Torn Pages", locationCategory.CHEST,[locationType.LoD]),
                                         KH2Location(127, "Throne Room Palace Map", locationCategory.CHEST,[locationType.LoD]),
                                         KH2Location(26, "Throne Room AP Boost", locationCategory.CHEST,[locationType.LoD]),
                                         KH2Location(27, "Throne Room Queen Recipe", locationCategory.CHEST,[locationType.LoD]),
                                         KH2Location(128, "Throne Room AP Boost (2)", locationCategory.CHEST,[locationType.LoD]),
                                         KH2Location(129, "Throne Room Ogre Shield", locationCategory.CHEST,[locationType.LoD]),
                                         KH2Location(130, "Throne Room Mythril Crystal", locationCategory.CHEST,[locationType.LoD]),
                                         KH2Location(131, "Throne Room Orichalcum", locationCategory.CHEST,[locationType.LoD]),]))
        self.add_node("Storm Rider",LocationNode([KH2Location(10, "Storm Rider", locationCategory.ITEMBONUS,[locationType.LoD]),]))
        self.add_node("Data Xigbar",LocationNode([KH2Location(555, "Xigbar (Data) Defense Boost", locationCategory.POPUP,[locationType.LoD, locationType.DataOrg]),]))

        self.data_nodes.append("Data Xigbar")

        if not self.reverse_rando:
            self.add_edge("Starting","Bamboo Grove",RequirementEdge())
            self.add_edge("Bamboo Grove","Encampment Area Map",RequirementEdge())
            self.add_edge("Encampment Area Map","Mission 3",RequirementEdge(battle=True))
            self.add_edge("Encampment Area Map","Checkpoint",RequirementEdge())
            self.add_edge("Mission 3","Mountain Trail",RequirementEdge(battle=True))
            self.add_edge("Mountain Trail","Village Cave Map Popup",RequirementEdge(battle=True))
            self.add_edge("Village Cave Map Popup","Village Cave",RequirementEdge())
            self.add_edge("Village Cave","Village Cave Bonus",RequirementEdge(battle=True))
            self.add_edge("Village Cave Bonus","Ridge",RequirementEdge())
            self.add_edge("Ridge","Shan-Yu",RequirementEdge(battle=True))
            self.add_edge("Shan-Yu","Throne Room",RequirementEdge(battle=True,req=ItemPlacementHelpers.mulan_check))
            self.add_edge("Throne Room","Storm Rider",RequirementEdge(battle=True))
            self.add_edge("Storm Rider","Data Xigbar",RequirementEdge(battle=True))
            self.first_boss_nodes.append("Shan-Yu")
            self.second_boss_nodes.append("Storm Rider")
        else:
            self.add_edge("Starting","Mountain Trail",RequirementEdge())
            self.add_edge("Mountain Trail","Checkpoint",RequirementEdge())
            self.add_edge("Mountain Trail","Ridge",RequirementEdge())
            self.add_edge("Ridge","Throne Room",RequirementEdge(battle=True))
            self.add_edge("Throne Room","Storm Rider",RequirementEdge(battle=True))
            self.add_edge("Storm Rider","Bamboo Grove",RequirementEdge(req=ItemPlacementHelpers.mulan_check))
            self.add_edge("Bamboo Grove","Encampment Area Map",RequirementEdge(battle=True))
            self.add_edge("Encampment Area Map","Mission 3",RequirementEdge())
            self.add_edge("Mission 3","Village Cave Map Popup",RequirementEdge(battle=True))
            self.add_edge("Village Cave Map Popup","Village Cave",RequirementEdge())
            self.add_edge("Village Cave","Village Cave Bonus",RequirementEdge(battle=True))
            self.add_edge("Village Cave Bonus","Shan-Yu",RequirementEdge(battle=True))
            self.add_edge("Shan-Yu","Data Xigbar",RequirementEdge(battle=True))
            self.first_boss_nodes.append("Storm Rider")
            self.second_boss_nodes.append("Shan-Yu")


    def makeAGGraph(self):
        self.add_node("Agrabah Map Popup",LocationNode([KH2Location(353, "Agrabah Map", locationCategory.POPUP,[locationType.Agrabah]),]))
        self.add_node("Agrabah",LocationNode([KH2Location(28, "Agrabah Dark Shard", locationCategory.CHEST,[locationType.Agrabah]),
                                        KH2Location(29, "Agrabah Mythril Shard", locationCategory.CHEST,[locationType.Agrabah]),
                                        KH2Location(30, "Agrabah Hi-Potion", locationCategory.CHEST,[locationType.Agrabah]),
                                        KH2Location(132, "Agrabah AP Boost", locationCategory.CHEST,[locationType.Agrabah]),
                                        KH2Location(133, "Agrabah Mythril Stone", locationCategory.CHEST,[locationType.Agrabah]),
                                        KH2Location(249, "Agrabah Mythril Shard (2)", locationCategory.CHEST,[locationType.Agrabah]),
                                        KH2Location(501, "Agrabah Serenity Shard", locationCategory.CHEST,[locationType.Agrabah]),]))
        self.add_node("Bazaar",LocationNode([KH2Location(31, "Bazaar Mythril Gem", locationCategory.CHEST,[locationType.Agrabah]),
                                        KH2Location(32, "Bazaar Power Shard", locationCategory.CHEST,[locationType.Agrabah]),
                                        KH2Location(33, "Bazaar Hi-Potion", locationCategory.CHEST,[locationType.Agrabah]),
                                        KH2Location(134, "Bazaar AP Boost", locationCategory.CHEST,[locationType.Agrabah]),
                                        KH2Location(135, "Bazaar Mythril Shard", locationCategory.CHEST,[locationType.Agrabah]),]))
        self.add_node("Palace Walls",LocationNode([KH2Location(136, "Palace Walls Skill Ring", locationCategory.CHEST,[locationType.Agrabah]),
                                        KH2Location(520, "Palace Walls Mythril Stone", locationCategory.CHEST,[locationType.Agrabah]),]))
        self.add_node("Cave of Wonders Entrance",LocationNode([KH2Location(250, "Cave Entrance Power Stone", locationCategory.CHEST,[locationType.Agrabah]),
                                        KH2Location(251, "Cave Entrance Mythril Shard", locationCategory.CHEST,[locationType.Agrabah]),]))
        self.add_node("Valley of Stone",LocationNode([KH2Location(35, "Valley of Stone Mythril Stone", locationCategory.CHEST,[locationType.Agrabah]),
                                        KH2Location(36, "Valley of Stone AP Boost", locationCategory.CHEST,[locationType.Agrabah]),
                                        KH2Location(137, "Valley of Stone Mythril Shard", locationCategory.CHEST,[locationType.Agrabah]),
                                        KH2Location(138, "Valley of Stone Hi-Potion", locationCategory.CHEST,[locationType.Agrabah]),]))
        self.add_node("Abu Escort",LocationNode([KH2Location(42, "Abu Escort", locationCategory.ITEMBONUS,[locationType.Agrabah]),]))
        self.add_node("Chasm of Challenges",LocationNode([KH2Location(487, "Chasm of Challenges Cave of Wonders Map", locationCategory.CHEST,[locationType.Agrabah]),
                                        KH2Location(37, "Chasm of Challenges AP Boost", locationCategory.CHEST,[locationType.Agrabah]),]))
        self.add_node("Treasure Room Bonus",LocationNode([KH2Location(46, "Treasure Room", locationCategory.STATBONUS,[locationType.Agrabah]),]))
        self.add_node("Treasure Room",LocationNode([KH2Location(502, "Treasure Room AP Boost", locationCategory.CHEST,[locationType.Agrabah]),
                                         KH2Location(503, "Treasure Room Serenity Gem", locationCategory.CHEST,[locationType.Agrabah]),]))
        self.add_node("Elemental Lords",LocationNode([KH2Location(37, "Elemental Lords", locationCategory.ITEMBONUS,[locationType.Agrabah]),
                                         KH2Location(300, "Lamp Charm", locationCategory.POPUP,[locationType.Agrabah]),]))
        self.add_node("Ruined Chamber",LocationNode([KH2Location(34, "Ruined Chamber Torn Pages", locationCategory.CHEST,[locationType.Agrabah]),
                                         KH2Location(486, "Ruined Chamber Ruins Map", locationCategory.CHEST,[locationType.Agrabah]),]))
        self.add_node("Genie Jafar",LocationNode([KH2Location(15, "Genie Jafar", locationCategory.ITEMBONUS,[locationType.Agrabah]),
                                         KH2Location(303, "Wishing Lamp", locationCategory.POPUP,[locationType.Agrabah]),]))
        self.add_node("AS Lexaeus",LocationNode([KH2Location(65, "Lexaeus Bonus", locationCategory.STATBONUS,[locationType.Agrabah, locationType.AS]),
                                         KH2Location(545, "Lexaeus (AS) Strength Beyond Strength", locationCategory.POPUP,[locationType.Agrabah, locationType.AS]),]))
        self.add_node("Data Lexaeus",LocationNode([KH2Location(550, "Lexaeus (Data) Lost Illusion", locationCategory.POPUP,[locationType.Agrabah, locationType.DataOrg]),]))

        self.data_nodes.append("Data Lexaeus")

        if not self.reverse_rando:
            self.add_edge("Starting","Agrabah Map Popup",RequirementEdge())
            self.add_edge("Agrabah Map Popup","Agrabah",RequirementEdge())
            self.add_edge("Agrabah","Bazaar",RequirementEdge())
            self.add_edge("Bazaar","Palace Walls",RequirementEdge())
            self.add_edge("Palace Walls","Cave of Wonders Entrance",RequirementEdge())
            self.add_edge("Cave of Wonders Entrance","Valley of Stone",RequirementEdge())
            self.add_edge("Valley of Stone","Abu Escort",RequirementEdge())
            self.add_edge("Abu Escort","Chasm of Challenges",RequirementEdge(battle=True))
            self.add_edge("Chasm of Challenges","Treasure Room Bonus",RequirementEdge(battle=True))
            self.add_edge("Treasure Room Bonus","Treasure Room",RequirementEdge())
            self.add_edge("Treasure Room","Elemental Lords",RequirementEdge(battle=True))
            self.add_edge("Elemental Lords","Ruined Chamber",RequirementEdge(battle=True,req=lambda inv : ItemPlacementHelpers.need_fire_blizzard_thunder(inv) and ItemPlacementHelpers.aladdin_check(inv)))
            self.add_edge("Ruined Chamber","Genie Jafar",RequirementEdge(battle=True))
            self.add_edge("Genie Jafar","AS Lexaeus",RequirementEdge(battle=True))
            self.add_edge("AS Lexaeus","Data Lexaeus",RequirementEdge())
            self.first_boss_nodes.append("Elemental Lords")
            self.second_boss_nodes.append("Genie Jafar")
        else:
            self.add_edge("Starting","Agrabah",RequirementEdge())
            self.add_edge("Agrabah","Bazaar",RequirementEdge())
            self.add_edge("Bazaar","Palace Walls",RequirementEdge())
            self.add_edge("Palace Walls","Ruined Chamber",RequirementEdge(battle=True,req=ItemPlacementHelpers.need_fire_blizzard_thunder))
            self.add_edge("Ruined Chamber","Genie Jafar",RequirementEdge(battle=True))
            self.add_edge("Genie Jafar","AS Lexaeus",RequirementEdge(battle=True))
            self.add_edge("AS Lexaeus","Agrabah Map Popup",RequirementEdge(req=ItemPlacementHelpers.aladdin_check))
            self.add_edge("Agrabah Map Popup","Cave of Wonders Entrance",RequirementEdge())
            self.add_edge("Cave of Wonders Entrance","Valley of Stone",RequirementEdge())
            self.add_edge("Valley of Stone","Abu Escort",RequirementEdge())
            self.add_edge("Abu Escort","Chasm of Challenges",RequirementEdge(battle=True))
            self.add_edge("Chasm of Challenges","Treasure Room Bonus",RequirementEdge(battle=True))
            self.add_edge("Treasure Room Bonus","Treasure Room",RequirementEdge())
            self.add_edge("Treasure Room","Elemental Lords",RequirementEdge(battle=True))
            self.add_edge("Elemental Lords","Data Lexaeus",RequirementEdge(battle=True))
            self.first_boss_nodes.append("Genie Jafar")
            self.second_boss_nodes.append("Elemental Lords")

    def makeDCGraph(self):
        self.add_node("DC Courtyard",LocationNode([KH2Location(16, "DC Courtyard Mythril Shard", locationCategory.CHEST,[locationType.DC]),
                                        KH2Location(17, "DC Courtyard Star Recipe", locationCategory.CHEST,[locationType.DC]),
                                        KH2Location(18, "DC Courtyard AP Boost", locationCategory.CHEST,[locationType.DC]),
                                        KH2Location(92, "DC Courtyard Mythril Stone", locationCategory.CHEST,[locationType.DC]),
                                        KH2Location(93, "DC Courtyard Blazing Stone", locationCategory.CHEST,[locationType.DC]),
                                        KH2Location(247, "DC Courtyard Blazing Shard", locationCategory.CHEST,[locationType.DC]),
                                        KH2Location(248, "DC Courtyard Mythril Shard (2)", locationCategory.CHEST,[locationType.DC]),]))
        self.add_node("Library",LocationNode([KH2Location(91, "Library Torn Pages", locationCategory.CHEST,[locationType.DC]),]))
        self.add_node("Library Popup",LocationNode([KH2Location(332, "Disney Castle Map", locationCategory.POPUP,[locationType.DC]),]))
        self.add_node("Minnie Escort",LocationNode([KH2Location(38, "Minnie Escort", locationCategory.HYBRIDBONUS,[locationType.DC]),]))
        self.add_node("Cornerstone Hill",LocationNode([KH2Location(79, "Cornerstone Hill Map", locationCategory.CHEST,[locationType.DC]),
                                        KH2Location(12, "Cornerstone Hill Frost Shard", locationCategory.CHEST,[locationType.DC]),]))
        self.add_node("Pier",LocationNode([KH2Location(81, "Pier Mythril Shard", locationCategory.CHEST,[locationType.DC]),
                                        KH2Location(82, "Pier Hi-Potion", locationCategory.CHEST,[locationType.DC]),]))
        self.add_node("Waterway",LocationNode([KH2Location(83, "Waterway Mythril Stone", locationCategory.CHEST,[locationType.DC]),
                                        KH2Location(84, "Waterway AP Boost", locationCategory.CHEST,[locationType.DC]),
                                        KH2Location(85, "Waterway Frost Stone", locationCategory.CHEST,[locationType.DC]),]))
        self.add_node("Windows Popup",LocationNode([KH2Location(368, "Window of Time Map", locationCategory.POPUP,[locationType.DC]),]))
        self.add_node("Boat Pete",LocationNode([KH2Location(16, "Boat Pete", locationCategory.ITEMBONUS,[locationType.DC]),]))
        self.add_node("Future Pete",LocationNode([KH2Location(17, "Future Pete", locationCategory.HYBRIDBONUS,[locationType.DC]),
                                        KH2Location(261, "Monochrome", locationCategory.POPUP,[locationType.DC]),]))
        self.add_node("Wisdom Popup",LocationNode([KH2Location(262, "Wisdom Form", locationCategory.POPUP,[locationType.DC]),]))
        self.add_node("AS Marluxia",LocationNode([KH2Location(67, "Marluxia Bonus", locationCategory.STATBONUS,[locationType.DC, locationType.AS]),
                                        KH2Location(548, "Marluxia (AS) Eternal Blossom", locationCategory.POPUP,[locationType.DC, locationType.AS]),]))
        self.add_node("Data Marluxia",LocationNode([KH2Location(553, "Marluxia (Data) Lost Illusion", locationCategory.POPUP,[locationType.DC, locationType.DataOrg]),]))
        self.add_node("Lingering Will",LocationNode([KH2Location(70, "Lingering Will Bonus", locationCategory.STATBONUS,[locationType.DC, locationType.LW], InvalidChecks=[itemType.PROOF_OF_CONNECTION]),
                                        KH2Location(587, "Lingering Will Proof of Connection", locationCategory.POPUP,[locationType.DC, locationType.LW], InvalidChecks=[itemType.PROOF_OF_CONNECTION]),
                                        KH2Location(591, "Lingering Will Manifest Illusion", locationCategory.POPUP,[locationType.DC, locationType.LW], InvalidChecks=[itemType.PROOF_OF_CONNECTION]),]))
        self.data_nodes.append("Data Marluxia")
        self.data_nodes.append("Lingering Will")
        self.first_boss_nodes.append("Wisdom Popup")
        self.second_boss_nodes.append("Wisdom Popup")

        if not self.reverse_rando:
            self.add_edge("Starting","DC Courtyard",RequirementEdge())
            self.add_edge("DC Courtyard","Library",RequirementEdge())
            self.add_edge("Library","Library Popup",RequirementEdge())
            self.add_edge("Library Popup","Minnie Escort",RequirementEdge())
            self.add_edge("Minnie Escort","Cornerstone Hill",RequirementEdge())
            self.add_edge("Cornerstone Hill","Pier",RequirementEdge())
            self.add_edge("Pier","Waterway",RequirementEdge(battle=True))
            self.add_edge("Waterway","Windows Popup",RequirementEdge(battle=True))
            self.add_edge("Windows Popup","Boat Pete",RequirementEdge(battle=True))
            self.add_edge("Boat Pete","Future Pete",RequirementEdge(battle=True))
            self.add_edge("Future Pete","Wisdom Popup",RequirementEdge())
            self.add_edge("Wisdom Popup","AS Marluxia",RequirementEdge(battle=True))
            self.add_edge("AS Marluxia","Data Marluxia",RequirementEdge())
            self.add_edge("Wisdom Popup","Lingering Will",RequirementEdge(battle=True,req=ItemPlacementHelpers.need_proof_connection))
        else:
            self.add_edge("Starting","Cornerstone Hill",RequirementEdge())
            self.add_edge("Cornerstone Hill","Pier",RequirementEdge())
            self.add_edge("Pier","Waterway",RequirementEdge(battle=True))
            self.add_edge("Waterway","Windows Popup",RequirementEdge(battle=True))
            self.add_edge("Windows Popup","Boat Pete",RequirementEdge(battle=True))
            self.add_edge("Boat Pete","Future Pete",RequirementEdge(battle=True))
            self.add_edge("Future Pete","AS Marluxia",RequirementEdge(battle=True))
            self.add_edge("AS Marluxia","DC Courtyard",RequirementEdge())
            self.add_edge("DC Courtyard","Library",RequirementEdge())
            self.add_edge("Library","Library Popup",RequirementEdge())
            self.add_edge("Library Popup","Minnie Escort",RequirementEdge())
            self.add_edge("Minnie Escort","Wisdom Popup",RequirementEdge())
            self.add_edge("Wisdom Popup","Data Marluxia",RequirementEdge(battle=True))
            self.add_edge("Wisdom Popup","Lingering Will",RequirementEdge(battle=True,req=ItemPlacementHelpers.need_proof_connection))


    def makeHundredAcreGraph(self):
        self.add_node("Pooh's Howse",LocationNode([KH2Location(313, "Pooh's House 100 Acre Wood Map", locationCategory.CHEST,[locationType.HUNDREDAW]),
                                        KH2Location(97, "Pooh's House AP Boost", locationCategory.CHEST,[locationType.HUNDREDAW]),
                                        KH2Location(98, "Pooh's House Mythril Stone", locationCategory.CHEST,[locationType.HUNDREDAW]),]))
        self.add_node("Piglet's Howse",LocationNode([KH2Location(105, "Piglet's House Defense Boost", locationCategory.CHEST,[locationType.HUNDREDAW]),
                                        KH2Location(103, "Piglet's House AP Boost", locationCategory.CHEST,[locationType.HUNDREDAW]),
                                        KH2Location(104, "Piglet's House Mythril Gem", locationCategory.CHEST,[locationType.HUNDREDAW]),]))
        self.add_node("Rabbit's Howse",LocationNode([KH2Location(314, "Rabbit's House Draw Ring", locationCategory.CHEST,[locationType.HUNDREDAW]),
                                        KH2Location(100, "Rabbit's House Mythril Crystal", locationCategory.CHEST,[locationType.HUNDREDAW]),
                                        KH2Location(101, "Rabbit's House AP Boost", locationCategory.CHEST,[locationType.HUNDREDAW]),]))
        self.add_node("Kanga's Howse",LocationNode([KH2Location(108, "Kanga's House Magic Boost", locationCategory.CHEST,[locationType.HUNDREDAW]),
                                        KH2Location(106, "Kanga's House AP Boost", locationCategory.CHEST,[locationType.HUNDREDAW]),
                                        KH2Location(107, "Kanga's House Orichalcum", locationCategory.CHEST,[locationType.HUNDREDAW]),]))
        self.add_node("Spooky Cave",LocationNode([KH2Location(110, "Spooky Cave Mythril Gem", locationCategory.CHEST,[locationType.HUNDREDAW]),
                                        KH2Location(111, "Spooky Cave AP Boost", locationCategory.CHEST,[locationType.HUNDREDAW]),
                                        KH2Location(112, "Spooky Cave Orichalcum", locationCategory.CHEST,[locationType.HUNDREDAW]),
                                        KH2Location(113, "Spooky Cave Guard Recipe", locationCategory.CHEST,[locationType.HUNDREDAW]),
                                        KH2Location(115, "Spooky Cave Mythril Crystal", locationCategory.CHEST,[locationType.HUNDREDAW]),
                                        KH2Location(116, "Spooky Cave AP Boost (2)", locationCategory.CHEST,[locationType.HUNDREDAW]),
                                        KH2Location(284, "Sweet Memories", locationCategory.POPUP,[locationType.HUNDREDAW]),
                                        KH2Location(485, "Spooky Cave Map", locationCategory.POPUP,[locationType.HUNDREDAW]),]))
        self.add_node("Starry Hill",LocationNode([KH2Location(312, "Starry Hill Cosmic Ring", locationCategory.CHEST,[locationType.HUNDREDAW]),
                                        KH2Location(94, "Starry Hill Style Recipe", locationCategory.CHEST,[locationType.HUNDREDAW]),
                                        KH2Location(285, "Starry Hill Cure Element", locationCategory.POPUP,[locationType.HUNDREDAW]),
                                        KH2Location(539, "Starry Hill Orichalcum+", locationCategory.POPUP,[locationType.HUNDREDAW]),]))

        if not self.reverse_rando:
            self.add_edge("Starting","Pooh's Howse",RequirementEdge())
            self.add_edge("Pooh's Howse","Piglet's Howse",RequirementEdge(req=ItemPlacementHelpers.need_1_page))
            self.add_edge("Piglet's Howse","Rabbit's Howse",RequirementEdge(req=ItemPlacementHelpers.need_2_pages))
            self.add_edge("Rabbit's Howse","Kanga's Howse",RequirementEdge(req=ItemPlacementHelpers.need_3_pages))
            self.add_edge("Kanga's Howse","Spooky Cave",RequirementEdge(req=ItemPlacementHelpers.need_4_pages))
            self.add_edge("Spooky Cave","Starry Hill",RequirementEdge(req=ItemPlacementHelpers.need_5_pages))
        else:
            self.add_edge("Starting","Starry Hill",RequirementEdge())
            self.add_edge("Starry Hill","Spooky Cave",RequirementEdge(req=ItemPlacementHelpers.need_1_page))
            self.add_edge("Spooky Cave","Kanga's Howse",RequirementEdge(req=ItemPlacementHelpers.need_2_pages))
            self.add_edge("Kanga's Howse","Rabbit's Howse",RequirementEdge(req=ItemPlacementHelpers.need_3_pages))
            self.add_edge("Rabbit's Howse","Piglet's Howse",RequirementEdge(req=ItemPlacementHelpers.need_4_pages))
            self.add_edge("Piglet's Howse","Pooh's Howse",RequirementEdge(req=ItemPlacementHelpers.need_5_pages))


    def makeOCGraph(self):
        self.add_node("Passage",LocationNode([KH2Location(7,"Passage Mythril Shard", locationCategory.CHEST,[locationType.OC]),
                                        KH2Location(8,"Passage Mythril Stone", locationCategory.CHEST,[locationType.OC]),
                                        KH2Location(144, "Passage Ether", locationCategory.CHEST,[locationType.OC]),
                                        KH2Location(145, "Passage AP Boost", locationCategory.CHEST,[locationType.OC]),
                                        KH2Location(146, "Passage Hi-Potion", locationCategory.CHEST,[locationType.OC]),]))
        self.add_node("Inner Chamber",LocationNode([KH2Location(2,"Inner Chamber Underworld Map", locationCategory.CHEST,[locationType.OC]),
                                        KH2Location(243, "Inner Chamber Mythril Shard", locationCategory.CHEST,[locationType.OC]),]))
        self.add_node("Cerberus Bonus",LocationNode([KH2Location(5, "Cerberus", locationCategory.ITEMBONUS,[locationType.OC]),]))
        self.add_node("Coliseum Map Popup",LocationNode([KH2Location(338, "Coliseum Map", locationCategory.POPUP,[locationType.OC]),]))
        self.add_node("Urns Bonus",LocationNode([KH2Location(57, "Urns", locationCategory.ITEMBONUS,[locationType.OC]),]))
        self.add_node("Underworld Entrance",LocationNode([KH2Location(242, "Underworld Entrance Power Boost", locationCategory.CHEST,[locationType.OC]),]))
        self.add_node("Caverns Entrance",LocationNode([KH2Location(3,"Caverns Entrance Lucid Shard", locationCategory.CHEST,[locationType.OC]),
                                        KH2Location(11, "Caverns Entrance AP Boost", locationCategory.CHEST,[locationType.OC]),
                                        KH2Location(504, "Caverns Entrance Mythril Shard", locationCategory.CHEST,[locationType.OC]),]))
        self.add_node("Lost Road",LocationNode([KH2Location(9,"The Lost Road Bright Shard", locationCategory.CHEST,[locationType.OC]),
                                        KH2Location(10, "The Lost Road Ether", locationCategory.CHEST,[locationType.OC]),
                                        KH2Location(148, "The Lost Road Mythril Shard", locationCategory.CHEST,[locationType.OC]),
                                        KH2Location(149, "The Lost Road Mythril Stone", locationCategory.CHEST,[locationType.OC]),]))
        self.add_node("Atrium",LocationNode([KH2Location(150, "Atrium Lucid Stone", locationCategory.CHEST,[locationType.OC]),
                                        KH2Location(151, "Atrium AP Boost", locationCategory.CHEST,[locationType.OC]),]))
        self.add_node("Demyx (OC)",LocationNode([KH2Location(58, "Demyx OC", locationCategory.STATBONUS,[locationType.OC]),
                                        KH2Location(529, "Secret Ansem Report 5", locationCategory.POPUP,[locationType.OC]),
                                        KH2Location(293, "Olympus Stone", locationCategory.POPUP,[locationType.OC]),]))
        self.add_node("The Lock",LocationNode([KH2Location(244, "The Lock Caverns Map", locationCategory.CHEST,[locationType.OC]),
                                        KH2Location(5,"The Lock Mythril Shard", locationCategory.CHEST,[locationType.OC]),
                                        KH2Location(142, "The Lock AP Boost", locationCategory.CHEST,[locationType.OC]),]))
        self.add_node("Pete (OC)",LocationNode([KH2Location(6, "Pete (OC)", locationCategory.ITEMBONUS,[locationType.OC]),]))
        self.add_node("Hydra",LocationNode([KH2Location(7, "Hydra", locationCategory.HYBRIDBONUS,[locationType.OC]),
                                        KH2Location(260, "Hero's Crest", locationCategory.POPUP,[locationType.OC]),]))
        self.add_node("Auron Statue",LocationNode([KH2Location(295, "Auron's Statue", locationCategory.POPUP,[locationType.OC]),]))
        self.add_node("Hades",LocationNode([KH2Location(8, "Hades", locationCategory.HYBRIDBONUS,[locationType.OC]),
                                        KH2Location(272, "Guardian Soul", locationCategory.POPUP,[locationType.OC]),]))
        self.add_node("Pain and Panic Cup",LocationNode([KH2Location(513, "Protect Belt (Pain and Panic Cup)", locationCategory.POPUP,[locationType.OC, locationType.OCCups], InvalidChecks=[itemType.TROPHY]),
                                        KH2Location(540, "Serenity Gem (Pain and Panic Cup)", locationCategory.POPUP,[locationType.OC, locationType.OCCups], InvalidChecks=[itemType.TROPHY]),]))
        self.add_node("Cerberus Cup",LocationNode([KH2Location(515, "Rising Dragon (Cerberus Cup)", locationCategory.POPUP,[locationType.OC, locationType.OCCups], InvalidChecks=[itemType.TROPHY]),
                                        KH2Location(542, "Serenity Crystal (Cerberus Cup)", locationCategory.POPUP,[locationType.OC, locationType.OCCups], InvalidChecks=[itemType.TROPHY]),]))
        self.add_node("Titan Cup",LocationNode([KH2Location(514, "Genji Shield (Titan Cup)", locationCategory.POPUP,[locationType.OC, locationType.OCCups], InvalidChecks=[itemType.TROPHY]),
                                        KH2Location(541, "Skillful Ring (Titan Cup)", locationCategory.POPUP,[locationType.OC, locationType.OCCups], InvalidChecks=[itemType.TROPHY]),]))
        self.add_node("Goddess of Fate Cup",LocationNode([KH2Location(516, "Fatal Crest (Goddess of Fate Cup)", locationCategory.POPUP,[locationType.OC, locationType.OCCups], InvalidChecks=[itemType.TROPHY]),
                                        KH2Location(517, "Orichalcum+ (Goddess of Fate Cup)", locationCategory.POPUP,[locationType.OC, locationType.OCCups], InvalidChecks=[itemType.TROPHY]),]))
        self.add_node("Paradox Cups",LocationNode([KH2Location(518, "Hades Cup Trophy (Paradox Cups)", locationCategory.POPUP,[locationType.OC, locationType.OCCups, locationType.OCParadoxCup], InvalidChecks=[itemType.TROPHY, itemType.FORM, itemType.SUMMON]),]))
        self.add_node("AS Zexion",LocationNode([KH2Location(66, "Zexion Bonus", locationCategory.STATBONUS,[locationType.OC, locationType.AS]),
                                        KH2Location(546, "Zexion (AS) Book of Shadows", locationCategory.POPUP,[locationType.OC, locationType.AS]),]))
        self.add_node("Data Zexion",LocationNode([KH2Location(551, "Zexion (Data) Lost Illusion", locationCategory.POPUP,[locationType.OC, locationType.DataOrg]),]))

        self.data_nodes.append("Data Zexion")

        if not self.reverse_rando:
            self.add_edge("Starting","Passage",RequirementEdge())
            self.add_edge("Passage","Inner Chamber",RequirementEdge())
            self.add_edge("Inner Chamber","Cerberus Bonus",RequirementEdge(battle=True))
            self.add_edge("Cerberus Bonus","Coliseum Map Popup",RequirementEdge())
            self.add_edge("Coliseum Map Popup","Urns Bonus",RequirementEdge())
            self.add_edge("Urns Bonus","Underworld Entrance",RequirementEdge())
            self.add_edge("Underworld Entrance","Caverns Entrance",RequirementEdge())
            self.add_edge("Caverns Entrance","Lost Road",RequirementEdge())
            self.add_edge("Lost Road","Atrium",RequirementEdge())
            self.add_edge("Atrium","Demyx (OC)",RequirementEdge(battle=True))
            self.add_edge("Demyx (OC)","The Lock",RequirementEdge())
            self.add_edge("The Lock","Pete (OC)",RequirementEdge(battle=True))
            self.add_edge("Pete (OC)","Hydra",RequirementEdge(battle=True))
            self.add_edge("Hydra","Auron Statue",RequirementEdge(battle=True,req=ItemPlacementHelpers.auron_check))
            self.add_edge("Auron Statue","Hades",RequirementEdge(battle=True))

            self.add_edge("Hades","Pain and Panic Cup",RequirementEdge(battle=True))
            self.add_edge("Hades","Cerberus Cup",RequirementEdge(battle=True))
            self.add_edge("Hades","Titan Cup",RequirementEdge(battle=True))
            self.add_edge("Hades","Goddess of Fate Cup",RequirementEdge(battle=True))
            self.add_edge("Hades","Paradox Cups",RequirementEdge(battle=True,req=lambda inv: ItemPlacementHelpers.need_forms(inv) and ItemPlacementHelpers.need_summons(inv)))
            self.add_edge("Hades","AS Zexion",RequirementEdge(battle=True))
            self.add_edge("AS Zexion","Data Zexion",RequirementEdge())
            self.first_boss_nodes.append("Hydra")
            self.second_boss_nodes.append("Hades")
        else:
            self.add_edge("Starting","Underworld Entrance",RequirementEdge())
            self.add_edge("Underworld Entrance","Passage",RequirementEdge())
            self.add_edge("Passage","Inner Chamber",RequirementEdge())
            self.add_edge("Inner Chamber","Auron Statue",RequirementEdge(battle=True))
            self.add_edge("Auron Statue","Hades",RequirementEdge(battle=True))
            self.add_edge("Hades","AS Zexion",RequirementEdge(battle=True))
            self.add_edge("AS Zexion","Cerberus Bonus",RequirementEdge(battle=True,req=ItemPlacementHelpers.auron_check))
            self.add_edge("Cerberus Bonus","Coliseum Map Popup",RequirementEdge())
            self.add_edge("Coliseum Map Popup","Urns Bonus",RequirementEdge())
            self.add_edge("Urns Bonus","Caverns Entrance",RequirementEdge())
            self.add_edge("Caverns Entrance","Lost Road",RequirementEdge())
            self.add_edge("Lost Road","Atrium",RequirementEdge())
            self.add_edge("Atrium","Demyx (OC)",RequirementEdge(battle=True))
            self.add_edge("Demyx (OC)","The Lock",RequirementEdge())
            self.add_edge("The Lock","Pete (OC)",RequirementEdge(battle=True))
            self.add_edge("Pete (OC)","Hydra",RequirementEdge(battle=True))
            self.add_edge("Hydra","Pain and Panic Cup",RequirementEdge(battle=True))
            self.add_edge("Hydra","Cerberus Cup",RequirementEdge(battle=True))
            self.add_edge("Hydra","Titan Cup",RequirementEdge(battle=True))
            self.add_edge("Hydra","Goddess of Fate Cup",RequirementEdge(battle=True))
            self.add_edge("Hydra","Paradox Cups",RequirementEdge(battle=True,req=lambda inv: ItemPlacementHelpers.need_forms(inv) and ItemPlacementHelpers.need_summons(inv)))
            self.add_edge("Hydra","Data Zexion",RequirementEdge(battle=True))
            self.first_boss_nodes.append("Hades")
            self.second_boss_nodes.append("Hydra")


    def makeBCGraph(self):
        self.add_node("BC Courtyard",LocationNode([KH2Location(39, "BC Courtyard AP Boost", locationCategory.CHEST,[locationType.BC]),
                                        KH2Location(40, "BC Courtyard Hi-Potion", locationCategory.CHEST,[locationType.BC]),
                                        KH2Location(505, "BC Courtyard Mythril Shard", locationCategory.CHEST,[locationType.BC]),]))
        self.add_node("Belle's Room",LocationNode([KH2Location(46, "Belle's Room Castle Map", locationCategory.CHEST,[locationType.BC]),
                                        KH2Location(240, "Belle's Room Mega-Recipe", locationCategory.CHEST,[locationType.BC]),]))
        self.add_node("East Wing",LocationNode([KH2Location(63, "The East Wing Mythril Shard", locationCategory.CHEST,[locationType.BC]),
                                        KH2Location(155, "The East Wing Tent", locationCategory.CHEST,[locationType.BC]),]))
        self.add_node("West Hall",LocationNode([KH2Location(41, "The West Hall Hi-Potion", locationCategory.CHEST,[locationType.BC]),
                                        KH2Location(207, "The West Hall Power Shard", locationCategory.CHEST,[locationType.BC]),
                                        KH2Location(158, "The West Hall AP Boost", locationCategory.CHEST,[locationType.BC]),
                                        KH2Location(159, "The West Hall Bright Stone", locationCategory.CHEST,[locationType.BC]),
                                        KH2Location(206, "The West Hall Mythril Shard", locationCategory.CHEST,[locationType.BC]),]))
        self.add_node("Thresholder",LocationNode([KH2Location(2, "Thresholder", locationCategory.ITEMBONUS,[locationType.BC]),]))
        self.add_node("Dungeon",LocationNode([KH2Location(239, "Dungeon Basement Map", locationCategory.CHEST,[locationType.BC]),
                                        KH2Location(43, "Dungeon AP Boost", locationCategory.CHEST,[locationType.BC]),]))
        self.add_node("Secret Passage",LocationNode([KH2Location(44, "Secret Passage Mythril Shard", locationCategory.CHEST,[locationType.BC]),
                                        KH2Location(168, "Secret Passage Hi-Potion", locationCategory.CHEST,[locationType.BC]),
                                        KH2Location(45, "Secret Passage Lucid Shard", locationCategory.CHEST,[locationType.BC]),]))
        self.add_node("West Hall Post Dungeon",LocationNode([KH2Location(208, "The West Hall Mythril Shard (Post Dungeon)", locationCategory.CHEST,[locationType.BC]),]))
        self.add_node("West Wing",LocationNode([KH2Location(42, "The West Wing Mythril Shard", locationCategory.CHEST,[locationType.BC]),
                                        KH2Location(164, "The West Wing Tent", locationCategory.CHEST,[locationType.BC]),]))
        self.add_node("Beast Bonus",LocationNode([KH2Location(12, "Beast", locationCategory.STATBONUS,[locationType.BC]),]))
        self.add_node("Beast's Room",LocationNode([KH2Location(241, "The Beast's Room Blazing Shard", locationCategory.CHEST,[locationType.BC]),]))
        self.add_node("Dark Thorn",LocationNode([KH2Location(3, "Dark Thorn Bonus", locationCategory.HYBRIDBONUS,[locationType.BC]),
                                        KH2Location(299, "Dark Thorn Cure Element", locationCategory.POPUP,[locationType.BC]),]))
        self.add_node("Rumbling Rose",LocationNode([KH2Location(270, "Rumbling Rose", locationCategory.POPUP,[locationType.BC]),
                                        KH2Location(325, "Castle Walls Map", locationCategory.POPUP,[locationType.BC]),]))
        self.add_node("Xaldin",LocationNode([KH2Location(4, "Xaldin Bonus", locationCategory.HYBRIDBONUS,[locationType.BC]),
                                        KH2Location(528, "Secret Ansem Report 6", locationCategory.POPUP,[locationType.BC]),]))
        self.add_node("Data Xaldin",LocationNode([KH2Location(559, "Xaldin (Data) Defense Boost", locationCategory.POPUP,[locationType.BC, locationType.DataOrg]),]))

        self.data_nodes.append("Data Xaldin")

        if not self.reverse_rando:
            self.add_edge("Starting","BC Courtyard",RequirementEdge())
            self.add_edge("BC Courtyard","Belle's Room",RequirementEdge())
            self.add_edge("Belle's Room","East Wing",RequirementEdge())
            self.add_edge("BC Courtyard","West Hall",RequirementEdge())
            self.add_edge("West Hall","Thresholder",RequirementEdge(battle=True))
            self.add_edge("Thresholder","Dungeon",RequirementEdge())
            self.add_edge("Dungeon","Secret Passage",RequirementEdge())
            self.add_edge("Secret Passage","West Hall Post Dungeon",RequirementEdge())
            self.add_edge("West Hall Post Dungeon","West Wing",RequirementEdge())
            self.add_edge("West Wing","Beast Bonus",RequirementEdge(battle=True))
            self.add_edge("Beast Bonus","Beast's Room",RequirementEdge())
            self.add_edge("Beast's Room","Dark Thorn",RequirementEdge(battle=True))
            self.add_edge("Dark Thorn","Rumbling Rose",RequirementEdge(battle=True,req=ItemPlacementHelpers.beast_check))
            self.add_edge("Rumbling Rose","Xaldin",RequirementEdge(battle=True))
            self.add_edge("Xaldin","Data Xaldin",RequirementEdge(battle=True))
            self.first_boss_nodes.append("Dark Thorn")
            self.second_boss_nodes.append("Xaldin")
        else:
            self.add_edge("Starting","West Hall",RequirementEdge(battle=True))
            self.add_edge("West Hall","West Hall Post Dungeon",RequirementEdge())
            self.add_edge("West Hall","West Wing",RequirementEdge())
            self.add_edge("West Wing","Beast's Room",RequirementEdge())
            self.add_edge("Beast's Room","Rumbling Rose",RequirementEdge())
            self.add_edge("Rumbling Rose","Xaldin",RequirementEdge(battle=True))
            self.add_edge("Xaldin","BC Courtyard",RequirementEdge(req=ItemPlacementHelpers.beast_check))
            self.add_edge("BC Courtyard","Belle's Room",RequirementEdge())
            self.add_edge("Belle's Room","East Wing",RequirementEdge())
            self.add_edge("East Wing","Thresholder",RequirementEdge(battle=True))
            self.add_edge("Thresholder","Dungeon",RequirementEdge())
            self.add_edge("Dungeon","Secret Passage",RequirementEdge())
            self.add_edge("Secret Passage","Beast Bonus",RequirementEdge(battle=True))
            self.add_edge("Beast Bonus","Dark Thorn",RequirementEdge(battle=True))
            self.add_edge("Dark Thorn","Data Xaldin",RequirementEdge(battle=True))
            self.first_boss_nodes.append("Xaldin")
            self.second_boss_nodes.append("Dark Thorn")


    def makeSPGraph(self):
        self.add_node("Pit Cell",LocationNode([KH2Location(316, "Pit Cell Area Map", locationCategory.CHEST,[locationType.SP]),
                                        KH2Location(64, "Pit Cell Mythril Crystal", locationCategory.CHEST,[locationType.SP]),]))
        self.add_node("Canyon",LocationNode([KH2Location(65, "Canyon Dark Crystal", locationCategory.CHEST,[locationType.SP]),
                                        KH2Location(171, "Canyon Mythril Stone", locationCategory.CHEST,[locationType.SP]),
                                        KH2Location(253, "Canyon Mythril Gem", locationCategory.CHEST,[locationType.SP]),
                                        KH2Location(521, "Canyon Frost Crystal", locationCategory.CHEST,[locationType.SP]),]))
        self.add_node("Screens Bonus",LocationNode([KH2Location(45, "Screens", locationCategory.STATBONUS,[locationType.SP]),]))
        self.add_node("Hallway",LocationNode([KH2Location(49, "Hallway Power Crystal", locationCategory.CHEST,[locationType.SP]),
                                        KH2Location(50, "Hallway AP Boost", locationCategory.CHEST,[locationType.SP]),]))
        self.add_node("Communications Room",LocationNode([KH2Location(255, "Communications Room I/O Tower Map", locationCategory.CHEST,[locationType.SP]),
                                        KH2Location(499, "Communications Room Gaia Belt", locationCategory.CHEST,[locationType.SP]),]))
        self.add_node("Hostile Program",LocationNode([KH2Location(31, "Hostile Program", locationCategory.HYBRIDBONUS,[locationType.SP]),]))
        self.add_node("Photon Debugger",LocationNode([KH2Location(267, "Photon Debugger", locationCategory.POPUP,[locationType.SP]),]))
        self.add_node("Solar Sailer Bonus",LocationNode([KH2Location(61, "Solar Sailer", locationCategory.ITEMBONUS,[locationType.SP]),]))
        self.add_node("Central Computer Core",LocationNode([KH2Location(177, "Central Computer Core AP Boost", locationCategory.CHEST,[locationType.SP]),
                                        KH2Location(178, "Central Computer Core Orichalcum+", locationCategory.CHEST,[locationType.SP]),
                                        KH2Location(51, "Central Computer Core Cosmic Arts", locationCategory.CHEST,[locationType.SP]),
                                        KH2Location(488, "Central Computer Core Map", locationCategory.CHEST,[locationType.SP]),]))
        self.add_node("MCP Bonus",LocationNode([KH2Location(32, "MCP", locationCategory.HYBRIDBONUS,[locationType.SP]),]))
        self.add_node("AS Larxene",LocationNode([KH2Location(68, "Larxene Bonus", locationCategory.STATBONUS,[locationType.SP, locationType.AS]),
                                        KH2Location(547, "Larxene (AS) Cloaked Thunder", locationCategory.POPUP,[locationType.SP, locationType.AS]),]))
        self.add_node("Data Larxene",LocationNode([KH2Location(552, "Larxene (Data) Lost Illusion", locationCategory.POPUP,[locationType.SP, locationType.DataOrg]),]))

        self.data_nodes.append("Data Larxene")

        if not self.reverse_rando:
            self.add_edge("Starting","Pit Cell",RequirementEdge())
            self.add_edge("Pit Cell","Canyon",RequirementEdge())
            self.add_edge("Canyon","Screens Bonus",RequirementEdge(battle=True))
            self.add_edge("Screens Bonus","Hallway",RequirementEdge())
            self.add_edge("Hallway","Communications Room",RequirementEdge())
            self.add_edge("Communications Room","Hostile Program",RequirementEdge(battle=True))
            self.add_edge("Hostile Program","Photon Debugger",RequirementEdge())
            self.add_edge("Photon Debugger","Solar Sailer Bonus",RequirementEdge(battle=True,req=ItemPlacementHelpers.tron_check))
            self.add_edge("Solar Sailer Bonus","Central Computer Core",RequirementEdge())
            self.add_edge("Central Computer Core","MCP Bonus",RequirementEdge(battle=True))
            self.add_edge("MCP Bonus","AS Larxene",RequirementEdge(battle=True))
            self.add_edge("AS Larxene","Data Larxene",RequirementEdge())
            self.first_boss_nodes.append("Photon Debugger")
            self.second_boss_nodes.append("MCP Bonus")
        else:
            self.add_edge("Starting","Pit Cell",RequirementEdge())
            self.add_edge("Pit Cell","Canyon",RequirementEdge())
            self.add_edge("Canyon","Communications Room",RequirementEdge(battle=True))
            self.add_edge("Communications Room","Hallway",RequirementEdge())
            self.add_edge("Hallway","Solar Sailer Bonus",RequirementEdge(battle=True))
            self.add_edge("Solar Sailer Bonus","Central Computer Core",RequirementEdge())
            self.add_edge("Central Computer Core","MCP Bonus",RequirementEdge(battle=True))
            self.add_edge("MCP Bonus","AS Larxene",RequirementEdge(battle=True))
            self.add_edge("AS Larxene","Screens Bonus",RequirementEdge(battle=True,req=ItemPlacementHelpers.tron_check))
            self.add_edge("Screens Bonus","Hostile Program",RequirementEdge(battle=True))
            self.add_edge("Hostile Program","Photon Debugger",RequirementEdge())
            self.add_edge("Photon Debugger","Data Larxene",RequirementEdge(battle=True))
            self.first_boss_nodes.append("MCP Bonus")
            self.second_boss_nodes.append("Photon Debugger")


    def makeHTGraph(self):
        self.add_node("Graveyard",LocationNode([KH2Location(53, "Graveyard Mythril Shard", locationCategory.CHEST,[locationType.HT]),
                                        KH2Location(212, "Graveyard Serenity Gem", locationCategory.CHEST,[locationType.HT]),]))
        self.add_node("Finklestein's Lab",LocationNode([KH2Location(211, "Finklestein's Lab Halloween Town Map", locationCategory.CHEST,[locationType.HT]),]))
        self.add_node("Town Square",LocationNode([KH2Location(209, "Town Square Mythril Stone", locationCategory.CHEST,[locationType.HT]),
                                        KH2Location(210, "Town Square Energy Shard", locationCategory.CHEST,[locationType.HT]),]))
        self.add_node("Hinterlands",LocationNode([KH2Location(54, "Hinterlands Lightning Shard", locationCategory.CHEST,[locationType.HT]),
                                        KH2Location(213, "Hinterlands Mythril Stone", locationCategory.CHEST,[locationType.HT]),
                                        KH2Location(214, "Hinterlands AP Boost", locationCategory.CHEST,[locationType.HT]),]))
        self.add_node("Candy Cane Lane",LocationNode([KH2Location(55, "Candy Cane Lane Mega-Potion", locationCategory.CHEST,[locationType.HT]),
                                        KH2Location(56, "Candy Cane Lane Mythril Gem", locationCategory.CHEST,[locationType.HT]),
                                        KH2Location(216, "Candy Cane Lane Lightning Stone", locationCategory.CHEST,[locationType.HT]),
                                        KH2Location(217, "Candy Cane Lane Mythril Stone", locationCategory.CHEST,[locationType.HT]),]))
        self.add_node("Santa's House",LocationNode([KH2Location(57, "Santa's House Christmas Town Map", locationCategory.CHEST,[locationType.HT]),
                                        KH2Location(58, "Santa's House AP Boost", locationCategory.CHEST,[locationType.HT]),]))
        self.add_node("Prison Keeper",LocationNode([KH2Location(18, "Prison Keeper", locationCategory.HYBRIDBONUS,[locationType.HT]),]))
        self.add_node("Oogie Boogie",LocationNode([KH2Location(19, "Oogie Boogie", locationCategory.STATBONUS,[locationType.HT]),
                                        KH2Location(301, "Oogie Boogie Magnet Element", locationCategory.POPUP,[locationType.HT]),]))
        self.add_node("Lock, Shock, and Barrel",LocationNode([KH2Location(40, "Lock, Shock, and Barrel", locationCategory.STATBONUS,[locationType.HT]),]))
        self.add_node("Presents",LocationNode([KH2Location(297, "Present", locationCategory.POPUP,[locationType.HT]),]))
        self.add_node("Decoy Present Minigame",LocationNode([KH2Location(298, "Decoy Presents", locationCategory.POPUP,[locationType.HT]),]))
        self.add_node("Experiment",LocationNode([KH2Location(20, "Experiment", locationCategory.STATBONUS,[locationType.HT]),
                                        KH2Location(275, "Decisive Pumpkin", locationCategory.POPUP,[locationType.HT]),]))
        self.add_node("AS Vexen",LocationNode([KH2Location(64, "Vexen Bonus", locationCategory.STATBONUS,[locationType.HT, locationType.AS]),
                                        KH2Location(544, "Vexen (AS) Road to Discovery", locationCategory.POPUP,[locationType.HT, locationType.AS]),]))
        self.add_node("Data Vexen",LocationNode([KH2Location(549, "Vexen (Data) Lost Illusion", locationCategory.POPUP,[locationType.HT, locationType.DataOrg])]))

        self.data_nodes.append("Data Vexen")

        if not self.reverse_rando:
            self.add_edge("Starting","Graveyard",RequirementEdge())
            self.add_edge("Graveyard","Finklestein's Lab",RequirementEdge())
            self.add_edge("Finklestein's Lab","Town Square",RequirementEdge())
            self.add_edge("Town Square","Hinterlands",RequirementEdge())
            self.add_edge("Hinterlands","Candy Cane Lane",RequirementEdge(battle=True))
            self.add_edge("Candy Cane Lane","Santa's House",RequirementEdge())
            self.add_edge("Santa's House","Prison Keeper",RequirementEdge(battle=True))
            self.add_edge("Prison Keeper","Oogie Boogie",RequirementEdge(battle=True))
            self.add_edge("Oogie Boogie","Lock, Shock, and Barrel",RequirementEdge(battle=True,req=ItemPlacementHelpers.jack_ht_check))
            self.add_edge("Lock, Shock, and Barrel","Presents",RequirementEdge(battle=True))
            self.add_edge("Presents","Decoy Present Minigame",RequirementEdge())
            self.add_edge("Decoy Present Minigame","Experiment",RequirementEdge(battle=True))
            self.add_edge("Experiment","AS Vexen",RequirementEdge(battle=True))
            self.add_edge("AS Vexen","Data Vexen",RequirementEdge())
            self.first_boss_nodes.append("Oogie Boogie")
            self.second_boss_nodes.append("Experiment")
        else:
            self.add_edge("Starting","Santa's House",RequirementEdge())
            self.add_edge("Santa's House","Candy Cane Lane",RequirementEdge())
            self.add_edge("Candy Cane Lane","Hinterlands",RequirementEdge())
            self.add_edge("Hinterlands","Graveyard",RequirementEdge())
            self.add_edge("Graveyard","Town Square",RequirementEdge())
            self.add_edge("Santa's House","Lock, Shock, and Barrel",RequirementEdge(battle=True))
            self.add_edge("Lock, Shock, and Barrel","Presents",RequirementEdge(battle=True))
            self.add_edge("Presents","Decoy Present Minigame",RequirementEdge())
            self.add_edge("Decoy Present Minigame","Experiment",RequirementEdge(battle=True))
            self.add_edge("Experiment","AS Vexen",RequirementEdge(battle=True))
            self.add_edge("AS Vexen","Finklestein's Lab",RequirementEdge(req=ItemPlacementHelpers.jack_ht_check))
            self.add_edge("Finklestein's Lab","Prison Keeper",RequirementEdge(battle=True))
            self.add_edge("Prison Keeper","Oogie Boogie",RequirementEdge(battle=True))
            self.add_edge("Oogie Boogie","Data Vexen",RequirementEdge(battle=True))
            self.first_boss_nodes.append("Experiment")
            self.second_boss_nodes.append("Oogie Boogie")

    
    def makePRGraph(self):
        self.add_node("Ramparts",LocationNode([KH2Location(70, "Rampart Naval Map", locationCategory.CHEST,[locationType.PR]),
                                        KH2Location(219, "Rampart Mythril Stone", locationCategory.CHEST,[locationType.PR]),
                                        KH2Location(220, "Rampart Dark Shard", locationCategory.CHEST,[locationType.PR]),]))
        self.add_node("PR Town",LocationNode([KH2Location(71, "Town Dark Stone", locationCategory.CHEST,[locationType.PR]),
                                        KH2Location(72, "Town AP Boost", locationCategory.CHEST,[locationType.PR]),
                                        KH2Location(73, "Town Mythril Shard", locationCategory.CHEST,[locationType.PR]),
                                        KH2Location(221, "Town Mythril Gem", locationCategory.CHEST,[locationType.PR]),]))
        self.add_node("Cave Mouth",LocationNode([KH2Location(74, "Cave Mouth Bright Shard", locationCategory.CHEST,[locationType.PR]),
                                        KH2Location(223, "Cave Mouth Mythril Shard", locationCategory.CHEST,[locationType.PR]),]))
        self.add_node("Isla de Meurta Popup",LocationNode([KH2Location(329, "Isla de Muerta Map", locationCategory.POPUP,[locationType.PR]),]))
        self.add_node("Boat Fight",LocationNode([KH2Location(62, "Boat Fight", locationCategory.ITEMBONUS,[locationType.PR]),]))
        self.add_node("Barrels Minigame",LocationNode([KH2Location(39, "Interceptor Barrels", locationCategory.STATBONUS,[locationType.PR]),]))
        self.add_node("Powder Store",LocationNode([KH2Location(369, "Powder Store AP Boost (1)", locationCategory.CHEST,[locationType.PR]),
                                        KH2Location(370, "Powder Store AP Boost (2)", locationCategory.CHEST,[locationType.PR]),]))
        self.add_node("Moonlight Nook",LocationNode([KH2Location(75, "Moonlight Nook Mythril Shard", locationCategory.CHEST,[locationType.PR]),
                                        KH2Location(224, "Moonlight Nook Serenity Gem", locationCategory.CHEST,[locationType.PR]),
                                        KH2Location(371, "Moonlight Nook Power Stone", locationCategory.CHEST,[locationType.PR]),]))
        self.add_node("Barbossa",LocationNode([KH2Location(21, "Barbossa", locationCategory.HYBRIDBONUS,[locationType.PR]),
                                        KH2Location(263, "Follow the Wind", locationCategory.POPUP,[locationType.PR]),]))
        self.add_node("Grim Reaper 1",LocationNode([KH2Location(59, "Grim Reaper 1", locationCategory.ITEMBONUS,[locationType.PR]),]))
        self.add_node("Interceptor's Hold",LocationNode([KH2Location(252, "Interceptor's Hold Feather Charm", locationCategory.CHEST,[locationType.PR]),]))
        self.add_node("Seadrift Keep",LocationNode([KH2Location(76, "Seadrift Keep AP Boost", locationCategory.CHEST,[locationType.PR]),
                                        KH2Location(225, "Seadrift Keep Orichalcum", locationCategory.CHEST,[locationType.PR]),
                                        KH2Location(372, "Seadrift Keep Meteor Staff", locationCategory.CHEST,[locationType.PR]),]))
        self.add_node("Seadrift Row",LocationNode([KH2Location(77, "Seadrift Row Serenity Gem", locationCategory.CHEST,[locationType.PR]),
                                        KH2Location(78, "Seadrift Row King Recipe", locationCategory.CHEST,[locationType.PR]),
                                        KH2Location(373, "Seadrift Row Mythril Crystal", locationCategory.CHEST,[locationType.PR]),]))
        self.add_node("Cursed Medallion Popup",LocationNode([KH2Location(296, "Seadrift Row Cursed Medallion", locationCategory.POPUP,[locationType.PR]),
                                        KH2Location(331, "Seadrift Row Ship Graveyard Map", locationCategory.POPUP,[locationType.PR]),]))
        self.add_node("Grim Reaper 2",LocationNode([KH2Location(22, "Grim Reaper 2", locationCategory.ITEMBONUS,[locationType.PR]),
                                        KH2Location(530, "Secret Ansem Report 4", locationCategory.POPUP,[locationType.PR]),]))
        self.add_node("Data Luxord",LocationNode([KH2Location(557, "Luxord (Data) AP Boost", locationCategory.POPUP,[locationType.PR, locationType.DataOrg]),]))

        self.data_nodes.append("Data Luxord")

        if not self.reverse_rando:
            self.add_edge("Starting","Ramparts",RequirementEdge())
            self.add_edge("Ramparts","PR Town",RequirementEdge(battle=True))
            self.add_edge("PR Town","Cave Mouth",RequirementEdge())
            self.add_edge("Cave Mouth","Isla de Meurta Popup",RequirementEdge(battle=True))
            self.add_edge("Isla de Meurta Popup","Boat Fight",RequirementEdge(battle=True))
            self.add_edge("Boat Fight","Barrels Minigame",RequirementEdge())
            self.add_edge("Barrels Minigame","Powder Store",RequirementEdge())
            self.add_edge("Powder Store","Moonlight Nook",RequirementEdge())
            self.add_edge("Moonlight Nook","Barbossa",RequirementEdge(battle=True))
            self.add_edge("Barbossa","Grim Reaper 1",RequirementEdge(battle=True,req=ItemPlacementHelpers.jack_pr_check))
            self.add_edge("Grim Reaper 1","Interceptor's Hold",RequirementEdge())
            self.add_edge("Interceptor's Hold","Seadrift Keep",RequirementEdge())
            self.add_edge("Seadrift Keep","Seadrift Row",RequirementEdge())
            self.add_edge("Seadrift Row","Cursed Medallion Popup",RequirementEdge(battle=True))
            self.add_edge("Cursed Medallion Popup","Grim Reaper 2",RequirementEdge(battle=True))
            self.add_edge("Grim Reaper 2","Data Luxord",RequirementEdge(battle=True))
            self.first_boss_nodes.append("Barbossa")
            self.second_boss_nodes.append("Grim Reaper 2")
        else:
            self.add_edge("Starting","Ramparts",RequirementEdge())
            self.add_edge("Ramparts","Grim Reaper 1",RequirementEdge(battle=True))
            self.add_edge("Grim Reaper 1","Interceptor's Hold",RequirementEdge())
            self.add_edge("Interceptor's Hold","Seadrift Keep",RequirementEdge())
            self.add_edge("Seadrift Keep","Seadrift Row",RequirementEdge())
            self.add_edge("Seadrift Row","Cursed Medallion Popup",RequirementEdge(battle=True))
            self.add_edge("Cursed Medallion Popup","Cave Mouth",RequirementEdge())
            self.add_edge("Cave Mouth","Grim Reaper 2",RequirementEdge(battle=True))
            self.add_edge("Grim Reaper 2","PR Town",RequirementEdge(battle=True,req=ItemPlacementHelpers.jack_pr_check))
            self.add_edge("PR Town","Isla de Meurta Popup",RequirementEdge(battle=True))
            self.add_edge("Isla de Meurta Popup","Boat Fight",RequirementEdge(battle=True))
            self.add_edge("Boat Fight","Barrels Minigame",RequirementEdge())
            self.add_edge("Barrels Minigame","Powder Store",RequirementEdge())
            self.add_edge("Powder Store","Moonlight Nook",RequirementEdge())
            self.add_edge("Moonlight Nook","Barbossa",RequirementEdge(battle=True))
            self.add_edge("Barbossa","Data Luxord",RequirementEdge(battle=True))
            self.first_boss_nodes.append("Grim Reaper 2")
            self.second_boss_nodes.append("Barbossa")


    def makeHBGraph(self):
        self.add_node("Marketplace Map Popup",LocationNode([KH2Location(362, "Marketplace Map", locationCategory.POPUP,[locationType.HB]),]))
        self.add_node("Borough",LocationNode([KH2Location(194, "Borough Drive Recovery", locationCategory.CHEST,[locationType.HB]),
                                        KH2Location(195, "Borough AP Boost", locationCategory.CHEST,[locationType.HB]),
                                        KH2Location(196, "Borough Hi-Potion", locationCategory.CHEST,[locationType.HB]),
                                        KH2Location(305, "Borough Mythril Shard", locationCategory.CHEST,[locationType.HB]),
                                        KH2Location(506, "Borough Dark Shard", locationCategory.CHEST,[locationType.HB]),]))
        self.add_node("Merlin's House Popup",LocationNode([KH2Location(256, "Merlin's House Membership Card", locationCategory.POPUP,[locationType.HB]),
                                        KH2Location(292, "Merlin's House Blizzard Element", locationCategory.POPUP,[locationType.HB]),]))
        self.add_node("Bailey",LocationNode([KH2Location(47, "Bailey", locationCategory.ITEMBONUS,[locationType.HB]),
                                        KH2Location(531, "Bailey Secret Ansem Report 7", locationCategory.POPUP,[locationType.HB]),]))
        self.add_node("Baseball Charm Popup",LocationNode([KH2Location(258, "Baseball Charm", locationCategory.POPUP,[locationType.HB]),]))
        self.add_node("Postern",LocationNode([KH2Location(310, "Postern Castle Perimeter Map", locationCategory.CHEST,[locationType.HB]),
                                        KH2Location(189, "Postern Mythril Gem", locationCategory.CHEST,[locationType.HB]),
                                        KH2Location(190, "Postern AP Boost", locationCategory.CHEST,[locationType.HB]),]))
        self.add_node("Cooridors",LocationNode([KH2Location(200, "Corridors Mythril Stone", locationCategory.CHEST,[locationType.HB]),
                                        KH2Location(201, "Corridors Mythril Crystal", locationCategory.CHEST,[locationType.HB]),
                                        KH2Location(202, "Corridors Dark Crystal", locationCategory.CHEST,[locationType.HB]),
                                        KH2Location(307, "Corridors AP Boost", locationCategory.CHEST,[locationType.HB]),]))
        self.add_node("DTD Popup",LocationNode([KH2Location(266, "Ansem's Study Master Form", locationCategory.POPUP,[locationType.HB]),
                                        KH2Location(276, "Ansem's Study Sleeping Lion", locationCategory.POPUP,[locationType.HB]),]))
        self.add_node("Ansem's Study",LocationNode([KH2Location(184, "Ansem's Study Skill Recipe", locationCategory.CHEST,[locationType.HB]),]))
        self.add_node("Ukulele Charm",LocationNode([KH2Location(183, "Ansem's Study Ukulele Charm", locationCategory.CHEST,[locationType.HB]),]))
        self.add_node("Restoration Site",LocationNode([KH2Location(309, "Restoration Site Moon Recipe", locationCategory.CHEST,[locationType.HB]),
                                        KH2Location(507, "Restoration Site AP Boost", locationCategory.CHEST,[locationType.HB]),]))
        self.add_node("Demyx (HB)",LocationNode([KH2Location(28, "Demyx (HB)", locationCategory.HYBRIDBONUS,[locationType.HB]),]))
        self.add_node("Final Fantasy Fights",LocationNode([KH2Location(361, "FF Fights Cure Element", locationCategory.POPUP,[locationType.HB]),]))
        self.add_node("Crystal Fissure",LocationNode([KH2Location(179, "Crystal Fissure Torn Pages", locationCategory.CHEST,[locationType.HB]),
                                        KH2Location(489, "Crystal Fissure The Great Maw Map", locationCategory.CHEST,[locationType.HB]),
                                        KH2Location(180, "Crystal Fissure Energy Crystal", locationCategory.CHEST,[locationType.HB]),
                                        KH2Location(181, "Crystal Fissure AP Boost", locationCategory.CHEST,[locationType.HB]),]))
        self.add_node("1000 Heartless",LocationNode([KH2Location(60, "1000 Heartless", locationCategory.ITEMBONUS,[locationType.HB]),
                                        KH2Location(525, "1000 Heartless Secret Ansem Report 1", locationCategory.POPUP,[locationType.HB]),
                                        KH2Location(269, "1000 Heartless Ice Cream", locationCategory.POPUP,[locationType.HB]),
                                        KH2Location(511, "1000 Heartless Picture", locationCategory.POPUP,[locationType.HB]),]))
        self.add_node("Gull Wing",LocationNode([KH2Location(491, "Postern Gull Wing", locationCategory.CHEST,[locationType.HB]),]))
        self.add_node("Heartless Manufactory",LocationNode([KH2Location(311, "Heartless Manufactory Cosmic Chain", locationCategory.CHEST,[locationType.HB], InvalidChecks=[itemType.MEMBERSHIPCARD]),]))
        self.add_node("Sephiroth",LocationNode([KH2Location(35, "Sephiroth Bonus", locationCategory.STATBONUS,[locationType.HB, locationType.Sephi]),
                                        KH2Location(282, "Sephiroth Fenrir", locationCategory.POPUP,[locationType.HB, locationType.Sephi]),]))
        self.add_node("Mushroom 13",LocationNode([KH2Location(588, "Winner's Proof", locationCategory.POPUP,[locationType.HB, locationType.Mush13], InvalidChecks=[itemType.PROOF_OF_PEACE]),
                                        KH2Location(589, "Proof of Peace", locationCategory.POPUP,[locationType.HB, locationType.Mush13], InvalidChecks=[itemType.PROOF_OF_PEACE]),]))
        self.add_node("Data Demyx",LocationNode([KH2Location(560, "Demyx (Data) AP Boost", locationCategory.POPUP,[locationType.HB, locationType.DataOrg], InvalidChecks=[itemType.FORM]),]))


        self.add_node("CoR Depths",LocationNode([KH2Location(562, "CoR Depths AP Boost", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                                        KH2Location(563, "CoR Depths Power Crystal", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                                        KH2Location(564, "CoR Depths Frost Crystal", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                                        KH2Location(565, "CoR Depths Manifest Illusion", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                                        KH2Location(566, "CoR Depths AP Boost (2)", locationCategory.CHEST,[locationType.HB, locationType.CoR]),]))
        self.add_node("CoR Mineshaft Pre-Fight 1",LocationNode([KH2Location(580, "CoR Mineshaft Lower Level Depths of Remembrance Map", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                                        KH2Location(578, "CoR Mineshaft Lower Level AP Boost", locationCategory.CHEST,[locationType.HB, locationType.CoR]),]))
        self.add_node("CoR-Depths Post-Fight 1",LocationNode([KH2Location(567, "CoR Depths Upper Level Remembrance Gem", locationCategory.CHEST,[locationType.HB, locationType.CoR]),]))
        self.add_node("CoR Mining Area",LocationNode([KH2Location(568, "CoR Mining Area Serenity Gem", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                                        KH2Location(569, "CoR Mining Area AP Boost", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                                        KH2Location(570, "CoR Mining Area Serenity Crystal", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                                        KH2Location(571, "CoR Mining Area Manifest Illusion", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                                        KH2Location(572, "CoR Mining Area Serenity Gem (2)", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                                        KH2Location(573, "CoR Mining Area Dark Remembrance Map", locationCategory.CHEST,[locationType.HB, locationType.CoR]),]))
        self.add_node("CoR Minshaft Pre-Fight 2",LocationNode([KH2Location(581, "CoR Mineshaft Mid Level Power Boost", locationCategory.CHEST,[locationType.HB, locationType.CoR]),]))
        self.add_node("CoR Engine Chamber",LocationNode([KH2Location(574, "CoR Engine Chamber Serenity Crystal", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                                        KH2Location(575, "CoR Engine Chamber Remembrance Crystal", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                                        KH2Location(576, "CoR Engine Chamber AP Boost", locationCategory.CHEST,[locationType.HB, locationType.CoR]),
                                        KH2Location(577, "CoR Engine Chamber Manifest Illusion", locationCategory.CHEST,[locationType.HB, locationType.CoR]),]))
        self.add_node("CoR Mineshaft Post Fight 2",LocationNode([KH2Location(582, "CoR Mineshaft Upper Level Magic Boost", locationCategory.CHEST,[locationType.HB, locationType.CoR]),]))
        self.add_node("CoR Mineshaft Last Chest",LocationNode([KH2Location(579, "CoR Mineshaft Upper Level AP Boost", locationCategory.CHEST,[locationType.HB, locationType.CoR]),]))
        self.add_node("Transport to Remembrance",LocationNode([KH2Location(72, "Transport to Remembrance", locationCategory.STATBONUS,[locationType.HB, locationType.CoR, locationType.TTR]),]))


        self.data_nodes.append("Data Demyx")

        if not self.reverse_rando:
            self.add_edge("Starting","Marketplace Map Popup",RequirementEdge())
            self.add_edge("Marketplace Map Popup","Borough",RequirementEdge())
            self.add_edge("Borough","Merlin's House Popup",RequirementEdge())
            self.add_edge("Merlin's House Popup","Bailey",RequirementEdge(battle=True))
            self.add_edge("Bailey","Baseball Charm Popup",RequirementEdge())
            self.add_edge("Baseball Charm Popup","Postern",RequirementEdge(req=ItemPlacementHelpers.hb_check))
            self.add_edge("Postern","Cooridors",RequirementEdge())
            self.add_edge("Cooridors","DTD Popup",RequirementEdge())
            self.add_edge("Cooridors","Ansem's Study",RequirementEdge())
            self.add_edge("DTD Popup","Ukulele Charm",RequirementEdge())

            self.add_edge("DTD Popup","CoR Depths",RequirementEdge(req=ItemPlacementHelpers.need_growths))
            self.add_edge("CoR Depths","CoR Mineshaft Pre-Fight 1",RequirementEdge())
            self.add_edge("CoR Mineshaft Pre-Fight 1","CoR-Depths Post-Fight 1",RequirementEdge(battle=True))
            self.add_edge("CoR-Depths Post-Fight 1","CoR Mining Area",RequirementEdge())
            self.add_edge("CoR Mining Area","CoR Minshaft Pre-Fight 2",RequirementEdge())
            self.add_edge("CoR Minshaft Pre-Fight 2","CoR Engine Chamber",RequirementEdge(battle=True))
            self.add_edge("CoR Engine Chamber","CoR Mineshaft Post Fight 2",RequirementEdge())
            self.add_edge("CoR Mineshaft Post Fight 2","CoR Mineshaft Last Chest",RequirementEdge())
            self.add_edge("CoR Mineshaft Last Chest","Transport to Remembrance",RequirementEdge(battle=True))

            self.add_edge("DTD Popup","Restoration Site",RequirementEdge(battle=True))
            self.add_edge("Restoration Site","Demyx (HB)",RequirementEdge(battle=True))
            self.add_edge("Demyx (HB)","Final Fantasy Fights",RequirementEdge(battle=True))
            self.add_edge("Final Fantasy Fights","Crystal Fissure",RequirementEdge())
            self.add_edge("Crystal Fissure","1000 Heartless",RequirementEdge(battle=True))
            self.add_edge("1000 Heartless","Gull Wing",RequirementEdge())
            self.add_edge("1000 Heartless","Heartless Manufactory",RequirementEdge())
            self.add_edge("1000 Heartless","Sephiroth",RequirementEdge(battle=True))
            self.add_edge("1000 Heartless","Mushroom 13",RequirementEdge(req=ItemPlacementHelpers.need_proof_peace))
            self.add_edge("1000 Heartless","Data Demyx",RequirementEdge(battle=True,req=ItemPlacementHelpers.need_forms))
            self.first_boss_nodes.append("Bailey")
            self.second_boss_nodes.append("1000 Heartless")
            self.data_nodes.append("Sephiroth")
        else:
            self.add_edge("Starting","Borough",RequirementEdge())
            self.add_edge("Borough","Postern",RequirementEdge())
            self.add_edge("Postern","Cooridors",RequirementEdge())
            self.add_edge("Cooridors","DTD Popup",RequirementEdge())
            self.add_edge("Cooridors","Ansem's Study",RequirementEdge())
            self.add_edge("DTD Popup","Ukulele Charm",RequirementEdge())
            self.add_edge("DTD Popup","Restoration Site",RequirementEdge(battle=True))
            self.add_edge("Restoration Site","Demyx (HB)",RequirementEdge(battle=True))
            self.add_edge("Demyx (HB)","Final Fantasy Fights",RequirementEdge(battle=True))
            self.add_edge("Final Fantasy Fights","Crystal Fissure",RequirementEdge())
            self.add_edge("Crystal Fissure","1000 Heartless",RequirementEdge(battle=True))
            self.add_edge("1000 Heartless","Gull Wing",RequirementEdge())
            self.add_edge("1000 Heartless","Heartless Manufactory",RequirementEdge())
            self.add_edge("1000 Heartless","CoR Depths",RequirementEdge(req=lambda inv : ItemPlacementHelpers.need_growths(inv) and ItemPlacementHelpers.hb_check(inv)))
            self.add_edge("CoR Depths","CoR Mineshaft Pre-Fight 1",RequirementEdge())
            self.add_edge("CoR Mineshaft Pre-Fight 1","CoR-Depths Post-Fight 1",RequirementEdge(battle=True))
            self.add_edge("CoR-Depths Post-Fight 1","CoR Mining Area",RequirementEdge())
            self.add_edge("CoR Mining Area","CoR Minshaft Pre-Fight 2",RequirementEdge())
            self.add_edge("CoR Minshaft Pre-Fight 2","CoR Engine Chamber",RequirementEdge(battle=True))
            self.add_edge("CoR Engine Chamber","CoR Mineshaft Post Fight 2",RequirementEdge())
            self.add_edge("CoR Mineshaft Post Fight 2","CoR Mineshaft Last Chest",RequirementEdge())
            self.add_edge("CoR Mineshaft Last Chest","Transport to Remembrance",RequirementEdge(battle=True))
            self.add_edge("Transport to Remembrance","Mushroom 13",RequirementEdge())
            self.add_edge("Transport to Remembrance","Sephiroth",RequirementEdge())
            self.add_edge("Sephiroth","Marketplace Map Popup",RequirementEdge())
            self.add_edge("Marketplace Map Popup","Merlin's House Popup",RequirementEdge())
            self.add_edge("Merlin's House Popup","Bailey",RequirementEdge(battle=True))
            self.add_edge("Bailey","Baseball Charm Popup",RequirementEdge())
            self.add_edge("Baseball Charm Popup","Data Demyx",RequirementEdge(battle=True,req=ItemPlacementHelpers.need_forms))
            self.first_boss_nodes.append("1000 Heartless")
            self.second_boss_nodes.append("Bailey")

    def makePLGraph(self):
        self.add_node("Gorge",LocationNode([KH2Location(492, "Gorge Savannah Map", locationCategory.CHEST,[locationType.PL]),
                                        KH2Location(404, "Gorge Dark Gem", locationCategory.CHEST,[locationType.PL]),
                                        KH2Location(405, "Gorge Mythril Stone", locationCategory.CHEST,[locationType.PL]),]))
        self.add_node("Elephant Graveyard",LocationNode([KH2Location(401, "Elephant Graveyard Frost Gem", locationCategory.CHEST,[locationType.PL]),
                                        KH2Location(402, "Elephant Graveyard Mythril Stone", locationCategory.CHEST,[locationType.PL]),
                                        KH2Location(403, "Elephant Graveyard Bright Stone", locationCategory.CHEST,[locationType.PL]),
                                        KH2Location(508, "Elephant Graveyard AP Boost", locationCategory.CHEST,[locationType.PL]),
                                        KH2Location(509, "Elephant Graveyard Mythril Shard", locationCategory.CHEST,[locationType.PL]),]))
        self.add_node("Pride Rock",LocationNode([KH2Location(418, "Pride Rock Map", locationCategory.CHEST,[locationType.PL]),
                                        KH2Location(392, "Pride Rock Mythril Stone", locationCategory.CHEST,[locationType.PL]),
                                        KH2Location(393, "Pride Rock Serenity Crystal", locationCategory.CHEST,[locationType.PL]),]))
        self.add_node("Wildebeest Valley",LocationNode([KH2Location(396, "Wildebeest Valley Energy Stone", locationCategory.CHEST,[locationType.PL]),
                                        KH2Location(397, "Wildebeest Valley AP Boost", locationCategory.CHEST,[locationType.PL]),
                                        KH2Location(398, "Wildebeest Valley Mythril Gem", locationCategory.CHEST,[locationType.PL]),
                                        KH2Location(399, "Wildebeest Valley Mythril Stone", locationCategory.CHEST,[locationType.PL]),
                                        KH2Location(400, "Wildebeest Valley Lucid Gem", locationCategory.CHEST,[locationType.PL]),]))
        self.add_node("Wastelands",LocationNode([KH2Location(406, "Wastelands Mythril Shard", locationCategory.CHEST,[locationType.PL]),
                                        KH2Location(407, "Wastelands Serenity Gem", locationCategory.CHEST,[locationType.PL]),
                                        KH2Location(408, "Wastelands Mythril Stone", locationCategory.CHEST,[locationType.PL]),]))
        self.add_node("Jungle",LocationNode([KH2Location(409, "Jungle Serenity Gem", locationCategory.CHEST,[locationType.PL]),
                                        KH2Location(410, "Jungle Mythril Stone", locationCategory.CHEST,[locationType.PL]),
                                        KH2Location(411, "Jungle Serenity Crystal", locationCategory.CHEST,[locationType.PL]),]))
        self.add_node("Oasis",LocationNode([KH2Location(412, "Oasis Map", locationCategory.CHEST,[locationType.PL]),
                                        KH2Location(493, "Oasis Torn Pages", locationCategory.CHEST,[locationType.PL]),
                                        KH2Location(413, "Oasis AP Boost", locationCategory.CHEST,[locationType.PL]),]))
        self.add_node("Circle of Life",LocationNode([KH2Location(264, "Circle of Life", locationCategory.POPUP,[locationType.PL]),]))
        self.add_node("Hyenas 1 Bonus",LocationNode([KH2Location(49, "Hyenas 1", locationCategory.STATBONUS,[locationType.PL]),]))
        self.add_node("Scar",LocationNode([KH2Location(29, "Scar", locationCategory.STATBONUS,[locationType.PL]),
                                        KH2Location(302, "Scar Fire Element", locationCategory.POPUP,[locationType.PL]),]))
        self.add_node("Hyenas 2 Bonus",LocationNode([KH2Location(50, "Hyenas 2", locationCategory.STATBONUS,[locationType.PL]),]))
        self.add_node("Groundshaker",LocationNode([KH2Location(30, "Groundshaker", locationCategory.HYBRIDBONUS,[locationType.PL]),]))
        self.add_node("Data Saix",LocationNode([KH2Location(556, "Saix (Data) Defense Boost", locationCategory.POPUP,[locationType.PL, locationType.DataOrg]),]))

        self.data_nodes.append("Data Saix")

        if not self.reverse_rando:
            self.add_edge("Starting","Gorge",RequirementEdge())
            self.add_edge("Gorge","Elephant Graveyard",RequirementEdge(battle=True))
            self.add_edge("Elephant Graveyard","Pride Rock",RequirementEdge())
            self.add_edge("Pride Rock","Wildebeest Valley",RequirementEdge())
            self.add_edge("Wildebeest Valley","Wastelands",RequirementEdge())
            self.add_edge("Wastelands","Jungle",RequirementEdge())
            self.add_edge("Jungle","Oasis",RequirementEdge())
            self.add_edge("Oasis","Circle of Life",RequirementEdge())
            self.add_edge("Circle of Life","Hyenas 1 Bonus",RequirementEdge(battle=True))
            self.add_edge("Hyenas 1 Bonus","Scar",RequirementEdge(battle=True))
            self.add_edge("Scar","Hyenas 2 Bonus",RequirementEdge(battle=True,req=ItemPlacementHelpers.simba_check))
            self.add_edge("Hyenas 2 Bonus","Groundshaker",RequirementEdge(battle=True))
            self.add_edge("Groundshaker","Data Saix",RequirementEdge(battle=True))
            self.first_boss_nodes.append("Scar")
            self.second_boss_nodes.append("Groundshaker")
        else:
            self.add_edge("Starting","Pride Rock",RequirementEdge())
            self.add_edge("Pride Rock","Elephant Graveyard",RequirementEdge())
            self.add_edge("Elephant Graveyard","Hyenas 2 Bonus",RequirementEdge(battle=True))
            self.add_edge("Hyenas 2 Bonus","Wildebeest Valley",RequirementEdge())
            self.add_edge("Wildebeest Valley","Wastelands",RequirementEdge())
            self.add_edge("Wastelands","Jungle",RequirementEdge())
            self.add_edge("Jungle","Groundshaker",RequirementEdge(battle=True))
            self.add_edge("Groundshaker","Gorge",RequirementEdge(req=ItemPlacementHelpers.simba_check))
            self.add_edge("Gorge","Oasis",RequirementEdge(battle=True))
            self.add_edge("Oasis","Circle of Life",RequirementEdge())
            self.add_edge("Circle of Life","Hyenas 1 Bonus",RequirementEdge(battle=True))
            self.add_edge("Hyenas 1 Bonus","Scar",RequirementEdge(battle=True))
            self.add_edge("Scar","Data Saix",RequirementEdge(battle=True))
            self.first_boss_nodes.append("Groundshaker")
            self.second_boss_nodes.append("Scar")

    def makeSTTGraph(self):
        self.add_node("Twilight Town Map Popup",LocationNode([KH2Location(319, "Twilight Town Map", locationCategory.POPUP,[locationType.STT]),]))
        self.add_node("Munny Pouch Popup",LocationNode([KH2Location(288, "Munny Pouch (Olette)", locationCategory.POPUP,[locationType.STT]),]))
        self.add_node("Roxas Station",LocationNode([KH2Location(54, "Station Dusks", locationCategory.ITEMBONUS,[locationType.STT]),
                                        KH2Location(315, "Station of Serenity Potion", locationCategory.CHEST,[locationType.STT]),
                                        KH2Location(472, "Station of Calling Potion", locationCategory.CHEST,[locationType.STT]),]))
        self.add_node("Twilight Thorn",LocationNode([KH2Location(33, "Twilight Thorn", locationCategory.ITEMBONUS,[locationType.STT]),]))
        self.add_node("Axel 1",LocationNode([KH2Location(73, "Axel 1", locationCategory.ITEMBONUS,[locationType.STT]),]))
        self.add_node("Struggle Champion",LocationNode([KH2Location(389, "(Junk) Champion Belt", locationCategory.CHEST,[locationType.STT], InvalidChecks=[e for e in itemType if e not in [itemType.SYNTH,itemType.ITEM] ]),
                                        KH2Location(390, "(Junk) Medal", locationCategory.CHEST,[locationType.STT], InvalidChecks=[e for e in itemType if e not in [itemType.SYNTH,itemType.ITEM] ]),
                                        KH2Location(519, "The Struggle Trophy", locationCategory.POPUP,[locationType.STT]),]))
        self.add_node("STT Central Station",LocationNode([KH2Location(428, "Central Station Potion (1)", locationCategory.CHEST,[locationType.STT]),
                                        KH2Location(429, "STT Central Station Hi-Potion", locationCategory.CHEST,[locationType.STT]),
                                        KH2Location(430, "Central Station Potion (2)", locationCategory.CHEST,[locationType.STT]),]))
        self.add_node("STT Sunset Terrace",LocationNode([KH2Location(434, "Sunset Terrace Ability Ring", locationCategory.CHEST,[locationType.STT]),
                                        KH2Location(435, "Sunset Terrace Hi-Potion", locationCategory.CHEST,[locationType.STT]),
                                        KH2Location(436, "Sunset Terrace Potion (1)", locationCategory.CHEST,[locationType.STT]),
                                        KH2Location(437, "Sunset Terrace Potion (2)", locationCategory.CHEST,[locationType.STT]),]))
        self.add_node("STT Mansion Foyer",LocationNode([KH2Location(449, "Mansion Foyer Hi-Potion", locationCategory.CHEST,[locationType.STT]),
                                        KH2Location(450, "Mansion Foyer Potion (1)", locationCategory.CHEST,[locationType.STT]),
                                        KH2Location(451, "Mansion Foyer Potion (2)", locationCategory.CHEST,[locationType.STT]),]))
        self.add_node("STT Mansion Dining Room",LocationNode([KH2Location(455, "Mansion Dining Room Elven Bandanna", locationCategory.CHEST,[locationType.STT]),
                                        KH2Location(456, "Mansion Dining Room Potion", locationCategory.CHEST,[locationType.STT]),]))
        self.add_node("Namine's Room",LocationNode([KH2Location(289, "Naminé´s Sketches", locationCategory.POPUP,[locationType.STT]),
                                        KH2Location(483, "Mansion Map", locationCategory.POPUP,[locationType.STT]),]))
        self.add_node("STT Mansion Library",LocationNode([KH2Location(459, "Mansion Library Hi-Potion", locationCategory.CHEST,[locationType.STT]),]))
        self.add_node("Axel 2",LocationNode([KH2Location(34, "Axel 2", locationCategory.STATBONUS,[locationType.STT]),]))
        self.add_node("STT Mansion Basement",LocationNode([KH2Location(463, "Mansion Basement Corridor Hi-Potion", locationCategory.CHEST,[locationType.STT]),]))
        self.add_node("Data Roxas",LocationNode([KH2Location(558, "Roxas (Data) Magic Boost", locationCategory.POPUP,[locationType.STT, locationType.DataOrg]),]))

        self.data_nodes.append("Data Roxas")

        if not self.reverse_rando:
            self.add_edge("Starting","Twilight Town Map Popup",RequirementEdge())
            self.add_edge("Twilight Town Map Popup","Munny Pouch Popup",RequirementEdge())
            self.add_edge("Munny Pouch Popup","Roxas Station",RequirementEdge())
            self.add_edge("Roxas Station","Twilight Thorn",RequirementEdge(battle=True))
            self.add_edge("Twilight Thorn","Axel 1",RequirementEdge(battle=True))
            self.add_edge("Axel 1","Struggle Champion",RequirementEdge(battle=True))
            self.add_edge("Struggle Champion","STT Central Station",RequirementEdge())
            self.add_edge("Struggle Champion","STT Sunset Terrace",RequirementEdge())
            self.add_edge("STT Sunset Terrace","STT Mansion Foyer",RequirementEdge(battle=True))
            self.add_edge("STT Mansion Foyer","STT Mansion Dining Room",RequirementEdge())
            self.add_edge("STT Mansion Foyer","Namine's Room",RequirementEdge())
            self.add_edge("Namine's Room","STT Mansion Library",RequirementEdge())
            self.add_edge("Namine's Room","Axel 2",RequirementEdge(battle=True))
            self.add_edge("Axel 2","STT Mansion Basement",RequirementEdge())
            self.add_edge("STT Mansion Basement","Data Roxas",RequirementEdge(battle=True))
            self.first_boss_nodes.append("STT Mansion Basement")
            self.second_boss_nodes.append("STT Mansion Basement")
        else:
            self.add_edge("Starting","STT Mansion Foyer",RequirementEdge())
            self.add_edge("STT Mansion Foyer","STT Mansion Dining Room",RequirementEdge())
            self.add_edge("STT Mansion Foyer","Namine's Room",RequirementEdge())
            self.add_edge("Namine's Room","STT Mansion Library",RequirementEdge())
            self.add_edge("Namine's Room","Axel 2",RequirementEdge(battle=True))
            self.add_edge("Axel 2","STT Mansion Basement",RequirementEdge())
            self.add_edge("STT Mansion Basement","STT Central Station",RequirementEdge())
            self.add_edge("STT Mansion Basement","STT Sunset Terrace",RequirementEdge())
            self.add_edge("STT Sunset Terrace","Axel 1",RequirementEdge(battle=True))
            self.add_edge("Axel 1","Struggle Champion",RequirementEdge(battle=True))
            self.add_edge("Struggle Champion","Roxas Station",RequirementEdge())
            self.add_edge("Roxas Station","Twilight Thorn",RequirementEdge(battle=True))
            self.add_edge("Twilight Thorn","Twilight Town Map Popup",RequirementEdge(battle=True))
            self.add_edge("Twilight Town Map Popup","Munny Pouch Popup",RequirementEdge())
            self.add_edge("Munny Pouch Popup","Data Roxas",RequirementEdge(battle=True))
            self.first_boss_nodes.append("Munny Pouch Popup")
            self.second_boss_nodes.append("Munny Pouch Popup")

    
    def makeTTGraph(self):
        self.add_node("Old Mansion",LocationNode([KH2Location(447, "Old Mansion Potion", locationCategory.CHEST,[locationType.TT]),
                                        KH2Location(448, "Old Mansion Mythril Shard", locationCategory.CHEST,[locationType.TT]),]))
        self.add_node("Woods",LocationNode([KH2Location(442, "The Woods Potion", locationCategory.CHEST,[locationType.TT]),
                                        KH2Location(443, "The Woods Mythril Shard", locationCategory.CHEST,[locationType.TT]),
                                        KH2Location(444, "The Woods Hi-Potion", locationCategory.CHEST,[locationType.TT]),]))
        self.add_node("Tram Common",LocationNode([KH2Location(420, "Tram Common Hi-Potion", locationCategory.CHEST,[locationType.TT]),
                                        KH2Location(421, "Tram Common AP Boost", locationCategory.CHEST,[locationType.TT]),
                                        KH2Location(422, "Tram Common Tent", locationCategory.CHEST,[locationType.TT]),
                                        KH2Location(423, "Tram Common Mythril Shard (1)", locationCategory.CHEST,[locationType.TT]),
                                        KH2Location(424, "Tram Common Potion (1)", locationCategory.CHEST,[locationType.TT]),
                                        KH2Location(425, "Tram Common Mythril Shard (2)", locationCategory.CHEST,[locationType.TT]),
                                        KH2Location(484, "Tram Common Potion (2)", locationCategory.CHEST,[locationType.TT]),]))
        self.add_node("Station Fight Popup",LocationNode([KH2Location(526, "Station Plaza Secret Ansem Report 2", locationCategory.POPUP,[locationType.TT]),
                                        KH2Location(290, "Munny Pouch (Mickey)", locationCategory.POPUP,[locationType.TT]),
                                        KH2Location(291, "Crystal Orb", locationCategory.POPUP,[locationType.TT]),]))
        self.add_node("TT Central Station",LocationNode([KH2Location(431, "Central Station Tent", locationCategory.CHEST,[locationType.TT]),
                                        KH2Location(432, "TT Central Station Hi-Potion", locationCategory.CHEST,[locationType.TT]),
                                        KH2Location(433, "Central Station Mythril Shard", locationCategory.CHEST,[locationType.TT]),]))
        self.add_node("Yensid Tower",LocationNode([KH2Location(465, "The Tower Potion", locationCategory.CHEST,[locationType.TT]),
                                        KH2Location(466, "The Tower Hi-Potion", locationCategory.CHEST,[locationType.TT]),
                                        KH2Location(522, "The Tower Ether", locationCategory.CHEST,[locationType.TT]),]))
        self.add_node("Yensid Tower Entryway",LocationNode([KH2Location(467, "Tower Entryway Ether", locationCategory.CHEST,[locationType.TT]),
                                        KH2Location(468, "Tower Entryway Mythril Shard", locationCategory.CHEST,[locationType.TT]),]))
        self.add_node("Sorcerer's Loft",LocationNode([KH2Location(469, "Sorcerer's Loft Tower Map", locationCategory.CHEST,[locationType.TT]),]))
        self.add_node("Tower Wardrobe",LocationNode([KH2Location(470, "Tower Wardrobe Mythril Stone", locationCategory.CHEST,[locationType.TT]),]))
        self.add_node("Valor Form",LocationNode([KH2Location(304, "Star Seeker", locationCategory.POPUP,[locationType.TT]),
                                        KH2Location(286, "Valor Form", locationCategory.POPUP,[locationType.TT]),]))
        self.add_node("Seifer's Trophy",LocationNode([KH2Location(294, "Seifer´s Trophy", locationCategory.POPUP,[locationType.TT]),]))
        self.add_node("Limit Form",LocationNode([KH2Location(265, "Oathkeeper", locationCategory.POPUP,[locationType.TT]),
                                        KH2Location(543, "Limit Form", locationCategory.POPUP,[locationType.TT]),]))
        self.add_node("Underground Concourse",LocationNode([KH2Location(479, "Underground Concourse Mythril Gem", locationCategory.CHEST,[locationType.TT]),
                                        KH2Location(480, "Underground Concourse Orichalcum", locationCategory.CHEST,[locationType.TT]),
                                        KH2Location(481, "Underground Concourse AP Boost", locationCategory.CHEST,[locationType.TT]),
                                        KH2Location(482, "Underground Concourse Mythril Crystal", locationCategory.CHEST,[locationType.TT]),]))
        self.add_node("Tunnelway",LocationNode([KH2Location(477, "Tunnelway Orichalcum", locationCategory.CHEST,[locationType.TT]),
                                        KH2Location(478, "Tunnelway Mythril Crystal", locationCategory.CHEST,[locationType.TT]),]))
        self.add_node("TT Sunset Terrace",LocationNode([KH2Location(438, "Sunset Terrace Orichalcum+", locationCategory.CHEST,[locationType.TT]),
                                        KH2Location(439, "Sunset Terrace Mythril Shard", locationCategory.CHEST,[locationType.TT]),
                                        KH2Location(440, "Sunset Terrace Mythril Crystal", locationCategory.CHEST,[locationType.TT]),
                                        KH2Location(441, "Sunset Terrace AP Boost", locationCategory.CHEST,[locationType.TT]),]))
        self.add_node("TT Mansion Bonus",LocationNode([KH2Location(56, "Mansion Nobodies", locationCategory.STATBONUS,[locationType.TT]),]))
        self.add_node("TT Mansion Foyer",LocationNode([KH2Location(452, "Mansion Foyer Mythril Crystal", locationCategory.CHEST,[locationType.TT]),
                                        KH2Location(453, "Mansion Foyer Mythril Stone", locationCategory.CHEST,[locationType.TT]),
                                        KH2Location(454, "Mansion Foyer Serenity Crystal", locationCategory.CHEST,[locationType.TT]),]))
        self.add_node("TT Mansion Dining Room",LocationNode([KH2Location(457, "Mansion Dining Room Mythril Crystal", locationCategory.CHEST,[locationType.TT]),
                                        KH2Location(458, "Mansion Dining Room Mythril Stone", locationCategory.CHEST,[locationType.TT]),]))
        self.add_node("TT Mansion Library",LocationNode([KH2Location(460, "Mansion Library Orichalcum", locationCategory.CHEST,[locationType.TT]),]))
        self.add_node("TT Beam",LocationNode([KH2Location(534, "Beam Secret Ansem Report 10", locationCategory.POPUP,[locationType.TT]),]))
        self.add_node("TT Mansion Basement",LocationNode([KH2Location(464, "Mansion Basement Corridor Ultimate Recipe", locationCategory.CHEST,[locationType.TT]),]))
        self.add_node("Betwixt and Between",LocationNode([KH2Location(63, "Betwixt and Between", locationCategory.ITEMBONUS,[locationType.TT]),
                                        KH2Location(317, "Betwixt and Between Bond of Flame", locationCategory.POPUP,[locationType.TT]),]))
        self.add_node("Data Axel",LocationNode([KH2Location(561, "Axel (Data) Magic Boost", locationCategory.POPUP,[locationType.TT, locationType.DataOrg]),]))

        self.data_nodes.append("Data Axel")

        if not self.reverse_rando:
            self.add_edge("Starting","Old Mansion",RequirementEdge())
            self.add_edge("Old Mansion","Tram Common",RequirementEdge())
            self.add_edge("Tram Common","Woods",RequirementEdge())
            self.add_edge("Tram Common","Station Fight Popup",RequirementEdge(battle=True))
            self.add_edge("Station Fight Popup","TT Central Station",RequirementEdge())
            self.add_edge("TT Central Station","Yensid Tower",RequirementEdge())
            self.add_edge("Yensid Tower","Yensid Tower Entryway",RequirementEdge())
            self.add_edge("Yensid Tower Entryway","Sorcerer's Loft",RequirementEdge(battle=True))
            self.add_edge("Sorcerer's Loft","Tower Wardrobe",RequirementEdge())
            self.add_edge("Tower Wardrobe","Valor Form",RequirementEdge())
            self.add_edge("Valor Form","Seifer's Trophy",RequirementEdge(battle=True,req=ItemPlacementHelpers.tt2_check))
            self.add_edge("Seifer's Trophy","Limit Form",RequirementEdge())
            self.add_edge("Limit Form","Underground Concourse",RequirementEdge(req=ItemPlacementHelpers.tt3_check))
            self.add_edge("Underground Concourse","Tunnelway",RequirementEdge())
            self.add_edge("Tunnelway","TT Sunset Terrace",RequirementEdge())
            self.add_edge("Limit Form","TT Mansion Bonus",RequirementEdge(battle=True))
            self.add_edge("TT Mansion Bonus","TT Mansion Foyer",RequirementEdge())
            self.add_edge("TT Mansion Foyer","TT Mansion Dining Room",RequirementEdge())
            self.add_edge("TT Mansion Foyer","TT Mansion Library",RequirementEdge())
            self.add_edge("TT Mansion Foyer","TT Beam",RequirementEdge())
            self.add_edge("TT Mansion Foyer","TT Mansion Basement",RequirementEdge())
            self.add_edge("TT Beam","Betwixt and Between",RequirementEdge(battle=True))
            self.add_edge("Betwixt and Between","Data Axel",RequirementEdge(battle=True))
            self.first_boss_nodes.append("Valor Form")
            self.second_boss_nodes.append("Betwixt and Between")
        else:
            self.add_edge("Starting","TT Central Station",RequirementEdge())
            self.add_edge("TT Central Station","Underground Concourse",RequirementEdge())
            self.add_edge("TT Central Station","Tram Common",RequirementEdge())
            self.add_edge("Tram Common","Woods",RequirementEdge())
            self.add_edge("Underground Concourse","Tunnelway",RequirementEdge())
            self.add_edge("Tunnelway","TT Sunset Terrace",RequirementEdge())
            self.add_edge("Woods","TT Mansion Bonus",RequirementEdge(battle=True))
            self.add_edge("TT Mansion Bonus","Old Mansion",RequirementEdge())
            self.add_edge("TT Mansion Bonus","TT Mansion Foyer",RequirementEdge())
            self.add_edge("TT Mansion Foyer","TT Mansion Dining Room",RequirementEdge())
            self.add_edge("TT Mansion Foyer","TT Mansion Library",RequirementEdge())
            self.add_edge("TT Mansion Foyer","TT Beam",RequirementEdge())
            self.add_edge("TT Mansion Foyer","TT Mansion Basement",RequirementEdge())
            self.add_edge("TT Beam","Betwixt and Between",RequirementEdge(battle=True))
            self.add_edge("Betwixt and Between","Seifer's Trophy",RequirementEdge(battle=True,req=ItemPlacementHelpers.tt2_check))
            self.add_edge("Seifer's Trophy","Limit Form",RequirementEdge())
            self.add_edge("Limit Form","Station Fight Popup",RequirementEdge(battle=True,req=ItemPlacementHelpers.tt3_check))
            self.add_edge("Station Fight Popup","Yensid Tower",RequirementEdge())
            self.add_edge("Yensid Tower","Yensid Tower Entryway",RequirementEdge())
            self.add_edge("Yensid Tower Entryway","Sorcerer's Loft",RequirementEdge(battle=True))
            self.add_edge("Sorcerer's Loft","Tower Wardrobe",RequirementEdge())
            self.add_edge("Tower Wardrobe","Valor Form",RequirementEdge())
            self.add_edge("Valor Form","Data Axel",RequirementEdge(battle=True))
            self.first_boss_nodes.append("Betwixt and Between")
            self.second_boss_nodes.append("Valor Form")


    def makeTWTNWGraph(self):
        self.add_node("Fragment Crossing",LocationNode([KH2Location(374, "Fragment Crossing Mythril Stone", locationCategory.CHEST,[locationType.TWTNW]),
                                            KH2Location(375, "Fragment Crossing Mythril Crystal", locationCategory.CHEST,[locationType.TWTNW]),
                                            KH2Location(376, "Fragment Crossing AP Boost", locationCategory.CHEST,[locationType.TWTNW]),
                                            KH2Location(377, "Fragment Crossing Orichalcum", locationCategory.CHEST,[locationType.TWTNW]),]))
        self.add_node("Roxas",LocationNode([KH2Location(69, "Roxas", locationCategory.HYBRIDBONUS,[locationType.TWTNW]),
                                            KH2Location(532, "Roxas Secret Ansem Report 8", locationCategory.POPUP,[locationType.TWTNW]),
                                            KH2Location(277, "Two Become One", locationCategory.POPUP,[locationType.TWTNW]),]))
        self.add_node("Memory's Skyscraper",LocationNode([KH2Location(391, "Memory's Skyscaper Mythril Crystal", locationCategory.CHEST,[locationType.TWTNW]),
                                            KH2Location(523, "Memory's Skyscaper AP Boost", locationCategory.CHEST,[locationType.TWTNW]),
                                            KH2Location(524, "Memory's Skyscaper Mythril Stone", locationCategory.CHEST,[locationType.TWTNW]),]))
        self.add_node("Brink of Despair",LocationNode([KH2Location(335, "The Brink of Despair Dark City Map", locationCategory.CHEST,[locationType.TWTNW]),
                                            KH2Location(500, "The Brink of Despair Orichalcum+", locationCategory.CHEST,[locationType.TWTNW]),]))
        self.add_node("Nothing's Call",LocationNode([KH2Location(378, "Nothing's Call Mythril Gem", locationCategory.CHEST,[locationType.TWTNW]),
                                            KH2Location(379, "Nothing's Call Orichalcum", locationCategory.CHEST,[locationType.TWTNW]),]))
        self.add_node("Twilight's View",LocationNode([KH2Location(336, "Twilight's View Cosmic Belt", locationCategory.CHEST,[locationType.TWTNW]),]))
        self.add_node("Xigbar",LocationNode([KH2Location(23, "Xigbar Bonus", locationCategory.STATBONUS,[locationType.TWTNW]),
                                              KH2Location(527, "Xigbar Secret Ansem Report 3", locationCategory.POPUP,[locationType.TWTNW]),]))
        self.add_node("Naught's Skyway",LocationNode([KH2Location(380, "Naught's Skyway Mythril Gem", locationCategory.CHEST,[locationType.TWTNW]),
                                            KH2Location(381, "Naught's Skyway Orichalcum", locationCategory.CHEST,[locationType.TWTNW]),
                                            KH2Location(382, "Naught's Skyway Mythril Crystal", locationCategory.CHEST,[locationType.TWTNW]),]))
        self.add_node("Oblivion",LocationNode([KH2Location(278, "Oblivion", locationCategory.POPUP,[locationType.TWTNW]),
                                            KH2Location(496, "Castle That Never Was Map", locationCategory.POPUP,[locationType.TWTNW]),]))
        self.add_node("Luxord",LocationNode([KH2Location(24, "Luxord Bonus", locationCategory.HYBRIDBONUS,[locationType.TWTNW]),
                                               KH2Location(533, "Luxord Secret Ansem Report 9", locationCategory.POPUP,[locationType.TWTNW]),]))
        self.add_node("Saix",LocationNode([KH2Location(25, "Saix Bonus", locationCategory.STATBONUS,[locationType.TWTNW]),
                                               KH2Location(536, "Saix Secret Ansem Report 12", locationCategory.POPUP,[locationType.TWTNW]),]))
        self.add_node("Pre-Xemnas 1 Popup",LocationNode([KH2Location(535, "(Pre-Xemnas 1) Secret Ansem Report 11", locationCategory.POPUP,[locationType.TWTNW]),]))
        self.add_node("Ruin and Creation's Passage",LocationNode([KH2Location(385, "Ruin and Creation's Passage Mythril Stone", locationCategory.CHEST,[locationType.TWTNW]),
                                            KH2Location(386, "Ruin and Creation's Passage AP Boost", locationCategory.CHEST,[locationType.TWTNW]),
                                            KH2Location(387, "Ruin and Creation's Passage Mythril Crystal", locationCategory.CHEST,[locationType.TWTNW]),
                                            KH2Location(388, "Ruin and Creation's Passage Orichalcum", locationCategory.CHEST,[locationType.TWTNW]),]))
        self.add_node("Xemnas 1",LocationNode([KH2Location(26, "Xemnas 1 Bonus", locationCategory.DOUBLEBONUS, [locationType.TWTNW]),
                                              KH2Location(537, "Xemnas 1 Secret Ansem Report 13", locationCategory.POPUP,[locationType.TWTNW]),]))
        self.add_node("Final Xemnas",LocationNode([KH2Location(71, "Final Xemnas", locationCategory.STATBONUS,[locationType.TWTNW],InvalidChecks=[e for e in itemType if e not in [itemType.GAUGE, itemType.SLOT, itemType.SYNTH,itemType.ITEM]]),]))
        self.add_node("Data Xemnas",LocationNode([KH2Location(554, "Xemnas (Data) Power Boost", locationCategory.POPUP,[locationType.TWTNW, locationType.DataOrg]),]))

        self.data_nodes.append("Data Xemnas")

        if not self.reverse_rando:
            self.add_edge("Starting","Fragment Crossing",RequirementEdge())
            self.add_edge("Fragment Crossing","Roxas",RequirementEdge(battle=True))
            self.add_edge("Roxas","Memory's Skyscraper",RequirementEdge())
            self.add_edge("Memory's Skyscraper","Brink of Despair",RequirementEdge())
            self.add_edge("Brink of Despair","Nothing's Call",RequirementEdge())
            self.add_edge("Nothing's Call","Twilight's View",RequirementEdge())
            self.add_edge("Twilight's View","Xigbar",RequirementEdge(battle=True))
            self.add_edge("Xigbar","Naught's Skyway",RequirementEdge())
            self.add_edge("Naught's Skyway","Oblivion",RequirementEdge())
            self.add_edge("Oblivion","Luxord",RequirementEdge(battle=True))
            self.add_edge("Luxord","Saix",RequirementEdge(battle=True))
            self.add_edge("Saix","Pre-Xemnas 1 Popup",RequirementEdge())
            self.add_edge("Pre-Xemnas 1 Popup","Ruin and Creation's Passage",RequirementEdge())
            self.add_edge("Ruin and Creation's Passage","Xemnas 1",RequirementEdge(battle=True))
            self.add_edge("Xemnas 1","Final Xemnas",RequirementEdge(battle=True))
            self.add_edge("Xemnas 1","Data Xemnas",RequirementEdge(battle=True))
            self.first_boss_nodes.append("Xemnas 1")
            self.second_boss_nodes.append("Xemnas 1")
        else:
            self.add_edge("Starting","Fragment Crossing",RequirementEdge())
            self.add_edge("Fragment Crossing","Xemnas 1",RequirementEdge(battle=True))
            self.add_edge("Xemnas 1","Memory's Skyscraper",RequirementEdge())
            self.add_edge("Memory's Skyscraper","Brink of Despair",RequirementEdge())
            self.add_edge("Brink of Despair","Nothing's Call",RequirementEdge())
            self.add_edge("Nothing's Call","Twilight's View",RequirementEdge())
            self.add_edge("Twilight's View","Saix",RequirementEdge(battle=True))
            self.add_edge("Saix","Naught's Skyway",RequirementEdge())
            self.add_edge("Naught's Skyway","Oblivion",RequirementEdge())
            self.add_edge("Oblivion","Luxord",RequirementEdge(battle=True))
            self.add_edge("Luxord","Xigbar",RequirementEdge(battle=True))
            self.add_edge("Xigbar","Pre-Xemnas 1 Popup",RequirementEdge())
            self.add_edge("Pre-Xemnas 1 Popup","Ruin and Creation's Passage",RequirementEdge())
            self.add_edge("Ruin and Creation's Passage","Roxas",RequirementEdge(battle=True))
            self.add_edge("Roxas","Final Xemnas",RequirementEdge(battle=True))
            self.add_edge("Roxas","Data Xemnas",RequirementEdge(battle=True))
            self.first_boss_nodes.append("Roxas")
            self.second_boss_nodes.append("Roxas")



    def makeATLGraph(self):
        self.add_node("Atlantica Tutorial",LocationNode([KH2Location(367, "Undersea Kingdom Map", locationCategory.POPUP,[locationType.Atlantica]),]))
        self.add_node("Ursula",LocationNode([KH2Location(287, "Mysterious Abyss", locationCategory.POPUP,[locationType.Atlantica]),]))
        self.add_node("New Day is Dawning",LocationNode([KH2Location(279, "Musical Blizzard Element", locationCategory.POPUP,[locationType.Atlantica]),
                                        KH2Location(538, "Musical Orichalcum+", locationCategory.POPUP,[locationType.Atlantica]),]))

        if not self.reverse_rando:
            self.add_edge("Starting","Atlantica Tutorial",RequirementEdge())
            self.add_edge("Atlantica Tutorial","Ursula",RequirementEdge(req=ItemPlacementHelpers.need_2_magnet))
            self.add_edge("Ursula","New Day is Dawning",RequirementEdge(req=lambda inv : ItemPlacementHelpers.need_2_magnet(inv) and ItemPlacementHelpers.need_3_thunders(inv)))
        else:
            self.add_edge("Starting","New Day is Dawning",RequirementEdge())
            self.add_edge("New Day is Dawning","Ursula",RequirementEdge(req=ItemPlacementHelpers.need_1_magnet))
            self.add_edge("Ursula","Atlantica Tutorial",RequirementEdge(req=lambda inv : ItemPlacementHelpers.need_2_magnet(inv) and ItemPlacementHelpers.need_3_thunders(inv)))


    @staticmethod
    def WeaponList():
        return [KH2Location(116,"Kingdom Key D (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(83,"Alpha Weapon (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(84,"Omega Weapon (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(80,"Kingdom Key (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(81,"Oathkeeper (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(82,"Oblivion (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(123,"Star Seeker (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(124,"Hidden Dragon (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(127,"Hero's Crest (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(128,"Monochrome (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(129,"Follow the Wind (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(130,"Circle of Life (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(131,"Photon Debugger (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(132,"Gull Wing (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(133,"Rumbling Rose (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(134,"Guardian Soul (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(135,"Wishing Lamp (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(136,"Decisive Pumpkin (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(138,"Sweet Memories (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(139,"Mysterious Abyss (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(137,"Sleeping Lion (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(141,"Bond of Flame (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(148,"Two Become One (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(140,"Fatal Crest (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(142,"Fenrir (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(143,"Ultima Weapon (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(149,"Winner's Proof (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(85,"Pureblood (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot])]

    @staticmethod
    def getStruggleWeapons():
        return  [KH2Location(122,"Struggle Sword (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                    KH2Location(144,"Struggle Wand (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                    KH2Location(145,"Struggle Hammer (Slot)",locationCategory.WEAPONSLOT,[locationType.WeaponSlot])]
    @staticmethod
    def DonaldBonusList():
        return [
            KH2Location(42,"Abu Escort", locationCategory.ITEMBONUS, LocationTypes=[locationType.Agrabah]),
            KH2Location(45,"Screens", locationCategory.ITEMBONUS, LocationTypes=[locationType.SP]),
            KH2Location(28,"Demyx (Hollow Bastion)", locationCategory.ITEMBONUS, LocationTypes=[locationType.HB]),
            KH2Location(58,"Demyx (Olympus)", locationCategory.ITEMBONUS, LocationTypes=[locationType.OC]),
            KH2Location(22,"Grim Reaper 2", locationCategory.ITEMBONUS, LocationTypes=[locationType.PR]),
            KH2Location(16,"Boat Pete", locationCategory.DOUBLEBONUS, LocationTypes=[locationType.DC]),
            KH2Location(18,"Prison Keeper", locationCategory.ITEMBONUS, LocationTypes=[locationType.HT]),
            KH2Location(29,"Scar", locationCategory.ITEMBONUS, LocationTypes=[locationType.PL]),
            KH2Location(61,"Solar Sailor", locationCategory.ITEMBONUS, LocationTypes=[locationType.SP]),
            KH2Location(20,"Experiment", locationCategory.ITEMBONUS, LocationTypes=[locationType.HT]),
            KH2Location(62,"Boat Fight", locationCategory.ITEMBONUS, LocationTypes=[locationType.PR]),
            KH2Location(56,"Mansion", locationCategory.ITEMBONUS, LocationTypes=[locationType.TT]),
            KH2Location(2, "Posessor",locationCategory.ITEMBONUS, LocationTypes=[locationType.BC]),
            KH2Location(4, "Xaldin",locationCategory.ITEMBONUS, LocationTypes=[locationType.BC]),
        ]

    @staticmethod
    def DonaldWeaponList():
        return [KH2Location(151,"Centurion+",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(90,"Comet Staff",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(87,"Hammer Staff",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(91,"Lord's Broom",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(86,"Mage's Staff",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(89,"Meteor Staff",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(94,"Nobody Lance",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(154,"Precious Mushroom",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(155,"Precious Mushroom+",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(156,"Premium Mushroom",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(93,"Rising Dragon",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(146,"Save the Queen+",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(95,"Shaman's Relic",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(88,"Victory Bell",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
                KH2Location(92,"Wisdom Wand",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            ]

    @staticmethod
    def DonaldStartingItems():
        return [KH2Location(i, f"Donald Starting Item {i}", locationCategory.CHEST, [locationType.Free]) for i in range(1,3)]


    @staticmethod
    def GoofyBonusList():
        return [KH2Location(21,"Barbossa",locationCategory.DOUBLEBONUS, [locationType.PR]),
                KH2Location(59,"Grim Reaper 1",locationCategory.ITEMBONUS, [locationType.PR]),
                KH2Location(31,"Hostile Program",locationCategory.ITEMBONUS, [locationType.SP]),
                KH2Location(49,"Hyenas 1",locationCategory.ITEMBONUS, [locationType.PL]),
                KH2Location(50,"Hyenas 2",locationCategory.ITEMBONUS, [locationType.PL]),
                KH2Location(40,"Lock/Shock/Barrel",locationCategory.ITEMBONUS, [locationType.HT]),
                KH2Location(19, "Oogie Boogie", locationCategory.ITEMBONUS, [locationType.HT]),
                KH2Location(6,"Pete (Olympus)",locationCategory.ITEMBONUS, [locationType.OC]),
                KH2Location(17,"Pete (Wharf)",locationCategory.ITEMBONUS, [locationType.DC]),
                KH2Location(9,"Shan-Yu",locationCategory.ITEMBONUS, [locationType.LoD]),
                KH2Location(10,"Storm Rider", locationCategory.ITEMBONUS, [locationType.LoD]),
                KH2Location(12,"Beast",locationCategory.ITEMBONUS, [locationType.BC]),
                KH2Location(39,"Interceptor Barrels",locationCategory.ITEMBONUS, [locationType.PR]),
                KH2Location(46,"Treasure Room Heartless",locationCategory.ITEMBONUS, [locationType.Agrabah]),
                KH2Location(66,"Zexion",locationCategory.ITEMBONUS, [locationType.OC, locationType.AS]),
                ]

    @staticmethod
    def GoofyWeaponList():
        return [
            KH2Location(100,"Adamant Shield",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(107,"Akashic Record",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(101,"Chain Gear",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(104,"Dream Cloud",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(103,"Falling Star",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(158,"Frozen Pride+",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(106,"Genji Shield",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(105,"Knight Defender",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(99,"Knight's Shield",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(161,"Majestic Mushroom",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(162,"Majestic Mushroom+",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(108,"Nobody Guard",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(102,"Ogre Shield",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(147,"Save The King+",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
            KH2Location(163,"Ultimate Mushroom",locationCategory.WEAPONSLOT,[locationType.WeaponSlot]),
        ]

    @staticmethod
    def GoofyStartingItems():
        return [KH2Location(i, f"Goofy Starting Item {i}", locationCategory.CHEST, [locationType.Free]) for i in range(1,3)]
