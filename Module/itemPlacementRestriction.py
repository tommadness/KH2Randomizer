from Class.itemClass import KH2Item
from List.inventory import ability, form, growth, magic, misc, proof, storyunlock, summon, synth
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
    def make_form_lambda(drive_form: DriveForm, form_level: int) -> RequirementFunction:
        if drive_form == form.ValorForm:
            return lambda inventory: ItemPlacementHelpers.has_valor_form(inventory) \
                                     and ItemPlacementHelpers.count_forms(inventory) >= form_level - 2
        if drive_form == form.WisdomForm:
            return lambda inventory: ItemPlacementHelpers.has_wisdom_form(inventory) \
                                     and ItemPlacementHelpers.count_forms(inventory) >= form_level - 2
        if drive_form == form.LimitForm:
            return lambda inventory: ItemPlacementHelpers.has_limit_form(inventory) \
                                     and ItemPlacementHelpers.count_forms(inventory) >= form_level - 2
        if drive_form == form.MasterForm:
            return lambda inventory: ItemPlacementHelpers.has_master_form(inventory) \
                                     and ItemPlacementHelpers.count_forms(inventory) >= form_level - 2
        if drive_form == form.FinalForm:
            return lambda inventory: ItemPlacementHelpers.has_final_form(inventory) \
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
                                     and max_form_level(inventory) >= form_level
        if drive_form == form.WisdomForm:
            return lambda inventory: (ItemPlacementHelpers.has_wisdom_form(inventory)
                                      or ItemPlacementHelpers.has_auto_wisdom(inventory)) \
                                     and max_form_level(inventory) >= form_level
        if drive_form == form.LimitForm:
            return lambda inventory: (ItemPlacementHelpers.has_limit_form(inventory)
                                      or ItemPlacementHelpers.has_auto_limit(inventory)) \
                                     and max_form_level(inventory) >= form_level
        if drive_form == form.MasterForm:
            return lambda inventory: (ItemPlacementHelpers.has_master_form(inventory)
                                      or ItemPlacementHelpers.has_auto_master(inventory)) \
                                     and max_form_level(inventory) >= form_level
        if drive_form == form.FinalForm:
            def have_final_form(inventory: list[int]) -> bool:
                return ItemPlacementHelpers.has_final_form(inventory) or final_possible_but_not_obtained(inventory)

            if form_level == 2:
                return lambda inventory: have_final_form(inventory) or ItemPlacementHelpers.has_auto_final(inventory)
            else:
                return lambda inventory: have_final_form(inventory) and max_form_level(inventory) >= form_level

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
                                     and max_form_level(inventory) >= form_level
        if drive_form == form.WisdomForm:
            return lambda inventory: (ItemPlacementHelpers.has_wisdom_form(inventory)
                                      or ItemPlacementHelpers.has_auto_wisdom(inventory)) \
                                     and max_form_level(inventory) >= form_level
        if drive_form == form.LimitForm:
            return lambda inventory: (ItemPlacementHelpers.has_limit_form(inventory)
                                      or ItemPlacementHelpers.has_auto_limit(inventory)) \
                                     and max_form_level(inventory) >= form_level
        if drive_form == form.MasterForm:
            return lambda inventory: (ItemPlacementHelpers.has_master_form(inventory)
                                      or ItemPlacementHelpers.has_auto_master(inventory)) \
                                     and max_form_level(inventory) >= form_level
        if drive_form == form.FinalForm:
            def have_final_form(inventory: list[int]) -> bool:
                return final_possible_but_not_obtained(inventory) or ItemPlacementHelpers.has_final_form(inventory)

            if form_level == 2:
                return lambda inventory: have_final_form(inventory) or ItemPlacementHelpers.has_auto_final(inventory)
            else:
                return lambda inventory: have_final_form(inventory) and max_form_level(inventory) >= form_level

        return lambda inventory: False

    @staticmethod
    def auron_check(inventory: list[int]) -> bool:
        return storyunlock.BattlefieldsOfWar.id in inventory

    @staticmethod
    def mulan_check(inventory: list[int]) -> bool:
        return storyunlock.SwordOfTheAncestor.id in inventory

    @staticmethod
    def beast_check(inventory: list[int]) -> bool:
        return storyunlock.BeastsClaw.id in inventory

    @staticmethod
    def jack_ht_check(inventory: list[int]) -> bool:
        return storyunlock.BoneFist.id in inventory

    @staticmethod
    def simba_check(inventory: list[int]) -> bool:
        return storyunlock.ProudFang.id in inventory

    @staticmethod
    def jack_pr_check(inventory: list[int]) -> bool:
        return storyunlock.SkillAndCrossbones.id in inventory

    @staticmethod
    def aladdin_check(inventory: list[int]) -> bool:
        return storyunlock.Scimitar.id in inventory

    # @staticmethod
    # def riku_check(inventory: list[int]) -> bool:
    #     return storyunlock.WayToTheDawn.id in inventory

    @staticmethod
    def tron_check(inventory: list[int]) -> bool:
        return storyunlock.IdentityDisk.id in inventory

    @staticmethod
    def tt2_check(inventory: list[int]) -> bool:
        return storyunlock.Picture.id in inventory

    @staticmethod
    def tt3_check(inventory: list[int]) -> bool:
        return storyunlock.Picture.id in inventory and storyunlock.IceCream.id in inventory

    @staticmethod
    def hb_check(inventory: list[int]) -> bool:
        return storyunlock.MembershipCard.id in inventory

    @staticmethod
    def make_synth_requirement(synth_item: KH2Item) -> RequirementFunction:
        # making lambdas for the different synth items
        default_access_lambda: RequirementFunction = lambda inventory: True
        synth_req_map: dict[InventoryItem, RequirementFunction] = {
            # TR access, so free
            synth.BlazingShard: default_access_lambda,

            synth.BlazingStone: lambda inv: ItemPlacementHelpers.mulan_check(inv) \
                                               or ItemPlacementHelpers.tron_check(inv) \
                                               or ItemPlacementHelpers.auron_check(inv),

            # AG 1 and 2 both have these, so no requirement needed
            synth.BlazingGem: default_access_lambda,

            synth.BlazingCrystal: lambda inv: ItemPlacementHelpers.auron_check(inv) \
                                                 or ItemPlacementHelpers.hb_check(inv) \
                                                 or ItemPlacementHelpers.beast_check(inv) \
                                                 or ItemPlacementHelpers.aladdin_check(inv),

            # shadows are always available in DC/TR
            synth.DarkShard: default_access_lambda,

            # LoD1 and 2 both have them
            synth.DarkStone: default_access_lambda,

            # BC1 and 2 have them
            synth.DarkGem: default_access_lambda,

            # PR1 has them, but could be locked out
            synth.DarkCrystal: lambda inv: ItemPlacementHelpers.mulan_check(inv),

            # TWTNW has them post Xemnas
            synth.DenseShard: default_access_lambda,

            # TWTNW has them post Xemnas
            synth.DenseStone: default_access_lambda,

            # TWTNW has them post Xemnas
            synth.DenseGem: default_access_lambda,

            # TWTNW has them post Xemnas
            synth.DenseCrystal: default_access_lambda,

            # BC ones can disappear
            synth.FrostShard: lambda inv: ItemPlacementHelpers.mulan_check(inv) \
                                             or ItemPlacementHelpers.aladdin_check(inv) \
                                             or ItemPlacementHelpers.jack_pr_check(inv),

            # TR is always available
            synth.FrostStone: default_access_lambda,

            # AG1 and 2 both have them
            synth.FrostGem: default_access_lambda,

            # PL1 and 2 both have them
            synth.FrostCrystal: default_access_lambda,

            # LoD1 and 2 both have them
            synth.LightningShard: default_access_lambda,

            # HT and SP ones can become unavailable
            synth.LightningStone: lambda inv: ItemPlacementHelpers.auron_check(inv) \
                                                 or ItemPlacementHelpers.mulan_check(inv) \
                                                 or ItemPlacementHelpers.aladdin_check(inv),

            synth.LightningGem: lambda inv: ItemPlacementHelpers.hb_check(inv) \
                                               or ItemPlacementHelpers.beast_check(inv) \
                                               or ItemPlacementHelpers.jack_pr_check(inv) \
                                               or ItemPlacementHelpers.jack_ht_check(inv) \
                                               or ItemPlacementHelpers.simba_check(inv) \
                                               or ItemPlacementHelpers.tron_check(inv),

            # SP1 and 2 both have them
            synth.LightningCrystal: default_access_lambda,

            # OC1 can be locked out
            synth.LucidShard: lambda inv: ItemPlacementHelpers.jack_pr_check(inv) \
                                             or ItemPlacementHelpers.jack_ht_check(inv),

            # HT1 and 2 have them
            synth.LucidStone: default_access_lambda,

            # SP1 and 2 both have them
            synth.LucidGem: default_access_lambda,

            synth.LucidCrystal: lambda inv: ItemPlacementHelpers.mulan_check(inv) \
                                               or ItemPlacementHelpers.beast_check(inv) \
                                               or ItemPlacementHelpers.auron_check(inv) \
                                               or ItemPlacementHelpers.jack_pr_check(inv) \
                                               or ItemPlacementHelpers.aladdin_check(inv) \
                                               or ItemPlacementHelpers.jack_ht_check(inv) \
                                               or ItemPlacementHelpers.simba_check(inv) \
                                               or ItemPlacementHelpers.hb_check(inv),

            # BC1 and 2 both have them, also TR
            synth.PowerShard: default_access_lambda,

            # AG1 and 2 both have them
            synth.PowerStone: default_access_lambda,

            # PL1 and 2 both have them
            synth.PowerGem: default_access_lambda,

            synth.PowerCrystal: lambda inv: ItemPlacementHelpers.hb_check(inv) \
                                               or ItemPlacementHelpers.beast_check(inv) \
                                               or ItemPlacementHelpers.auron_check(inv) \
                                               or ItemPlacementHelpers.jack_pr_check(inv),

            # TWTNW always has them in Luxord and Saix rooms
            synth.TwilightShard: default_access_lambda,

            # TWTNW always has them
            synth.TwilightStone: default_access_lambda,

            # TWTNW always has them
            synth.TwilightGem: default_access_lambda,

            # TWTNW always has them
            synth.TwilightCrystal: default_access_lambda,
        }

        item = synth_item.item
        if item in synth_req_map:
            return synth_req_map[item]

        # default returned lambda, doesn't allow for acquiring the item, failsafe
        return lambda inventory: False
