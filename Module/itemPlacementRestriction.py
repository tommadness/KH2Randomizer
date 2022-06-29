from collections import namedtuple

class ItemPlacementHelpers():
    def __init__(self):
        pass

    @staticmethod
    def need_fire_blizzard_thunder(inventory):
        return 21 in inventory and 22 in inventory and 23 in inventory

    @staticmethod
    def need_1_magnet(inventory):
        return inventory.count(87)>=1

    @staticmethod
    def need_2_magnet(inventory):
        return inventory.count(87)>=2

    @staticmethod
    def need_3_thunders(inventory):
        return inventory.count(23)==3

    @staticmethod
    def need_growths(inventory):
        count_high_jumps = lambda inventory : ((94 in inventory) + (95 in inventory) + (96 in inventory) + (97 in inventory))
        count_quick_runs = lambda inventory : ((98 in inventory) + (99 in inventory) + (100 in inventory) + (101 in inventory))
        count_aerial_dodges = lambda inventory : ((102 in inventory) + (103 in inventory) + (104 in inventory) + (105 in inventory))
        count_glides = lambda inventory : ((106 in inventory) + (107 in inventory) + (108 in inventory) + (109 in inventory))
        return count_high_jumps(inventory)>=3 and count_quick_runs(inventory)>=3 and count_aerial_dodges(inventory)>=3 and count_glides(inventory)>=3

    @staticmethod
    def need_proof_connection(inventory):
        return 593 in inventory

    @staticmethod
    def need_proof_peace(inventory):
        return 595 in inventory


    @staticmethod
    def count_forms(inventory):
        has_valor = lambda inventory : (26 in inventory)
        has_wisdom = lambda inventory : (27 in inventory)
        has_limit = lambda inventory : (563 in inventory)
        has_master = lambda inventory : (31 in inventory)
        has_final = lambda inventory : (29 in inventory)
        return (has_valor(inventory) + has_wisdom(inventory) + has_limit(inventory) + has_master(inventory) + has_final(inventory))

    @staticmethod
    def need_forms(inventory):
        return ItemPlacementHelpers.count_forms(inventory)==5

    @staticmethod
    def need_summons(inventory):
        return (159 in inventory) and (160 in inventory) and (25 in inventory) and (383 in inventory)

    @staticmethod
    def need_1_page(inventory):
        count_pages = lambda inventory : inventory.count(32)
        return count_pages(inventory) >= 1
        
    @staticmethod
    def need_2_pages(inventory):
        count_pages = lambda inventory : inventory.count(32)
        return count_pages(inventory) >= 2

    @staticmethod
    def need_3_pages(inventory):
        count_pages = lambda inventory : inventory.count(32)
        return count_pages(inventory) >= 3

    @staticmethod
    def need_4_pages(inventory):
        count_pages = lambda inventory : inventory.count(32)
        return count_pages(inventory) >= 4

    @staticmethod
    def need_5_pages(inventory):
        count_pages = lambda inventory : inventory.count(32)
        return count_pages(inventory) == 5

    @staticmethod
    def need_proofs(inventory):
        return (593 in inventory) and (594 in inventory) and (595 in inventory)

        
    @staticmethod
    def make_form_lambda(form_id,form_level):
        has_valor = lambda inventory : (26 in inventory)
        has_wisdom = lambda inventory : (27 in inventory)
        has_limit = lambda inventory : (563 in inventory)
        has_master = lambda inventory : (31 in inventory)
        has_final = lambda inventory : (29 in inventory)
        if form_id=="Valor":
            return lambda inventory : has_valor(inventory) and ItemPlacementHelpers.count_forms(inventory)>=form_level-2
        if form_id=="Wisdom":
            return lambda inventory : has_wisdom(inventory) and ItemPlacementHelpers.count_forms(inventory)>=form_level-2
        if form_id=="Limit":
            return lambda inventory : has_limit(inventory) and ItemPlacementHelpers.count_forms(inventory)>=form_level-2
        if form_id=="Master":
            return lambda inventory : has_master(inventory) and ItemPlacementHelpers.count_forms(inventory)>=form_level-2
        if form_id=="Final":
            return lambda inventory : has_final(inventory) and ItemPlacementHelpers.count_forms(inventory)>=form_level-2

        return lambda inventory : False

    @staticmethod
    def make_form_lambda_nightmare(form_id,form_level):
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
        count_auto_forms = lambda inventory : (has_auto_valor(inventory) + has_auto_wisdom(inventory) + has_auto_limit(inventory) + has_auto_master(inventory) )
        final_possible_but_not_obtained = lambda inventory : (has_valor(inventory) or has_wisdom(inventory) or has_limit(inventory) or has_master(inventory) or count_auto_forms(inventory)>=1) and not has_final(inventory)
        form_level_obtainable = lambda inventory : ItemPlacementHelpers.count_forms(inventory) + (1 if final_possible_but_not_obtained(inventory) else 0) + 2

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

    @staticmethod
    def auron_check(inventory):
        return 54 in inventory
    @staticmethod
    def mulan_check(inventory):
        return 55 in inventory
    @staticmethod
    def beast_check(inventory):
        return 59 in inventory
    @staticmethod
    def jack_ht_check(inventory):
        return 60 in inventory
    @staticmethod
    def simba_check(inventory):
        return 61 in inventory
    @staticmethod
    def jack_pr_check(inventory):
        return 62 in inventory
    @staticmethod
    def aladdin_check(inventory):
        return 72 in inventory
    @staticmethod
    def riku_check(inventory):
        return 73 in inventory
    @staticmethod
    def tron_check(inventory):
        return 74 in inventory
    @staticmethod
    def tt2_check(inventory):
        return 376 in inventory # Picture
    @staticmethod
    def tt3_check(inventory):
        return 375 in inventory # Ice Cream
    @staticmethod
    def hb_check(inventory):
        return 369 in inventory # Membership Card