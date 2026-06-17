import random
from Class.openkhmod import AttackEntriesOrganizer, ATKPObject

WEAK_MAX_DIFFERENCE = 0.3
WEAK_MIN_DIFFERENCE = 0.0
MILD_MAX_DIFFERENCE = 0.5
MILD_MIN_DIFFERENCE = 0.0
MEDIUM_MAX_DIFFERENCE = 0.8
MEDIUM_MIN_DIFFERENCE = 0.2
STRONG_MAX_DIFFERENCE = 1.2
STRONG_MIN_DIFFERENCE = 0.5
HEAVY_MAX_DIFFERENCE = 2.0
HEAVY_MIN_DIFFERENCE = 0.8
CHAOS_MAX_DIFFERENCE = 4.0
CHAOS_MIN_DIFFERENCE = 0.0

LIST_OF_COMPANION_IDS = [
	1698,
	151,
	152,
	155,
	1698,
	151,
	152,
	155,
	153,
	154,
	1163,
	1164,
	1165,
	1525,
	139,
	146,
	156,
	157,
	158,
	159,
	1160,
	1188,
	1161,
	1162,
	224,
	895,
	225,
	563,
	564,
	565,
	273,
	274,
	1176,
	1177,
	1178,
	861,
	941,
	862,
	863,
	864,
	864,
	1179,
	1180,
	1526,
	214,
	215,
	216,
	217,
	218,
	1174,
	1175,
	1193,
	365,
	366,
	367,
	368,
	369,
	371,
	384,
	387,
	385,
	372,
	373,
	1169,
	622,
	219,
	220,
	223,
	221,
	222,
	1166,
	570,
	575,
	361,
	1527,
	1528,
	1529,
	627,
	1181,
	494,
	495,
	646,
	647,
	648,
	515,
	649,
	1171,
	1172,
	1173,
	1494,
	1495,
	1496,
	1497,
	1498,
	1499,
	1500,
	1501,
	1502,
	1503,
	1504,
	1505,
	1506,
	1507,
	1508,
	1509,
	1510,
	1511,
	1512,
	1513,
	1514,
	1515,
	1516,
	1531,
	1532,
	193,
	194,
	195,
	196,
	1272,
	1576,
	153,
	154,
	1716,
	1717,
	1718,
	1165,
	1643,
	1942,
	85,
	86,
	87,
	95,
	1253,
	1258,
	1188,
	1292,
	1293,
	1294,
	1295,
	1296,
	1297,
	1315,
	1006,
	1183,
	1644,
	1689,
	1265,
	988,
	996,
	999,
	1555,
	1579,
	1477,
	1478,
	1373,
	1628,
	1629,
	1631,
	1135,
	1574,
	1225,
	860,
	1573,
	855,
	1227,
	1733,
	1261,
	1441,
	1444,
	1445,
	883,
	1210,
]
KNOCBACK_LIST = [8, 11, 12]

ALL_DAMAGE_PRESETS = {
	"WEAK": [WEAK_MAX_DIFFERENCE, WEAK_MIN_DIFFERENCE],
	"MILD": [MILD_MAX_DIFFERENCE, MILD_MIN_DIFFERENCE],
	"MEDIUM": [MEDIUM_MAX_DIFFERENCE, MEDIUM_MIN_DIFFERENCE],
	"STRONG": [STRONG_MAX_DIFFERENCE, STRONG_MIN_DIFFERENCE],
	"HEAVY": [HEAVY_MAX_DIFFERENCE, HEAVY_MIN_DIFFERENCE],
	"CHAOS": [CHAOS_MAX_DIFFERENCE, CHAOS_MIN_DIFFERENCE],
}
ALL_KNOCKBACK_AMOUNT_PRESETS = {
	"WEAK": [WEAK_MAX_DIFFERENCE, WEAK_MIN_DIFFERENCE],
	"MILD": [MILD_MAX_DIFFERENCE, MILD_MIN_DIFFERENCE],
	"MEDIUM": [MEDIUM_MAX_DIFFERENCE, MEDIUM_MIN_DIFFERENCE],
	"STRONG": [STRONG_MAX_DIFFERENCE, STRONG_MIN_DIFFERENCE],
	"HEAVY": [HEAVY_MAX_DIFFERENCE, HEAVY_MIN_DIFFERENCE],
	"CHAOS": [CHAOS_MAX_DIFFERENCE, CHAOS_MIN_DIFFERENCE],
}
ALL_REVENGE_VALUE_PRESETS = {
	"WEAK": [0, 1],
	"MILD": [0, 2],
	"MEDIUM": [1, 2],
	"STRONG": [1, 3],
	"HEAVY": [2, 4],
	"CHAOS": [0, 10],
}
ALL_MULTI_HIT_PRESETS = {
	"WEAK": [3, 24, 32],
	"MILD": [5, 22, 28],
	"MEDIUM": [8, 18, 28],
	"STRONG": [12, 15, 24],
	"HEAVY": [20, 8, 24],
	"CHAOS": [25, 3, 32],
}

