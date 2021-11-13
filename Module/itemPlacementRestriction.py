from collections import namedtuple

RestrictedConfig = namedtuple("RestrictedConfig","treasures bonuses forms puzzles")

class ItemPlacementRestriction():
    def __init__(self,mode,nightmare=False):
        need_fire_blizzard_thunder = lambda inventory : (21 in inventory and 22 in inventory and 23 in inventory)
        need_1_magnet = lambda inventory : (inventory.count(87)>=1)
        need_2_magnets = lambda inventory : (inventory.count(87)>=2)
        need_2_magnets_all_thunders = lambda inventory : (inventory.count(87)>=2 and inventory.count(23)==3)
        count_high_jumps = lambda inventory : ((94 in inventory) + (95 in inventory) + (96 in inventory) + (97 in inventory))
        count_quick_runs = lambda inventory : ((98 in inventory) + (99 in inventory) + (100 in inventory) + (101 in inventory))
        count_aerial_dodges = lambda inventory : ((102 in inventory) + (103 in inventory) + (104 in inventory) + (105 in inventory))
        count_glides = lambda inventory : ((106 in inventory) + (107 in inventory) + (108 in inventory) + (109 in inventory))
        need_growths = lambda inventory : (count_high_jumps(inventory)>=3 and count_quick_runs(inventory)>=3 and count_aerial_dodges(inventory)>=3 and count_glides(inventory)>=3)
        need_proof_connection = lambda inventory : (593 in inventory)
        need_proof_peace = lambda inventory : (595 in inventory)
        has_valor = lambda inventory : (26 in inventory)
        has_wisdom = lambda inventory : (27 in inventory)
        has_limit = lambda inventory : (563 in inventory)
        has_master = lambda inventory : (31 in inventory)
        has_final = lambda inventory : (29 in inventory)
        has_auto_valor = lambda inventory : (385 in inventory)
        has_auto_wisdom = lambda inventory : (386 in inventory)
        has_auto_limit = lambda inventory : (568 in inventory)
        has_auto_master = lambda inventory : (387 in inventory)
        has_auto_final = lambda inventory : (388 in inventory)
        count_forms = lambda inventory : (has_valor(inventory) + has_wisdom(inventory) + has_limit(inventory) + has_master(inventory) + has_final(inventory))
        count_auto_forms = lambda inventory : (has_auto_valor(inventory) + has_auto_wisdom(inventory) + has_auto_limit(inventory) + has_auto_master(inventory) )
        need_forms  = lambda inventory : (count_forms(inventory)==5)
        need_summons = lambda inventory : (( 159 in inventory) and ( 160 in inventory) and ( 25 in inventory) and ( 383 in inventory))
        need_forms_and_summons = lambda inventory : (need_forms(inventory) and need_summons(inventory))
        count_pages = lambda inventory : inventory.count(32)
        need_1_page = lambda inventory : count_pages(inventory) >= 1
        need_2_pages = lambda inventory : count_pages(inventory) >= 2
        need_3_pages = lambda inventory : count_pages(inventory) >= 3
        need_4_pages = lambda inventory : count_pages(inventory) >= 4
        need_5_pages = lambda inventory : count_pages(inventory) == 5

        if mode=="Reverse":
            restricted_treasures = [([34,486,303,545,550,250,251,35,36,137,138,487,37,502,503,300],need_fire_blizzard_thunder),
                                    ([287],need_1_magnet),
                                    ([367],need_2_magnets_all_thunders),
                                    ([587,591],need_proof_connection),
                                    ([560],need_forms),
                                    ([518],need_forms_and_summons),
                                    ([313,97,98], need_5_pages),
                                    ([103,104,105], need_4_pages),
                                    ([100,101,314], need_3_pages),
                                    ([106,107,108], need_2_pages),
                                    ([110,111,112,113,115,116,284,485], need_1_page)]
            restricted_bonuses = [([15,37,42,46],need_fire_blizzard_thunder)]
        else: #regular seed restrictions
            restricted_treasures = [([34,486,303,545,550],need_fire_blizzard_thunder),
                                    ([287],need_2_magnets),
                                    ([279,538],need_2_magnets_all_thunders),
                                    ([562,563,564,565,566,567,568,569,570,571,572,573,574,575,576,577,578,579,580,581,582],need_growths),
                                    ([587,591],need_proof_connection),
                                    ([588,589],need_proof_peace),
                                    ([560],need_forms),
                                    ([518],need_forms_and_summons),
                                    ([103,104,105], need_1_page),
                                    ([100,101,314], need_2_pages),
                                    ([106,107,108], need_3_pages),
                                    ([110,111,112,113,115,116,284,485], need_4_pages),
                                    ([285,539,312,94], need_5_pages)]

            restricted_bonuses = [([15],need_fire_blizzard_thunder)]


        def make_form_lambda(form_id,form_level):
            if form_id=="Valor":
                return lambda inventory : has_valor(inventory) and count_forms(inventory)>=form_level-2
            if form_id=="Wisdom":
                return lambda inventory : has_wisdom(inventory) and count_forms(inventory)>=form_level-2
            if form_id=="Limit":
                return lambda inventory : has_limit(inventory) and count_forms(inventory)>=form_level-2
            if form_id=="Master":
                return lambda inventory : has_master(inventory) and count_forms(inventory)>=form_level-2
            if form_id=="Final":
                return lambda inventory : has_final(inventory) and count_forms(inventory)>=form_level-2

            return lambda inventory : False

        def make_form_lambda_nightmare(form_id,form_level):
            final_possible_but_not_obtained = lambda inventory : (has_valor(inventory) or has_wisdom(inventory) or has_limit(inventory) or has_master(inventory) or count_auto_forms(inventory)>=1) and not has_final(inventory)
            form_level_obtainable = lambda inventory : count_forms(inventory) + (1 if final_possible_but_not_obtained(inventory) else 0) + 2

            if form_id=="Valor":
                return lambda inventory : (has_valor(inventory) or has_auto_valor(inventory) ) and form_level_obtainable(inventory)>=form_level
            if form_id=="Wisdom":
                return lambda inventory : (has_wisdom(inventory) or has_auto_wisdom(inventory) ) and form_level_obtainable(inventory)>=form_level
            if form_id=="Limit":
                return lambda inventory : (has_limit(inventory) or has_auto_limit(inventory) ) and form_level_obtainable(inventory)>=form_level
            if form_id=="Master":
                return lambda inventory : (has_master(inventory) or has_auto_master(inventory) ) and form_level_obtainable(inventory)>=form_level
            if form_id=="Final":
                have_final_form = lambda inventory : final_possible_but_not_obtained(inventory) or has_final(inventory)
                if form_level==2:
                    return lambda inventory : have_final_form(inventory) or has_auto_final(inventory)
                else:
                    return lambda inventory : have_final_form(inventory) and form_level_obtainable(inventory)>=form_level

            return lambda inventory : False

        if not nightmare:
            restricted_forms = [("Valor",2,make_form_lambda("Valor",2)),
                                ("Valor",3,make_form_lambda("Valor",3)),
                                ("Valor",4,make_form_lambda("Valor",4)),
                                ("Valor",5,make_form_lambda("Valor",5)),
                                ("Valor",6,make_form_lambda("Valor",6)),
                                ("Valor",7,make_form_lambda("Valor",7)),
                                ("Wisdom",2,make_form_lambda("Wisdom",2)),
                                ("Wisdom",3,make_form_lambda("Wisdom",3)),
                                ("Wisdom",4,make_form_lambda("Wisdom",4)),
                                ("Wisdom",5,make_form_lambda("Wisdom",5)),
                                ("Wisdom",6,make_form_lambda("Wisdom",6)),
                                ("Wisdom",7,make_form_lambda("Wisdom",7)),
                                ("Limit",2,make_form_lambda("Limit",2)),
                                ("Limit",3,make_form_lambda("Limit",3)),
                                ("Limit",4,make_form_lambda("Limit",4)),
                                ("Limit",5,make_form_lambda("Limit",5)),
                                ("Limit",6,make_form_lambda("Limit",6)),
                                ("Limit",7,make_form_lambda("Limit",7)),
                                ("Master",2,make_form_lambda("Master",2)),
                                ("Master",3,make_form_lambda("Master",3)),
                                ("Master",4,make_form_lambda("Master",4)),
                                ("Master",5,make_form_lambda("Master",5)),
                                ("Master",6,make_form_lambda("Master",6)),
                                ("Master",7,make_form_lambda("Master",7)),
                                ("Final",2,make_form_lambda("Final",2)),
                                ("Final",3,make_form_lambda("Final",3)),
                                ("Final",4,make_form_lambda("Final",4)),
                                ("Final",5,make_form_lambda("Final",5)),
                                ("Final",6,make_form_lambda("Final",6)),
                                ("Final",7,make_form_lambda("Final",7))]
        else:
            restricted_forms = [("Valor",2,make_form_lambda_nightmare("Valor",2)),
                            ("Valor",3,make_form_lambda_nightmare("Valor",3)),
                            ("Valor",4,make_form_lambda_nightmare("Valor",4)),
                            ("Valor",5,make_form_lambda_nightmare("Valor",5)),
                            ("Valor",6,make_form_lambda_nightmare("Valor",6)),
                            ("Valor",7,make_form_lambda_nightmare("Valor",7)),
                            ("Wisdom",2,make_form_lambda_nightmare("Wisdom",2)),
                            ("Wisdom",3,make_form_lambda_nightmare("Wisdom",3)),
                            ("Wisdom",4,make_form_lambda_nightmare("Wisdom",4)),
                            ("Wisdom",5,make_form_lambda_nightmare("Wisdom",5)),
                            ("Wisdom",6,make_form_lambda_nightmare("Wisdom",6)),
                            ("Wisdom",7,make_form_lambda_nightmare("Wisdom",7)),
                            ("Limit",2,make_form_lambda_nightmare("Limit",2)),
                            ("Limit",3,make_form_lambda_nightmare("Limit",3)),
                            ("Limit",4,make_form_lambda_nightmare("Limit",4)),
                            ("Limit",5,make_form_lambda_nightmare("Limit",5)),
                            ("Limit",6,make_form_lambda_nightmare("Limit",6)),
                            ("Limit",7,make_form_lambda_nightmare("Limit",7)),
                            ("Master",2,make_form_lambda_nightmare("Master",2)),
                            ("Master",3,make_form_lambda_nightmare("Master",3)),
                            ("Master",4,make_form_lambda_nightmare("Master",4)),
                            ("Master",5,make_form_lambda_nightmare("Master",5)),
                            ("Master",6,make_form_lambda_nightmare("Master",6)),
                            ("Master",7,make_form_lambda_nightmare("Master",7)),
                            ("Final",2,make_form_lambda_nightmare("Final",2)),
                            ("Final",3,make_form_lambda_nightmare("Final",3)),
                            ("Final",4,make_form_lambda_nightmare("Final",4)),
                            ("Final",5,make_form_lambda_nightmare("Final",5)),
                            ("Final",6,make_form_lambda_nightmare("Final",6)),
                            ("Final",7,make_form_lambda_nightmare("Final",7))]


        restricted_puzzles = [(1,need_growths),
                              (2,need_growths),
                              (3,need_growths),
                              (4,lambda inventory : need_growths(inventory) and need_5_pages(inventory)),
                              (5,need_growths)]

        def treasure_restriction(location):
            for loc_list,condition in restricted_treasures:
                if location.LocationId in loc_list:
                    return condition
            return lambda inventory: True
        def bonus_restriction(location):
            for loc_list,condition in restricted_bonuses:
                if location.LocationId in loc_list:
                    return condition
            return lambda inventory: True
        def form_restriction(location):
            for f_id,f_level,condition in restricted_forms:
                if f_id in location.Description and str(f_level) in location.Description:
                    return condition
            return lambda inventory: True
        def puzzle_restriction(location):
            puzzle_id = location.LocationId
            for p_id,condition in restricted_puzzles:
                if p_id == puzzle_id :
                    return condition
            return lambda inventory: True

        self.treasure_restriction_function = treasure_restriction
        self.bonus_restriction_function = bonus_restriction
        self.form_restriction_function = form_restriction
        self.puzzle_restriction_function = puzzle_restriction

    def get_restriction_functions(self):
        return RestrictedConfig(self.treasure_restriction_function,self.bonus_restriction_function,self.form_restriction_function,self.puzzle_restriction_function)