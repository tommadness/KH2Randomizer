from dataclasses import dataclass

@dataclass (frozen=True)
class KH2Chest:
    LocationId: int
    ChestIndex: int
    SpawnName: str

    @staticmethod
    def getChestList():
        return [
            #Agrabah
            KH2Chest(28, 0, "al00/m_70"),
            KH2Chest(29, 1, "al00/m_70"),
            KH2Chest(30, 2, "al00/m_70"),
            KH2Chest(132, 3, "al00/m_70"),
            KH2Chest(133, 4, "al00/m_70"),
            KH2Chest(249, 5, "al00/m_70"),
            KH2Chest(501, 6, "al00/m_70"),
            #Bazaar
            KH2Chest(31, 0, "al01/m_70"),
            KH2Chest(32, 1, "al01/m_70"),
            KH2Chest(33, 2, "al01/m_70"),
            KH2Chest(134, 3, "al01/m_70"),
            KH2Chest(135, 4, "al01/m_70"),
            #Palace Walls
            KH2Chest(136, 0, "al06/m_70"),
            KH2Chest(520, 1, "al06/m_70"),
            #Cave of Wonders Entrance
            KH2Chest(250, 0, "al07/m_70"),
            KH2Chest(251, 1, "al07/m_70"),
            #Treasure Room
            KH2Chest(502, 0, "al10/m_70"),
            KH2Chest(503, 1, "al10/m_70"),
            #Ruined Chamber
            KH2Chest(34, 0, "al11/m_70"),
            KH2Chest(486, 1, "al11/m_70"),
            #Valley of Stone
            KH2Chest(35, 0, "al12/m_70"),
            KH2Chest(36, 1, "al12/m_70"),
            KH2Chest(137, 2, "al12/m_70"),
            KH2Chest(138, 3, "al12/m_70"),
            #Chasm of Challenges
            KH2Chest(37, 0, "al13/m_70"),
            KH2Chest(487, 1, "al13/m_70"),
            #"Belle's Room"
            KH2Chest(46, 0, "bb02/m_70"),
            KH2Chest(240, 1, "bb02/m_70"),
            #"Beast's Room"
            KH2Chest(241, 0, "bb03/m_70"),
            #"BC Courtyard"
            KH2Chest(505, 0, "bb06/m_70"),
            KH2Chest(39, 1, "bb06/m_70"),
            KH2Chest(40, 2, "bb06/m_70"),
            #"East Wing"
            KH2Chest(63, 0, "bb07/m_70"),
            KH2Chest(155, 1, "bb07/m_70"),
            #"West Hall"
            KH2Chest(206, 0, "bb08/m_70"),
            KH2Chest(41, 1, "bb08/m_70"),
            KH2Chest(207, 2, "bb08/m_70"),
            KH2Chest(208, 3, "bb08/m_70"),
            KH2Chest(158, 4, "bb08/m_70"),
            KH2Chest(159, 5, "bb08/m_70"),
            #"West Wing"
            KH2Chest(42, 0, "bb09/m_70"),
            KH2Chest(164, 1, "bb09/m_70"),
            #"Dungeon"
            KH2Chest(43, 0, "bb10/m_70"),
            KH2Chest(239, 1, "bb10/m_70"),
            #"Secret Passage"
            KH2Chest(44, 0, "bb12/m_70"),
            KH2Chest(168, 1, "bb12/m_70"),
            KH2Chest(45, 0, "bb12/m_71"),
            #"Ramparts"
            KH2Chest(70, 0, "ca00/m_70"),
            KH2Chest(219, 1, "ca00/m_70"),
            KH2Chest(220, 2, "ca00/m_70"),
            #"PR Town"
            KH2Chest(71, 0, "ca02/m_70"),
            KH2Chest(72, 1, "ca02/m_70"),
            KH2Chest(73, 2, "ca02/m_70"),
            KH2Chest(221, 3, "ca02/m_70"),
            #"Cave Mouth"
            KH2Chest(74, 0, "ca09/m_70"),
            KH2Chest(223, 1, "ca09/m_70"),
            #"Interceptor's Hold"
            KH2Chest(252, 0, "ca11/m_70"),
            #"Powder Store"
            KH2Chest(369, 0, "ca12/m_70"),
            KH2Chest(370, 1, "ca12/m_70"),
            #"Moonlight Nook"
            KH2Chest(75, 0, "ca13/m_70"),
            KH2Chest(224, 1, "ca13/m_70"),
            KH2Chest(371, 2, "ca13/m_70"),
            #"Seadrift Keep"
            KH2Chest(76, 0, "ca14/m_70"),
            KH2Chest(372, 1, "ca14/m_70"),
            KH2Chest(225, 2, "ca14/m_70"),
            #"Seadrift Row"
            KH2Chest(77, 0, "ca15/m_70"),
            KH2Chest(373, 1, "ca15/m_70"),
            KH2Chest(78, 2, "ca15/m_70"),
            #"Library"
            KH2Chest(91, 0, "dc01/m_70"),
            #"DC Courtyard"
            KH2Chest(16, 0, "dc03/m_70"),
            KH2Chest(17, 1, "dc03/m_70"),
            KH2Chest(18, 2, "dc03/m_70"),
            KH2Chest(92, 3, "dc03/m_70"),
            KH2Chest(93, 4, "dc03/m_70"),
            KH2Chest(247, 5, "dc03/m_70"),
            KH2Chest(248, 6, "dc03/m_70"),
            #"Fragment Crossing"
            KH2Chest(374, 0, "eh02/m_70"),
            KH2Chest(375, 1, "eh02/m_70"),
            KH2Chest(376, 2, "eh02/m_70"),
            KH2Chest(377, 3, "eh02/m_70"),
            #"Memory's Skyscraper"
            KH2Chest(391, 0, "eh03/m_70"),
            KH2Chest(523, 1, "eh03/m_70"),
            KH2Chest(524, 2, "eh03/m_70"),
            #"Brink of Despair"
            KH2Chest(335, 0, "eh04/m_70"),
            KH2Chest(500, 1, "eh04/m_70"),
            #"Nothing's Call"
            KH2Chest(378, 0, "eh06/m_70"),
            KH2Chest(379, 1, "eh06/m_70"),
            #"Twilight's View"
            KH2Chest(336, 0, "eh09/m_70"),
            #"Naught's Skyway"
            KH2Chest(381, 0, "eh12/m_70"),
            KH2Chest(382, 1, "eh12/m_70"),
            KH2Chest(380, 2, "eh12/m_70"),
            #"Ruin and Creation's Passage"
            KH2Chest(385, 0, "eh17/m_70"),
            KH2Chest(386, 1, "eh17/m_70"),
            KH2Chest(387, 2, "eh17/m_70"),
            KH2Chest(388, 3, "eh17/m_70"),
            #"Crystal Fissure"
            KH2Chest(180, 0, "hb03/m_70"),
            KH2Chest(181, 1, "hb03/m_70"),
            KH2Chest(179, 2, "hb03/m_70"),
            KH2Chest(489, 3, "hb03/m_70"),
            #"Ansem's Study"
            KH2Chest(184, 0, "hb05/m_70"),
            KH2Chest(183, 0, "hb05/m_71"),
            #"Postern"
            KH2Chest(189, 0, "hb06/m_70"),
            KH2Chest(310, 1, "hb06/m_70"),
            KH2Chest(190, 2, "hb06/m_70"),
            KH2Chest(491, 0, "hb06/m_71"),
            #"Borough"
            KH2Chest(194, 0, "hb09/m_70"),
            KH2Chest(195, 1, "hb09/m_70"),
            KH2Chest(196, 2, "hb09/m_70"),
            KH2Chest(305, 3, "hb09/m_70"),
            KH2Chest(506, 4, "hb09/m_70"),
            #"Corridors"
            KH2Chest(200, 0, "hb11/m_70"),
            KH2Chest(201, 1, "hb11/m_70"),
            KH2Chest(202, 2, "hb11/m_70"),
            KH2Chest(307, 3, "hb11/m_70"),
            #"Heartless Manufactory"
            KH2Chest(311, 0, "hb12/m_70"),
            #"Restoration Site"
            KH2Chest(309, 0, "hb18/m_70"),
            KH2Chest(507, 1, "hb18/m_70"),
            #"CoR Depths"
            KH2Chest(563, 0, "hb21/m_70"),
            KH2Chest(564, 1, "hb21/m_70"),
            KH2Chest(566, 2, "hb21/m_70"),
            KH2Chest(565, 3, "hb21/m_70"),
            KH2Chest(562, 4, "hb21/m_70"),
            KH2Chest(567, 5, "hb21/m_70"),
            #"CoR Mining Area"
            KH2Chest(568, 0, "hb22/m_70"),
            KH2Chest(569, 1, "hb22/m_70"),
            KH2Chest(570, 2, "hb22/m_70"),
            KH2Chest(571, 3, "hb22/m_70"),
            KH2Chest(572, 4, "hb22/m_70"),
            KH2Chest(573, 5, "hb22/m_70"),
            #"CoR Engine Chamber"
            KH2Chest(574, 0, "hb23/m_70"),
            KH2Chest(576, 1, "hb23/m_70"),
            KH2Chest(577, 2, "hb23/m_70"),
            KH2Chest(575, 3, "hb23/m_70"),
            #"CoR Mineshaft"
            KH2Chest(580, 0, "hb24/m_70"),
            KH2Chest(579, 1, "hb24/m_70"),
            KH2Chest(582, 2, "hb24/m_70"),
            KH2Chest(581, 3, "hb24/m_70"),
            KH2Chest(578, 4, "hb24/m_70"),
            #"Garden of Assemblage"
            KH2Chest(585, 0, "hb26/m_70"),
            KH2Chest(586, 1, "hb26/m_70"),
            KH2Chest(590, 0, "hb26/m_71"),
            #"Underworld Entrance"
            KH2Chest(242, 0, "he03/m_70"),
            #"Inner Chamber"
            KH2Chest(2, 0, "he10/m_70"),
            KH2Chest(243, 1, "he10/m_70"),
            #"Caverns Entrance"
            KH2Chest(3, 0, "he11/m_70"),
            KH2Chest(11, 1, "he11/m_70"),
            KH2Chest(504, 2, "he11/m_70"),
            #"The Lock"
            KH2Chest(244, 0, "he12/m_70"),
            KH2Chest(142, 1, "he12/m_70"),
            KH2Chest(5, 2, "he12/m_70"),
            #"Passage"
            KH2Chest(146, 0, "he15/m_70"),
            KH2Chest(7, 1, "he15/m_70"),
            KH2Chest(8, 2, "he15/m_70"),
            KH2Chest(144, 3, "he15/m_70"),
            KH2Chest(145, 4, "he15/m_70"),
            #"Lost Road"
            KH2Chest(9, 0, "he16/m_70"),
            KH2Chest(10, 1, "he16/m_70"),
            KH2Chest(148, 2, "he16/m_70"),
            KH2Chest(149, 3, "he16/m_70"),
            #"Atrium"
            KH2Chest(150, 0, "he17/m_70"),
            KH2Chest(151, 1, "he17/m_70"),
            #"Pride Rock"
            KH2Chest(393, 0, "lk00/m_70"),
            KH2Chest(392, 1, "lk00/m_70"),
            KH2Chest(418, 2, "lk00/m_70"),
            #"Wildebeest Valley"
            KH2Chest(396, 0, "lk03/m_70"),
            KH2Chest(397, 1, "lk03/m_70"),
            KH2Chest(398, 2, "lk03/m_70"),
            KH2Chest(399, 3, "lk03/m_70"),
            KH2Chest(400, 4, "lk03/m_70"),
            #"Elephant Graveyard"
            KH2Chest(401, 0, "lk05/m_70"),
            KH2Chest(403, 1, "lk05/m_70"),
            KH2Chest(402, 2, "lk05/m_70"),
            KH2Chest(509, 3, "lk05/m_70"),
            KH2Chest(508, 4, "lk05/m_70"),
            #"Gorge"
            KH2Chest(405, 0, "lk06/m_70"),
            KH2Chest(404, 1, "lk06/m_70"),
            KH2Chest(492, 2, "lk06/m_70"),
            #"Wastelands"
            KH2Chest(406, 0, "lk07/m_70"),
            KH2Chest(408, 1, "lk07/m_70"),
            KH2Chest(407, 2, "lk07/m_70"),
            #"Jungle"
            KH2Chest(409, 0, "lk08/m_70"),
            KH2Chest(410, 1, "lk08/m_70"),
            KH2Chest(411, 2, "lk08/m_70"),
            #"Oasis"
            KH2Chest(412, 0, "lk09/m_70"),
            KH2Chest(493, 1, "lk09/m_70"),
            KH2Chest(413, 2, "lk09/m_70"),
            #"Bamboo Grove"
            KH2Chest(245, 0, "mu00/m_70"),
            KH2Chest(497, 1, "mu00/m_70"),
            KH2Chest(498, 2, "mu00/m_70"),
            #"Checkpoint"
            KH2Chest(21, 0, "mu02/m_70"),
            KH2Chest(121, 1, "mu02/m_70"),
            #"Mountain Trail"
            KH2Chest(22, 0, "mu03/m_70"),
            KH2Chest(23, 1, "mu03/m_70"),
            KH2Chest(122, 2, "mu03/m_70"),
            KH2Chest(123, 3, "mu03/m_70"),
            #"Village Cave"
            KH2Chest(124, 0, "mu05/m_70"),
            KH2Chest(125, 1, "mu05/m_70"),
            #"Ridge"
            KH2Chest(24, 0, "mu06/m_70"),
            KH2Chest(126, 1, "mu06/m_70"),
            #"Throne Room"
            KH2Chest(26, 0, "mu11/m_70"),
            KH2Chest(27, 1, "mu11/m_70"),
            KH2Chest(128, 2, "mu11/m_70"),
            KH2Chest(129, 3, "mu11/m_70"),
            KH2Chest(130, 4, "mu11/m_70"),
            KH2Chest(131, 5, "mu11/m_70"),
            KH2Chest(25, 6, "mu11/m_70"),
            KH2Chest(127, 7, "mu11/m_70"),
            #"Town Square"
            KH2Chest(209, 0, "nm00/m_70"),
            KH2Chest(210, 1, "nm00/m_70"),
            #"Finklestein's Lab"
            KH2Chest(211, 0, "nm01/m_70"),
            #"Graveyard"
            KH2Chest(53, 0, "nm02/m_70"),
            KH2Chest(212, 1, "nm02/m_70" ),
            #"Hinterlands"
            KH2Chest(214, 0, "nm04/m_70"),
            KH2Chest(54, 1, "nm04/m_70"),
            KH2Chest(213, 2, "nm04/m_70" ),
            #"Candy Cane Lane"
            KH2Chest(55, 0, "nm06/m_70"),
            KH2Chest(56, 1, "nm06/m_70"),
            KH2Chest(216, 2, "nm06/m_70"),
            KH2Chest(217, 3, "nm06/m_70"),
            #"Santa's House"
            KH2Chest(57, 0, "nm08/m_70"),
            KH2Chest(58, 1, "nm08/m_70"),
            #"Starry Hill"
            KH2Chest(94, 0, "po01/m_70"),
            KH2Chest(312, 1, "po01/m_70"),
            #"Pooh's Howse"
            KH2Chest(98, 0, "po02/m_70"),
            KH2Chest(97, 1, "po02/m_70"),
            KH2Chest(313, 2, "po02/m_70"),
            #"Rabbit's Howse"
            KH2Chest(100, 0, "po03/m_70"),
            KH2Chest(101, 1, "po03/m_70"),
            KH2Chest(314, 2, "po03/m_70"),
            #"Piglet's Howse"
            KH2Chest(105, 0, "po04/m_70"),
            KH2Chest(103, 1, "po04/m_70"),
            KH2Chest(104, 2, "po04/m_70"),
            #"Kanga's Howse"
            KH2Chest(106, 0, "po05/m_70"),
            KH2Chest(107, 1, "po05/m_70"),
            KH2Chest(108, 2, "po05/m_70"),
            #"Spooky Cave"
            KH2Chest(116, 0, "po09/m_70"),
            KH2Chest(110, 1, "po09/m_70"),
            KH2Chest(111, 2, "po09/m_70"),
            KH2Chest(112, 3, "po09/m_70"),
            KH2Chest(113, 4, "po09/m_70"),
            KH2Chest(115, 5, "po09/m_70"),
            #"Pit Cell"
            KH2Chest(64, 0, "tr00/m_70"),
            KH2Chest(316, 1, "tr00/m_70"),
            #"Canyon"
            KH2Chest(65, 0, "tr01/m_70"),
            KH2Chest(171, 1, "tr01/m_70"),
            KH2Chest(253, 2, "tr01/m_70"),
            KH2Chest(521, 3, "tr01/m_70"),
            #"Hallway"
            KH2Chest(50, 0, "tr04/m_70"),
            KH2Chest(49, 1, "tr04/m_70"),
            #"Communications Room"
            KH2Chest(499, 0, "tr05/m_70"),
            KH2Chest(255, 1, "tr05/m_70"),
            #"Central Computer Core"
            KH2Chest(51, 0, "tr08/m_70"),
            KH2Chest(177, 1, "tr08/m_70"),
            KH2Chest(178, 2, "tr08/m_70"),
            KH2Chest(488, 3, "tr08/m_70"),
            #"STT Central Station"
            KH2Chest(428, 0, "tt09/m_70"),
            KH2Chest(429, 1, "tt09/m_70"),
            KH2Chest(430, 2, "tt09/m_70"),
            #"STT Sunset Terrace"
            KH2Chest(434, 0, "tt10/m_70"),
            KH2Chest(435, 1, "tt10/m_70"),
            KH2Chest(436, 2, "tt10/m_70"),
            KH2Chest(437, 3, "tt10/m_70"),
            #"STT Mansion Foyer"
            KH2Chest(449, 0, "tt15/m_70"),
            KH2Chest(450, 1, "tt15/m_70"),
            KH2Chest(451, 2, "tt15/m_70"),
            #"STT Mansion Dining Room"
            KH2Chest(455, 0, "tt16/m_70"),
            KH2Chest(456, 1, "tt16/m_70"),
            #"STT Mansion Library"
            KH2Chest(459, 0, "tt17/m_70"),
            #"STT Mansion Basement"
            KH2Chest(463, 0, "tt22/m_70"),
            #"STT Dive to the Heart"
            KH2Chest(315, 0, "tt32/m_70"),
            KH2Chest(472, 0, "tt33/m_70"),
            #"TT Tram Common"
            KH2Chest(420, 0, "tt07/m_71"),
            KH2Chest(421, 1, "tt07/m_71"),
            KH2Chest(422, 2, "tt07/m_71"),
            KH2Chest(423, 3, "tt07/m_71"),
            KH2Chest(424, 4, "tt07/m_71"),
            KH2Chest(425, 5, "tt07/m_71"),
            KH2Chest(484, 6, "tt07/m_71"),
            #"TT Central Station"
            KH2Chest(431, 0, "tt09/m_71"),
            KH2Chest(433, 1, "tt09/m_71"),
            KH2Chest(432, 2, "tt09/m_71"),
            #"TT Sunset Terrace"
            KH2Chest(438, 0, "tt10/m_71"),
            KH2Chest(439, 1, "tt10/m_71"),
            KH2Chest(440, 2, "tt10/m_71"),
            KH2Chest(441, 3, "tt10/m_71"),
            #"TT Woods"
            KH2Chest(442, 0, "tt13/m_71"),
            KH2Chest(443, 1, "tt13/m_71"),
            KH2Chest(444, 2, "tt13/m_71"),
            #"TT Old Mansion"
            KH2Chest(447, 0, "tt14/m_71"),
            KH2Chest(448, 1, "tt14/m_71"),
            #"TT Mansion Foyer"
            KH2Chest(452, 0, "tt15/m_71"),
            KH2Chest(453, 1, "tt15/m_71"),
            KH2Chest(454, 2, "tt15/m_71"),
            #"TT Mansion Dining Room"
            KH2Chest(457, 0, "tt16/m_71"),
            KH2Chest(458, 1, "tt16/m_71"),
            #"TT Mansion Library"
            KH2Chest(460, 0, "tt17/m_71"),
            #"TT Mansion Basement"
            KH2Chest(464, 0, "tt22/m_71"),
            #"TT Yensid Tower"
            KH2Chest(465, 0, "tt25/m_71"),
            KH2Chest(466, 1, "tt25/m_71"),
            KH2Chest(522, 2, "tt25/m_71"),
            #"TT Yensid Tower Entryway"
            KH2Chest(467, 0, "tt26/m_71"),
            KH2Chest(468, 1, "tt26/m_71"),
            #"TT Sorcerer's Loft"
            KH2Chest(469, 0, "tt27/m_71"),
            #"TT Tower Wardrobe"
            KH2Chest(470, 0, "tt28/m_71"),
            #"TT Tunnelway"
            KH2Chest(477, 0, "tt36/m_71"),
            KH2Chest(478, 1, "tt36/m_71"),
            #"TT Underground Concourse"
            KH2Chest(479, 0, "tt37/m_71"),
            KH2Chest(480, 1, "tt37/m_71"),
            KH2Chest(481, 2, "tt37/m_71"),
            KH2Chest(482, 3, "tt37/m_71"),
            #Cornerstone Hill
            KH2Chest(12, 0, "wi00/m_70"),
            KH2Chest(79, 1, "wi00/m_70"),
            #Pier
            KH2Chest(81, 0, "wi01/m_70"),
            KH2Chest(82, 1, "wi01/m_70"),
            #Wharf
            KH2Chest(83, 0, "wi02/m_70"),
            KH2Chest(84, 1, "wi02/m_70"),
            KH2Chest(85, 2, "wi02/m_70")
        ]

