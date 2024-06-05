from Class.itemClass import KH2Item
from List.inventory import ability, form, growth, magic, misc, proof, storyunlock, summon, synth, keyblade
from List.inventory.form import DriveForm
from List.inventory.growth import GrowthType
from List.inventory.item import InventoryItem
from List.location.graph import RequirementFunction


class ItemPlacementHelpers:

    @staticmethod
    def need_fire_blizzard_thunder(inventory: list[int]) -> bool:
        return magic.Fire.id in inventory and magic.Blizzard.id in inventory and magic.Thunder.id in inventory

    @staticmethod
    def need_1_magnet(inventory: list[int]) -> bool:
        return inventory.count(magic.Magnet.id) >= 1

    @staticmethod
    def need_2_magnet(inventory: list[int]) -> bool:
        return inventory.count(magic.Magnet.id) >= 2

    @staticmethod
    def need_3_thunders(inventory: list[int]) -> bool:
        return inventory.count(magic.Thunder.id) == 3

    @staticmethod
    def count_growth(inventory: list[int], growth_type: GrowthType) -> int:
        ids = [item.id for item in growth.all_growth() if item.growth_type == growth_type]
        count = 0
        for item in inventory:
            if item in ids:
                count += 1
        return count

    @staticmethod
    def need_growths(inventory: list[int]) -> bool:
        return ItemPlacementHelpers.count_growth(inventory, GrowthType.HIGH_JUMP) >= 3 \
            and ItemPlacementHelpers.count_growth(inventory, GrowthType.QUICK_RUN) >= 3 \
            and ItemPlacementHelpers.count_growth(inventory, GrowthType.AERIAL_DODGE) >= 3 \
            and ItemPlacementHelpers.count_growth(inventory, GrowthType.GLIDE) >= 3

    @staticmethod
    def need_proof_connection(inventory: list[int]) -> bool:
        return proof.ProofOfConnection.id in inventory

    @staticmethod
    def need_proof_peace(inventory: list[int]) -> bool:
        return proof.ProofOfPeace.id in inventory

    @staticmethod
    def has_valor_form(inventory: list[int]) -> bool:
        return form.ValorForm.id in inventory

    @staticmethod
    def has_wisdom_form(inventory: list[int]) -> bool:
        return form.WisdomForm.id in inventory

    @staticmethod
    def has_limit_form(inventory: list[int]) -> bool:
        return form.LimitForm.id in inventory

    @staticmethod
    def has_master_form(inventory: list[int]) -> bool:
        return form.MasterForm.id in inventory

    @staticmethod
    def has_final_form(inventory: list[int]) -> bool:
        return form.FinalForm.id in inventory
    
    @staticmethod
    def can_level_valor(inventory: list[int]) -> bool:
        return True
    @staticmethod
    def can_level_wisdom(inventory: list[int]) -> bool:
        return True
    @staticmethod
    def can_level_limit(inventory: list[int]) -> bool:
        return True
    @staticmethod
    def can_level_master(inventory: list[int]) -> bool:
        return ItemPlacementHelpers.ht1_check(inventory) \
              or ItemPlacementHelpers.hb2_check(inventory)
    @staticmethod
    def can_level_final(inventory: list[int]) -> bool:
        return ItemPlacementHelpers.twtnw_roxas_check(inventory) \
              or ItemPlacementHelpers.pr2_check(inventory) \
              or ItemPlacementHelpers.bc2_check(inventory) \
              or ItemPlacementHelpers.lod2_check(inventory) \
              or ItemPlacementHelpers.tt3_check(inventory)

    @staticmethod
    def has_auto_valor(inventory: list[int]) -> bool:
        return ability.AutoValor.id in inventory

    @staticmethod
    def has_auto_wisdom(inventory: list[int]) -> bool:
        return ability.AutoWisdom.id in inventory

    @staticmethod
    def has_auto_limit(inventory: list[int]) -> bool:
        return ability.AutoLimitForm.id in inventory

    @staticmethod
    def has_auto_master(inventory: list[int]) -> bool:
        return ability.AutoMaster.id in inventory

    @staticmethod
    def has_auto_final(inventory: list[int]) -> bool:
        return ability.AutoFinal.id in inventory

    @staticmethod
    def count_forms(inventory: list[int]) -> int:
        count = 0
        if ItemPlacementHelpers.has_valor_form(inventory):
            count += 1
        if ItemPlacementHelpers.has_wisdom_form(inventory):
            count += 1
        if ItemPlacementHelpers.has_limit_form(inventory):
            count += 1
        if ItemPlacementHelpers.has_master_form(inventory):
            count += 1
        if ItemPlacementHelpers.has_final_form(inventory):
            count += 1
        return count

    @staticmethod
    def need_forms(inventory: list[int]) -> bool:
        return ItemPlacementHelpers.count_forms(inventory) == 5

    @staticmethod
    def need_summons(inventory: list[int]) -> bool:
        return summon.LampCharm.id in inventory \
            and summon.FeatherCharm.id in inventory \
            and summon.UkuleleCharm.id in inventory \
            and summon.BaseballCharm.id in inventory

    @staticmethod
    def count_pages(inventory: list[int]) -> int:
        return inventory.count(misc.TornPages.id)

    @staticmethod
    def need_torn_pages(count: int) -> RequirementFunction:
        return lambda inventory: ItemPlacementHelpers.count_pages(inventory) >= count

    @staticmethod
    def need_proofs(inventory: list[int]) -> bool:
        return proof.ProofOfConnection.id in inventory \
            and proof.ProofOfNonexistence.id in inventory \
            and proof.ProofOfPeace.id in inventory
    
    @staticmethod
    def need_promise_charm(inventory: list[int]) -> bool:
        return misc.PromiseCharm.id in inventory
    
    @staticmethod
    def make_need_objectives_lambda(num_objectives_needed: int):
        return lambda inventory : inventory.count(misc.ObjectiveItem.id) >= num_objectives_needed        

    @staticmethod
    def make_form_lambda(drive_form: DriveForm, form_level: int) -> RequirementFunction:
        if drive_form == form.ValorForm:
            return lambda inventory: ItemPlacementHelpers.has_valor_form(inventory) \
                                     and ItemPlacementHelpers.can_level_valor(inventory) \
                                     and ItemPlacementHelpers.count_forms(inventory) >= form_level - 2
        if drive_form == form.WisdomForm:
            return lambda inventory: ItemPlacementHelpers.has_wisdom_form(inventory) \
                                     and ItemPlacementHelpers.can_level_wisdom(inventory) \
                                     and ItemPlacementHelpers.count_forms(inventory) >= form_level - 2
        if drive_form == form.LimitForm:
            return lambda inventory: ItemPlacementHelpers.has_limit_form(inventory) \
                                     and ItemPlacementHelpers.can_level_limit(inventory) \
                                     and ItemPlacementHelpers.count_forms(inventory) >= form_level - 2
        if drive_form == form.MasterForm:
            return lambda inventory: ItemPlacementHelpers.has_master_form(inventory) \
                                     and ItemPlacementHelpers.can_level_master(inventory) \
                                     and ItemPlacementHelpers.count_forms(inventory) >= form_level - 2
        if drive_form == form.FinalForm:
            return lambda inventory: ItemPlacementHelpers.has_final_form(inventory) \
                                     and ItemPlacementHelpers.can_level_final(inventory) \
                                     and ItemPlacementHelpers.count_forms(inventory) >= form_level - 2
        return lambda inventory: False

    @staticmethod
    def make_form_lambda_nightmare(drive_form: DriveForm, form_level: int) -> RequirementFunction:
        def count_auto_forms(inventory: list[int]) -> int:
            count = 0
            if ItemPlacementHelpers.has_auto_valor(inventory):
                count += 1
            if ItemPlacementHelpers.has_auto_wisdom(inventory):
                count += 1
            if ItemPlacementHelpers.has_auto_limit(inventory):
                count += 1
            if ItemPlacementHelpers.has_auto_master(inventory):
                count += 1
            return count

        def final_possible_but_not_obtained(inventory: list[int]) -> bool:
            return (ItemPlacementHelpers.has_valor_form(inventory)
                    or ItemPlacementHelpers.has_wisdom_form(inventory)
                    or ItemPlacementHelpers.has_limit_form(inventory)
                    or ItemPlacementHelpers.has_master_form(inventory)
                    or count_auto_forms(inventory) >= 1) \
                and not ItemPlacementHelpers.has_final_form(inventory)

        def max_form_level(inventory: list[int]) -> int:
            base_count = ItemPlacementHelpers.count_forms(inventory) + 2
            if final_possible_but_not_obtained(inventory):
                return base_count + 1
            else:
                return base_count

        if drive_form == form.ValorForm:
            return lambda inventory: (ItemPlacementHelpers.has_valor_form(inventory)
                                      or ItemPlacementHelpers.has_auto_valor(inventory)) \
                                     and ItemPlacementHelpers.can_level_valor(inventory) \
                                     and max_form_level(inventory) >= form_level
        if drive_form == form.WisdomForm:
            return lambda inventory: (ItemPlacementHelpers.has_wisdom_form(inventory)
                                      or ItemPlacementHelpers.has_auto_wisdom(inventory)) \
                                     and ItemPlacementHelpers.can_level_wisdom(inventory) \
                                     and max_form_level(inventory) >= form_level
        if drive_form == form.LimitForm:
            return lambda inventory: (ItemPlacementHelpers.has_limit_form(inventory)
                                      or ItemPlacementHelpers.has_auto_limit(inventory)) \
                                     and ItemPlacementHelpers.can_level_limit(inventory) \
                                     and max_form_level(inventory) >= form_level
        if drive_form == form.MasterForm:
            return lambda inventory: (ItemPlacementHelpers.has_master_form(inventory)
                                      or ItemPlacementHelpers.has_auto_master(inventory)) \
                                     and ItemPlacementHelpers.can_level_master(inventory) \
                                     and max_form_level(inventory) >= form_level
        if drive_form == form.FinalForm:
            def have_final_form(inventory: list[int]) -> bool:
                return ItemPlacementHelpers.has_final_form(inventory) or final_possible_but_not_obtained(inventory)

            if form_level == 2:
                return lambda inventory: (have_final_form(inventory) or ItemPlacementHelpers.has_auto_final(inventory)) \
                                     and ItemPlacementHelpers.can_level_final(inventory)
            else:
                return lambda inventory: have_final_form(inventory) \
                                     and max_form_level(inventory) >= form_level \
                                     and ItemPlacementHelpers.can_level_final(inventory)

        return lambda inventory: False


    @staticmethod
    def make_form_lambda_nightmare_no_anti(drive_form: DriveForm, form_level: int) -> RequirementFunction:
        def max_form_level(inventory: list[int]) -> int:
            base_count = ItemPlacementHelpers.count_forms(inventory) + 2
            return base_count

        if drive_form == form.ValorForm:
            return lambda inventory: (ItemPlacementHelpers.has_valor_form(inventory)
                                      or ItemPlacementHelpers.has_auto_valor(inventory)) \
                                     and ItemPlacementHelpers.can_level_valor(inventory) \
                                     and max_form_level(inventory) >= form_level
        if drive_form == form.WisdomForm:
            return lambda inventory: (ItemPlacementHelpers.has_wisdom_form(inventory)
                                      or ItemPlacementHelpers.has_auto_wisdom(inventory)) \
                                     and ItemPlacementHelpers.can_level_wisdom(inventory) \
                                     and max_form_level(inventory) >= form_level
        if drive_form == form.LimitForm:
            return lambda inventory: (ItemPlacementHelpers.has_limit_form(inventory)
                                      or ItemPlacementHelpers.has_auto_limit(inventory)) \
                                     and ItemPlacementHelpers.can_level_limit(inventory) \
                                     and max_form_level(inventory) >= form_level
        if drive_form == form.MasterForm:
            return lambda inventory: (ItemPlacementHelpers.has_master_form(inventory)
                                      or ItemPlacementHelpers.has_auto_master(inventory)) \
                                     and ItemPlacementHelpers.can_level_master(inventory) \
                                     and max_form_level(inventory) >= form_level
        if drive_form == form.FinalForm:
            return lambda inventory: (ItemPlacementHelpers.has_final_form(inventory)
                                      or ItemPlacementHelpers.has_auto_final(inventory)) \
                                     and ItemPlacementHelpers.can_level_final(inventory) \
                                     and max_form_level(inventory) >= form_level

        return lambda inventory: False

    @staticmethod
    def make_form_lambda_nightmare_no_final(drive_form: DriveForm, form_level: int) -> RequirementFunction:
        def final_possible_but_not_obtained(_: list[int]) -> bool:
            return False

        def max_form_level(inventory: list[int]) -> int:
            base_count = ItemPlacementHelpers.count_forms(inventory) + 2
            if final_possible_but_not_obtained(inventory):
                return base_count + 1
            else:
                return base_count

        if drive_form == form.ValorForm:
            return lambda inventory: (ItemPlacementHelpers.has_valor_form(inventory)
                                      or ItemPlacementHelpers.has_auto_valor(inventory)) \
                                     and ItemPlacementHelpers.can_level_valor(inventory) \
                                     and max_form_level(inventory) >= form_level
        if drive_form == form.WisdomForm:
            return lambda inventory: (ItemPlacementHelpers.has_wisdom_form(inventory)
                                      or ItemPlacementHelpers.has_auto_wisdom(inventory)) \
                                     and ItemPlacementHelpers.can_level_wisdom(inventory) \
                                     and max_form_level(inventory) >= form_level
        if drive_form == form.LimitForm:
            return lambda inventory: (ItemPlacementHelpers.has_limit_form(inventory)
                                      or ItemPlacementHelpers.has_auto_limit(inventory)) \
                                     and ItemPlacementHelpers.can_level_limit(inventory) \
                                     and max_form_level(inventory) >= form_level
        if drive_form == form.MasterForm:
            return lambda inventory: (ItemPlacementHelpers.has_master_form(inventory)
                                      or ItemPlacementHelpers.has_auto_master(inventory)) \
                                     and ItemPlacementHelpers.can_level_master(inventory) \
                                     and max_form_level(inventory) >= form_level
        if drive_form == form.FinalForm:
            def have_final_form(inventory: list[int]) -> bool:
                return final_possible_but_not_obtained(inventory) or ItemPlacementHelpers.has_final_form(inventory)

            if form_level == 2:
                return lambda inventory: (have_final_form(inventory) or ItemPlacementHelpers.has_auto_final(inventory)) \
                                     and ItemPlacementHelpers.can_level_final(inventory)
            else:
                return lambda inventory: have_final_form(inventory) and max_form_level(inventory) >= form_level \
                                     and ItemPlacementHelpers.can_level_final(inventory)

        return lambda inventory: False

    @staticmethod
    def get_number_visit_unlocks(inventory: list[int]) -> int:
        visit_unlock_ids = [u.id for u in storyunlock.all_story_unlocks()]
        running_total = 0
        for id in visit_unlock_ids:
            running_total+=inventory.count(id)
        return running_total

    @staticmethod
    def make_level_group_check(group_index) -> RequirementFunction:
        thresholds = [1,3,6,9,12,15,18,21,24] # modified from AP so that max level could in theory have a visit unlock
        if group_index<len(thresholds):
            return lambda inv: ItemPlacementHelpers.get_number_visit_unlocks(inv) >= thresholds[group_index]
        else:
            return lambda inv: ItemPlacementHelpers.get_number_visit_unlocks(inv) >= thresholds[-1]


    @staticmethod
    def stt_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.NaminesSketches.id)==1
    
    @staticmethod
    def dc1_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.RoyalSummons.id)>=1

    @staticmethod
    def dc2_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.RoyalSummons.id)==2

    @staticmethod
    def oc1_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.BattlefieldsOfWar.id)>=1

    @staticmethod
    def oc2_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.BattlefieldsOfWar.id)==2

    @staticmethod
    def lod1_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.SwordOfTheAncestor.id)>=1
    
    @staticmethod
    def lod2_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.SwordOfTheAncestor.id)==2

    @staticmethod
    def bc1_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.BeastsClaw.id)>=1
    
    @staticmethod
    def bc2_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.BeastsClaw.id)==2

    @staticmethod
    def ht1_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.BoneFist.id)>=1
    
    @staticmethod
    def ht2_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.BoneFist.id)==2

    @staticmethod
    def pl1_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.ProudFang.id)>=1
    
    @staticmethod
    def pl2_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.ProudFang.id)==2
    
    @staticmethod
    def pr1_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.SkillAndCrossbones.id)>=1

    @staticmethod
    def pr2_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.SkillAndCrossbones.id)==2

    @staticmethod
    def ag1_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.Scimitar.id)>=1

    @staticmethod
    def ag2_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.Scimitar.id)==2

    @staticmethod
    def twtnw_roxas_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.WayToTheDawn.id) >= 1
    
    @staticmethod
    def twtnw_post_saix_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.WayToTheDawn.id) == 2

    @staticmethod
    def sp1_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.IdentityDisk.id)>=1
    
    @staticmethod
    def sp2_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.IdentityDisk.id) == 2

    @staticmethod
    def tt1_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.IceCream.id) >= 1

    @staticmethod
    def tt2_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.IceCream.id) >= 2

    @staticmethod
    def tt3_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.IceCream.id) == 3

    @staticmethod
    def hb1_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.MembershipCard.id) >= 1

    @staticmethod
    def hb2_check(inventory: list[int]) -> bool:
        return inventory.count(storyunlock.MembershipCard.id) == 2

    @staticmethod
    def make_synth_requirement(synth_item: KH2Item) -> RequirementFunction:
        # making lambdas for the different synth items
        default_access_lambda: RequirementFunction = lambda inventory: True
        synth_req_map: dict[InventoryItem, RequirementFunction] = {
            synth.BlazingShard: lambda inv: ItemPlacementHelpers.dc2_check(inv) \
                                               or ItemPlacementHelpers.bc2_check(inv) \
                                               or ItemPlacementHelpers.oc2_check(inv),

            synth.BlazingStone: lambda inv: ItemPlacementHelpers.lod2_check(inv) \
                                               or ItemPlacementHelpers.sp2_check(inv) \
                                               or ItemPlacementHelpers.oc2_check(inv),

            synth.BlazingGem: ItemPlacementHelpers.ag1_check,

            synth.BlazingCrystal: lambda inv: ItemPlacementHelpers.oc2_check(inv) \
                                                 or ItemPlacementHelpers.hb2_check(inv) \
                                                 or ItemPlacementHelpers.bc2_check(inv) \
                                                 or ItemPlacementHelpers.ag2_check(inv),

            # shadows are guaranteed anytime in DC/TR
            synth.DarkShard: ItemPlacementHelpers.dc1_check,

            # LoD1 and 2 both have them
            synth.DarkStone: ItemPlacementHelpers.lod1_check,

            # BC1 and 2 have them
            synth.DarkGem: ItemPlacementHelpers.bc1_check,

            # PR1 has them, but could be locked out
            synth.DarkCrystal: lambda inv: ItemPlacementHelpers.lod2_check(inv),

            # TWTNW has them post Xemnas
            synth.DenseShard: lambda inv: ItemPlacementHelpers.twtnw_post_saix_check(inv) \
                                            or ItemPlacementHelpers.bc2_check(inv) \
                                            or ItemPlacementHelpers.tt3_check(inv),

            # TWTNW has them post Xemnas
            synth.DenseStone: lambda inv: ItemPlacementHelpers.lod2_check(inv) \
                                            or ItemPlacementHelpers.twtnw_roxas_check(inv),

            # TWTNW has them post Xemnas
            synth.DenseGem: lambda inv: ItemPlacementHelpers.tt3_check(inv) \
                                            or ItemPlacementHelpers.stt_check(inv) \
                                            or ItemPlacementHelpers.twtnw_roxas_check(inv),

            # TWTNW has them post Xemnas
            synth.DenseCrystal:  lambda inv: ItemPlacementHelpers.tt3_check(inv) \
                                            or ItemPlacementHelpers.twtnw_roxas_check(inv) \
                                            or ItemPlacementHelpers.pl2_check(inv),

            # BC ones can disappear
            synth.FrostShard: lambda inv: ItemPlacementHelpers.lod2_check(inv) \
                                             or ItemPlacementHelpers.ag2_check(inv) \
                                             or ItemPlacementHelpers.pr2_check(inv),

            # DC/TR
            synth.FrostStone: ItemPlacementHelpers.dc2_check,

            # AG1 and 2 both have them
            synth.FrostGem: ItemPlacementHelpers.ag1_check,

            # PL1 and 2 both have them
            synth.FrostCrystal: ItemPlacementHelpers.pl1_check,

            # LoD1 and 2 both have them
            synth.LightningShard: lambda inv: ItemPlacementHelpers.lod1_check(inv) \
                                                or ItemPlacementHelpers.dc1_check(inv) \
                                                or ItemPlacementHelpers.pl2_check(inv) \
                                                or ItemPlacementHelpers.pr2_check(inv) \
                                                or ItemPlacementHelpers.ag2_check(inv),

            # HT and SP ones can become unavailable
            synth.LightningStone: lambda inv: ItemPlacementHelpers.oc2_check(inv) \
                                                 or ItemPlacementHelpers.lod2_check(inv) \
                                                 or ItemPlacementHelpers.ag2_check(inv),

            synth.LightningGem: lambda inv: ItemPlacementHelpers.hb2_check(inv) \
                                               or ItemPlacementHelpers.bc2_check(inv) \
                                               or ItemPlacementHelpers.pr2_check(inv) \
                                               or ItemPlacementHelpers.ht2_check(inv) \
                                               or ItemPlacementHelpers.pl2_check(inv) \
                                               or ItemPlacementHelpers.sp2_check(inv),

            # SP1 and 2 both have them
            synth.LightningCrystal: ItemPlacementHelpers.sp1_check,

            # OC1 can be locked out
            synth.LucidShard: lambda inv: ItemPlacementHelpers.pr2_check(inv) \
                                             or ItemPlacementHelpers.ht2_check(inv),

            # HT1 and 2 have them
            synth.LucidStone: ItemPlacementHelpers.ht1_check,

            # SP1 and 2 both have them
            synth.LucidGem: lambda inv: ItemPlacementHelpers.hb2_check(inv) \
                                            or ItemPlacementHelpers.sp1_check(inv),

            synth.LucidCrystal: lambda inv: ItemPlacementHelpers.lod2_check(inv) \
                                               or ItemPlacementHelpers.bc2_check(inv) \
                                               or ItemPlacementHelpers.oc2_check(inv) \
                                               or ItemPlacementHelpers.pr2_check(inv) \
                                               or ItemPlacementHelpers.ag2_check(inv) \
                                               or ItemPlacementHelpers.ht2_check(inv) \
                                               or ItemPlacementHelpers.pl2_check(inv) \
                                               or ItemPlacementHelpers.hb2_check(inv),

            # BC1 and 2 both have them, also TR
            synth.PowerShard: lambda inv: ItemPlacementHelpers.bc1_check(inv)\
                                          or ItemPlacementHelpers.dc2_check(inv)\
                                          or ItemPlacementHelpers.ht2_check(inv),

            # AG1 and 2 both have them
            synth.PowerStone: ItemPlacementHelpers.ag1_check,

            # PL1 and 2 both have them
            synth.PowerGem: ItemPlacementHelpers.pl1_check,

            synth.PowerCrystal: lambda inv: ItemPlacementHelpers.hb2_check(inv) \
                                               or ItemPlacementHelpers.bc2_check(inv) \
                                               or ItemPlacementHelpers.oc2_check(inv) \
                                               or ItemPlacementHelpers.pr2_check(inv),

            # TWTNW always has them in Luxord and Saix rooms
            synth.TwilightShard: lambda inv: ItemPlacementHelpers.twtnw_roxas_check(inv)\
                                                or ItemPlacementHelpers.pr2_check(inv)\
                                                or ItemPlacementHelpers.tt3_check(inv)\
                                                or ItemPlacementHelpers.lod2_check(inv),

            # TWTNW always has them
            synth.TwilightStone: lambda inv: ItemPlacementHelpers.tt3_check(inv)\
                                                or ItemPlacementHelpers.twtnw_roxas_check(inv)\
                                                or ItemPlacementHelpers.hb2_check(inv),

            # TWTNW always has them
            synth.TwilightGem: lambda inv: ItemPlacementHelpers.twtnw_roxas_check(inv)\
                                            or ItemPlacementHelpers.tt3_check(inv),

            # TWTNW always has them
            synth.TwilightCrystal: ItemPlacementHelpers.twtnw_roxas_check,
        }

        item = synth_item.item
        if item in synth_req_map:
            return synth_req_map[item]

        # default returned lambda, doesn't allow for acquiring the item, failsafe
        return lambda inventory: False

    @staticmethod
    def need_stt_keyblade(inventory: list[int]) -> bool:
        return keyblade.BondOfFlame.id in inventory
    @staticmethod
    def need_tt_keyblade(inventory: list[int]) -> bool:
        return keyblade.Oathkeeper.id in inventory
    @staticmethod
    def need_hb_keyblade(inventory: list[int]) -> bool:
        return keyblade.SleepingLion.id in inventory
    @staticmethod
    def need_cor_keyblade(inventory: list[int]) -> bool:
        return keyblade.WinnersProof.id in inventory
    @staticmethod
    def need_lod_keyblade(inventory: list[int]) -> bool:
        return keyblade.HiddenDragon.id in inventory
    @staticmethod
    def need_bc_keyblade(inventory: list[int]) -> bool:
        return keyblade.RumblingRose.id in inventory
    @staticmethod
    def need_oc_keyblade(inventory: list[int]) -> bool:
        return keyblade.HerosCrest.id in inventory
    @staticmethod
    def need_dc_keyblade(inventory: list[int]) -> bool:
        return keyblade.Monochrome.id in inventory
    @staticmethod
    def need_pr_keyblade(inventory: list[int]) -> bool:
        return keyblade.FollowTheWind.id in inventory
    @staticmethod
    def need_ag_keyblade(inventory: list[int]) -> bool:
        return keyblade.WishingLamp.id in inventory
    @staticmethod
    def need_ht_keyblade(inventory: list[int]) -> bool:
        return keyblade.DecisivePumpkin.id in inventory
    @staticmethod
    def need_pl_keyblade(inventory: list[int]) -> bool:
        return keyblade.CircleOfLife.id in inventory
    @staticmethod
    def need_sp_keyblade(inventory: list[int]) -> bool:
        return keyblade.PhotonDebugger.id in inventory
    @staticmethod
    def need_twtnw_keyblade(inventory: list[int]) -> bool:
        return keyblade.TwoBecomeOne.id in inventory
    @staticmethod
    def need_haw_keyblade(inventory: list[int]) -> bool:
        return keyblade.SweetMemories.id in inventory
