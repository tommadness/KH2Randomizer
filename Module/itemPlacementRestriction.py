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
            print("Reverse Rando Restrictions")
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
            if form_id==1:
                return lambda inventory : has_valor(inventory) and count_forms(inventory)>=form_level-2
            if form_id==2:
                return lambda inventory : has_wisdom(inventory) and count_forms(inventory)>=form_level-2
            if form_id==3:
                return lambda inventory : has_limit(inventory) and count_forms(inventory)>=form_level-2
            if form_id==4:
                return lambda inventory : has_master(inventory) and count_forms(inventory)>=form_level-2
            if form_id==5:
                return lambda inventory : has_final(inventory) and count_forms(inventory)>=form_level-2

            return lambda inventory : False

        def make_form_lambda_nightmare(form_id,form_level):
            final_possible_but_not_obtained = lambda inventory : (has_valor(inventory) or has_wisdom(inventory) or has_limit(inventory) or has_master(inventory) or count_auto_forms(inventory)>=1) and not has_final(inventory)
            form_level_obtainable = lambda inventory : count_forms(inventory) + (1 if final_possible_but_not_obtained(inventory) else 0) + 2

            if form_id==1:
                return lambda inventory : (has_valor(inventory) or has_auto_valor(inventory) ) and form_level_obtainable(inventory)>=form_level
            if form_id==2:
                return lambda inventory : (has_wisdom(inventory) or has_auto_wisdom(inventory) ) and form_level_obtainable(inventory)>=form_level
            if form_id==3:
                return lambda inventory : (has_limit(inventory) or has_auto_limit(inventory) ) and form_level_obtainable(inventory)>=form_level
            if form_id==4:
                return lambda inventory : (has_master(inventory) or has_auto_master(inventory) ) and form_level_obtainable(inventory)>=form_level
            if form_id==5:
                have_final_form = lambda inventory : final_possible_but_not_obtained(inventory) or has_final(inventory)
                if form_level==2:
                    return lambda inventory : have_final_form(inventory) or has_auto_final(inventory)
                else:
                    return lambda inventory : have_final_form(inventory) and form_level_obtainable(inventory)>=form_level

            return lambda inventory : False

        if not nightmare:
            restricted_forms = [(1,2,make_form_lambda(1,2)),
                                (1,3,make_form_lambda(1,3)),
                                (1,4,make_form_lambda(1,4)),
                                (1,5,make_form_lambda(1,5)),
                                (1,6,make_form_lambda(1,6)),
                                (1,7,make_form_lambda(1,7)),
                                (2,2,make_form_lambda(2,2)),
                                (2,3,make_form_lambda(2,3)),
                                (2,4,make_form_lambda(2,4)),
                                (2,5,make_form_lambda(2,5)),
                                (2,6,make_form_lambda(2,6)),
                                (2,7,make_form_lambda(2,7)),
                                (3,2,make_form_lambda(3,2)),
                                (3,3,make_form_lambda(3,3)),
                                (3,4,make_form_lambda(3,4)),
                                (3,5,make_form_lambda(3,5)),
                                (3,6,make_form_lambda(3,6)),
                                (3,7,make_form_lambda(3,7)),
                                (4,2,make_form_lambda(4,2)),
                                (4,3,make_form_lambda(4,3)),
                                (4,4,make_form_lambda(4,4)),
                                (4,5,make_form_lambda(4,5)),
                                (4,6,make_form_lambda(4,6)),
                                (4,7,make_form_lambda(4,7)),
                                (5,2,make_form_lambda(5,2)),
                                (5,3,make_form_lambda(5,3)),
                                (5,4,make_form_lambda(5,4)),
                                (5,5,make_form_lambda(5,5)),
                                (5,6,make_form_lambda(5,6)),
                                (5,7,make_form_lambda(5,7))]
        else:
            restricted_forms = [(1,2,make_form_lambda_nightmare(1,2)),
                            (1,3,make_form_lambda_nightmare(1,3)),
                            (1,4,make_form_lambda_nightmare(1,4)),
                            (1,5,make_form_lambda_nightmare(1,5)),
                            (1,6,make_form_lambda_nightmare(1,6)),
                            (1,7,make_form_lambda_nightmare(1,7)),
                            (2,2,make_form_lambda_nightmare(2,2)),
                            (2,3,make_form_lambda_nightmare(2,3)),
                            (2,4,make_form_lambda_nightmare(2,4)),
                            (2,5,make_form_lambda_nightmare(2,5)),
                            (2,6,make_form_lambda_nightmare(2,6)),
                            (2,7,make_form_lambda_nightmare(2,7)),
                            (3,2,make_form_lambda_nightmare(3,2)),
                            (3,3,make_form_lambda_nightmare(3,3)),
                            (3,4,make_form_lambda_nightmare(3,4)),
                            (3,5,make_form_lambda_nightmare(3,5)),
                            (3,6,make_form_lambda_nightmare(3,6)),
                            (3,7,make_form_lambda_nightmare(3,7)),
                            (4,2,make_form_lambda_nightmare(4,2)),
                            (4,3,make_form_lambda_nightmare(4,3)),
                            (4,4,make_form_lambda_nightmare(4,4)),
                            (4,5,make_form_lambda_nightmare(4,5)),
                            (4,6,make_form_lambda_nightmare(4,6)),
                            (4,7,make_form_lambda_nightmare(4,7)),
                            (5,2,make_form_lambda_nightmare(5,2)),
                            (5,3,make_form_lambda_nightmare(5,3)),
                            (5,4,make_form_lambda_nightmare(5,4)),
                            (5,5,make_form_lambda_nightmare(5,5)),
                            (5,6,make_form_lambda_nightmare(5,6)),
                            (5,7,make_form_lambda_nightmare(5,7))]


        restricted_puzzles = [(1,need_growths),
                              (2,need_growths),
                              (3,need_growths),
                              (4,lambda inventory : need_growths(inventory) and need_5_pages(inventory)),
                              (5,need_growths)]

        def treasure_restriction(location_id):
            for loc_list,condition in restricted_treasures:
                if location_id in loc_list:
                    return condition
            return lambda inventory: True
        def bonus_restriction(location_id):
            for loc_list,condition in restricted_bonuses:
                if location_id in loc_list:
                    return condition
            return lambda inventory: True
        def form_restriction(form_id,form_level):
            for f_id,f_level,condition in restricted_forms:
                if f_id == form_id and f_level==form_level:
                    return condition
            return lambda inventory: True
        def puzzle_restriction(puzzle_id):
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