chestFiles = [
    "al00/m_70", 
    "al01/m_70", 
    "al06/m_70", 
    "al07/m_70", 
    "al10/m_70", 
    "al11/m_70", 
    "al12/m_70", 
    "al13/m_70", 
    "bb02/m_70", 
    "bb03/m_70", 
    "bb06/m_70", 
    "bb07/m_70", 
    "bb08/m_70", 
    "bb09/m_70", 
    "bb10/m_70", 
    "bb12/m_70", 
    "bb12/m_71", 
    "ca00/m_70", 
    "ca02/m_70", 
    "ca09/m_70", 
    "ca11/m_70", 
    "ca12/m_70", 
    "ca13/m_70", 
    "ca14/m_70", 
    "ca15/m_70", 
    "dc01/m_70", 
    "dc03/m_70", 
    "eh02/m_70", 
    "eh03/m_70", 
    "eh04/m_70", 
    "eh06/m_70", 
    "eh09/m_70", 
    "eh12/m_70", 
    "eh17/m_70", 
    "hb03/m_70", 
    "hb05/m_70", 
    "hb05/m_71", 
    "hb06/m_70", 
    "hb06/m_71", 
    "hb09/m_70", 
    "hb11/m_70", 
    "hb12/m_70", 
    "hb18/m_70", 
    "hb21/m_70", 
    "hb22/m_70", 
    "hb23/m_70", 
    "hb24/m_70", 
    "hb26/m_70", 
    "hb26/m_71", 
    "he03/m_70", 
    "he10/m_70", 
    "he11/m_70", 
    "he12/m_70", 
    "he15/m_70", 
    "he16/m_70", 
    "he17/m_70", 
    "lk00/m_70", 
    "lk03/m_70", 
    "lk05/m_70", 
    "lk06/m_70", 
    "lk07/m_70", 
    "lk08/m_70", 
    "lk09/m_70", 
    "mu00/m_70", 
    "mu02/m_70", 
    "mu03/m_70", 
    "mu05/m_70", 
    "mu06/m_70", 
    "mu11/m_70", 
    "nm00/m_70", 
    "nm01/m_70", 
    "nm02/m_70", 
    "nm04/m_70", 
    "nm06/m_70", 
    "nm08/m_70", 
    "po01/m_70", 
    "po02/m_70", 
    "po03/m_70", 
    "po04/m_70", 
    "po05/m_70", 
    "po09/m_70", 
    "tr00/m_70", 
    "tr01/m_70", 
    "tr04/m_70", 
    "tr05/m_70", 
    "tr08/m_70", 
    "tt09/m_70", 
    "tt10/m_70", 
    "tt15/m_70", 
    "tt16/m_70", 
    "tt17/m_70", 
    "tt22/m_70", 
    "tt32/m_70", 
    "tt33/m_70", 
    "tt07/m_71", 
    "tt09/m_71", 
    "tt10/m_71", 
    "tt13/m_71", 
    "tt14/m_71", 
    "tt15/m_71", 
    "tt16/m_71", 
    "tt17/m_71", 
    "tt22/m_71", 
    "tt25/m_71", 
    "tt26/m_71", 
    "tt27/m_71", 
    "tt28/m_71", 
    "tt36/m_71", 
    "tt37/m_71", 
    "wi00/m_70", 
    "wi01/m_70", 
    "wi02/m_70"]

def getChestFileList():
    return chestFiles