class atkpRandomizerClass:
	def __init__(self, kill_boss, companion_damage):
		self.companion_kill_boss = kill_boss
		self.companion_deal_damage = companion_damage
		self.DAMAGE_PRESETS = []
		self.KNOCKBACK_AMOUNT_PRESETS = []
		self.REVENGE_VALUE_PRESETS = []
		self.MULTI_HIT_PRESETS = []
	
	def randomize_atkp_data(self, atkp_organizer: AttackEntriesOrganizer, damage_preset: str, on_hit, element, revenge_value_preset, multi_hit_preset, knockback_amount_preset):
		list_data = atkp_organizer.get_all_attack_ids()
		attack_entries = []
		self.DAMAGE_PRESETS = ALL_DAMAGE_PRESETS[damage_preset]
		self.KNOCKBACK_AMOUNT_PRESETS = ALL_KNOCKBACK_AMOUNT_PRESETS[knockback_amount_preset]
		self.REVENGE_VALUE_PRESETS = ALL_REVENGE_VALUE_PRESETS[revenge_value_preset]
		self.MULTI_HIT_PRESETS = ALL_MULTI_HIT_PRESETS[multi_hit_preset]

		for attack_entry in list_data:
			attack_entries.append(atkp_organizer.attack_entry_constructor(attack_entry))
		for attack_entry in attack_entries:
			attack_entry: ATKPObject
			attack_entry.Power = int(round(self.randomize_power(attack_entry.Power)))
			if(element):
				attack_entry.Element = self.randomize_elements()
			if(LIST_OF_COMPANION_IDS.__contains__(attack_entry.Id)):
				if(self.companion_deal_damage):
					attack_entry.EnemyReaction = self.randomize_companion_knockback_type()
				attack_entry.Flags = self.companion_kill_boss
			if(on_hit): 
				attack_entry.EffectOnHit = self.randomize_on_hit()
			#Knockback values in vanilla can reach as high as 32767, which I don't think is for attacks that really knock you back
			#Therefore, to avoid overflow issues, knockback is capped at 32767. This limit shouldn't be reached by any other number
			attack_entry.KnockbackStrength1 = min(int(round(self.randomize_value(attack_entry.KnockbackStrength1, self.KNOCKBACK_AMOUNT_PRESETS[0], self.KNOCKBACK_AMOUNT_PRESETS[1]))), 32767)
			attack_entry.KnockbackStrength2 = min(int(round(self.randomize_value(attack_entry.KnockbackStrength2, self.KNOCKBACK_AMOUNT_PRESETS[0], self.KNOCKBACK_AMOUNT_PRESETS[1]))), 32767)
			attack_entry.RevengeDamage += self.randomize_revenge_value(self.REVENGE_VALUE_PRESETS[0], self.REVENGE_VALUE_PRESETS[1])
			self.randomize_multi_hit(self.MULTI_HIT_PRESETS[0], self.MULTI_HIT_PRESETS[1], self.MULTI_HIT_PRESETS[2], attack_entry)
		
		for attack_entry in attack_entries:
			atkp_organizer.convert_atkp_object_to_dict_and_add_to_data(attack_entry)
				


	def randomize_value(self, value, max_difference, min_difference):
		increase_value = False
		if(random.randint(0, 100) > 50):
			increase_value = True
		if(increase_value):
			multiplier = 1.0 + random.uniform(min_difference, max_difference)
			return value * multiplier
		else:
			divisor = 1.0 + random.uniform(min_difference, max_difference)
			return value / divisor
	
	def randomize_elements(self):
		return random.randint(0, 5)
	
	def randomize_on_hit(self):
		return random.randint(0, 12)
	
	def randomize_companion_knockback_type(self):
		index = random.randint(0, 2)
		return KNOCBACK_LIST[index]

	def randomize_multi_hit(self, chance, minFrames, maxFrames, current_attack_entry: ATKPObject):
		if(random.randint(1, 100) > chance):
			return
		current_attack_entry.Interval = random.randint(minFrames, maxFrames)
	
	# Because a lot of moves have either 0 revenge value or a high amount, randomization
	# is handled by first determining if any change will happen, then by a flat value.
	# This is to avoid 0 values being multiplied uselessly or moves with revenge value
	# to get ridiculously high. Generally, revenge value is not randomized at high
	# differences because the game would be kind of unplayable. (unless Chaos enabled)
	def randomize_revenge_value(self, minValue, maxValue):
		increase_value = False
		if(random.randint(0, 100) > 50):
			increase_value = True
		num = random.randint(minValue, maxValue)
		if(not increase_value):
			return -num
		return num

	def randomize_power(self, value):
		if(value == 0):
			return 0
		return self.randomize_value(value, self.DAMAGE_PRESETS[0], self.DAMAGE_PRESETS[1])
