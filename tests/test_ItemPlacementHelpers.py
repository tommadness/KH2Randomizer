import unittest

from List.inventory import magic, growth, proof, form, summon, misc, storyunlock, ability
from Module.itemPlacementRestriction import ItemPlacementHelpers


class Tests(unittest.TestCase):

    def test_need_fire_blizzard_thunder(self):
        inventory = []
        restriction = ItemPlacementHelpers.need_fire_blizzard_thunder
        self.assertFalse(restriction(inventory))

        inventory.append(magic.Fire.id)
        self.assertFalse(restriction(inventory))

        inventory.clear()
        inventory.append(magic.Blizzard.id)
        self.assertFalse(restriction(inventory))

        inventory.clear()
        inventory.append(magic.Thunder.id)
        self.assertFalse(restriction(inventory))

        inventory.append(magic.Fire.id)
        inventory.append(magic.Blizzard.id)
        self.assertTrue(restriction(inventory))

    def test_need_1_magnet(self):
        inventory = []
        restriction = ItemPlacementHelpers.need_1_magnet
        self.assertFalse(restriction(inventory))

        inventory.append(magic.Magnet.id)
        self.assertTrue(restriction(inventory))

        inventory.append(magic.Magnet.id)
        self.assertTrue(restriction(inventory))

        inventory.append(magic.Magnet.id)
        self.assertTrue(restriction(inventory))

    def test_need_2_magnet(self):
        inventory = []
        restriction = ItemPlacementHelpers.need_2_magnet
        self.assertFalse(restriction(inventory))

        inventory.append(magic.Magnet.id)
        self.assertFalse(restriction(inventory))

        inventory.append(magic.Magnet.id)
        self.assertTrue(restriction(inventory))

        inventory.append(magic.Magnet.id)
        self.assertTrue(restriction(inventory))

    def test_need_3_thunder(self):
        inventory = []
        restriction = ItemPlacementHelpers.need_3_thunders
        self.assertFalse(restriction(inventory))

        inventory.append(magic.Thunder.id)
        self.assertFalse(restriction(inventory))

        inventory.append(magic.Thunder.id)
        self.assertFalse(restriction(inventory))

        inventory.append(magic.Thunder.id)
        self.assertTrue(restriction(inventory))

    def test_need_growths(self):
        inventory = []
        restriction = ItemPlacementHelpers.need_growths
        self.assertFalse(restriction(inventory))

        inventory.append(growth.HighJump1.id)
        inventory.append(growth.HighJumpMax.id)
        inventory.append(growth.QuickRun3.id)
        inventory.append(growth.QuickRun2.id)
        inventory.append(growth.AerialDodge1.id)
        inventory.append(growth.AerialDodge2.id)
        inventory.append(growth.GlideMax.id)
        inventory.append(growth.Glide3.id)
        self.assertFalse(restriction(inventory))

        inventory.append(growth.HighJump2.id)
        inventory.append(growth.QuickRun1.id)
        inventory.append(growth.AerialDodgeMax.id)
        self.assertFalse(restriction(inventory))

        inventory.append(growth.Glide2.id)
        self.assertTrue(restriction(inventory))

    def test_need_proof_connection(self):
        inventory = []
        restriction = ItemPlacementHelpers.need_proof_connection
        self.assertFalse(restriction(inventory))

        inventory.append(proof.ProofOfNonexistence.id)
        inventory.append(proof.ProofOfPeace.id)
        self.assertFalse(restriction(inventory))

        inventory.append(proof.ProofOfConnection.id)
        self.assertTrue(restriction(inventory))

    def test_need_proof_peace(self):
        inventory = []
        restriction = ItemPlacementHelpers.need_proof_peace
        self.assertFalse(restriction(inventory))

        inventory.append(proof.ProofOfConnection.id)
        inventory.append(proof.ProofOfNonexistence.id)
        self.assertFalse(restriction(inventory))

        inventory.append(proof.ProofOfPeace.id)
        self.assertTrue(restriction(inventory))

    def test_need_forms(self):
        inventory = []
        restriction = ItemPlacementHelpers.need_forms
        self.assertFalse(restriction(inventory))

        inventory.append(form.LimitForm.id)
        inventory.append(form.MasterForm.id)
        inventory.append(form.FinalForm.id)
        inventory.append(form.ValorForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.WisdomForm.id)
        self.assertTrue(restriction(inventory))

    def test_need_summons(self):
        inventory = []
        restriction = ItemPlacementHelpers.need_summons
        self.assertFalse(restriction(inventory))

        inventory.append(summon.LampCharm.id)
        inventory.append(summon.UkuleleCharm.id)
        inventory.append(summon.BaseballCharm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(summon.FeatherCharm.id)
        self.assertTrue(restriction(inventory))

    def test_need_n_pages(self):
        inventory = []

        restriction = ItemPlacementHelpers.need_torn_pages(3)
        self.assertFalse(restriction(inventory))

        inventory.append(misc.TornPages.id)
        self.assertFalse(restriction(inventory))

        inventory.append(misc.TornPages.id)
        self.assertFalse(restriction(inventory))

        inventory.append(misc.TornPages.id)
        self.assertTrue(restriction(inventory))

        inventory.append(misc.TornPages.id)
        self.assertTrue(restriction(inventory))

        inventory.append(misc.TornPages.id)
        self.assertTrue(restriction(inventory))

        inventory.append(misc.TornPages.id)
        self.assertTrue(restriction(inventory))

        inventory.append(misc.TornPages.id)
        self.assertTrue(restriction(inventory))

    def test_need_proofs(self):
        inventory = []

        restriction = ItemPlacementHelpers.need_proofs
        self.assertFalse(restriction(inventory))

        inventory.append(proof.ProofOfPeace.id)
        self.assertFalse(restriction(inventory))

        inventory.append(proof.ProofOfConnection.id)
        self.assertFalse(restriction(inventory))

        inventory.append(proof.ProofOfNonexistence.id)
        self.assertTrue(restriction(inventory))

    def test_oc1_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.oc1_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.BattlefieldsOfWar.id)
        self.assertTrue(restriction(inventory))

    def test_oc2_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.oc2_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.BattlefieldsOfWar.id)
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.BattlefieldsOfWar.id)
        self.assertTrue(restriction(inventory))

    def test_lod1_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.lod1_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.SwordOfTheAncestor.id)
        self.assertTrue(restriction(inventory))

    def test_lod2_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.lod2_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.SwordOfTheAncestor.id)
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.SwordOfTheAncestor.id)
        self.assertTrue(restriction(inventory))

    def test_bc1_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.bc1_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.BeastsClaw.id)
        self.assertTrue(restriction(inventory))

    def test_bc2_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.bc2_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.BeastsClaw.id)
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.BeastsClaw.id)
        self.assertTrue(restriction(inventory))

    def test_ht1_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.ht1_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.BoneFist.id)
        self.assertTrue(restriction(inventory))

    def test_ht2_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.ht2_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.BoneFist.id)
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.BoneFist.id)
        self.assertTrue(restriction(inventory))

    def test_pl1_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.pl1_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.ProudFang.id)
        self.assertTrue(restriction(inventory))

    def test_pl2_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.pl2_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.ProudFang.id)
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.ProudFang.id)
        self.assertTrue(restriction(inventory))

    def test_pr1_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.pr1_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.SkillAndCrossbones.id)
        self.assertTrue(restriction(inventory))

    def test_pr2_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.pr2_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.SkillAndCrossbones.id)
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.SkillAndCrossbones.id)
        self.assertTrue(restriction(inventory))

    def test_ag1_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.ag1_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.Scimitar.id)
        self.assertTrue(restriction(inventory))

    def test_ag2_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.ag2_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.Scimitar.id)
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.Scimitar.id)
        self.assertTrue(restriction(inventory))

    def test_sp1_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.sp1_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.IdentityDisk.id)
        self.assertTrue(restriction(inventory))

    def test_sp2_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.sp2_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.IdentityDisk.id)
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.IdentityDisk.id)
        self.assertTrue(restriction(inventory))


    def test_twtnw_roxas_check(self):
        inventory = []
    
        restriction = ItemPlacementHelpers.twtnw_roxas_check
        self.assertFalse(restriction(inventory))
    
        inventory.append(storyunlock.WayToTheDawn.id)
        self.assertTrue(restriction(inventory))

    def test_twtnw_post_saix_check(self):
        inventory = []
    
        restriction = ItemPlacementHelpers.twtnw_post_saix_check
        self.assertFalse(restriction(inventory))
    
        inventory.append(storyunlock.WayToTheDawn.id)
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.WayToTheDawn.id)
        self.assertTrue(restriction(inventory))

    def test_tt1_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.tt1_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.IceCream.id)
        self.assertTrue(restriction(inventory))

    def test_tt2_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.tt2_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.IceCream.id)
        inventory.append(storyunlock.IceCream.id)
        self.assertTrue(restriction(inventory))

    def test_tt3_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.tt3_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.IceCream.id)
        inventory.append(storyunlock.IceCream.id)
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.IceCream.id)
        self.assertTrue(restriction(inventory))

    def test_hb1_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.hb1_check
        self.assertFalse(restriction(inventory))
        
        inventory.append(storyunlock.MembershipCard.id)
        self.assertTrue(restriction(inventory))

    def test_hb2_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.hb2_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.MembershipCard.id)
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.MembershipCard.id)
        self.assertTrue(restriction(inventory))


    def test_dc1_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.dc1_check
        self.assertFalse(restriction(inventory))
        
        inventory.append(storyunlock.DisneyCastleKey.id)
        self.assertTrue(restriction(inventory))

    def test_dc2_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.dc2_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.DisneyCastleKey.id)
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.DisneyCastleKey.id)
        self.assertTrue(restriction(inventory))

    def test_stt_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.stt_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.NaminesSketches.id)
        self.assertTrue(restriction(inventory))


    def test_form_lambda_valor_2(self):
        inventory = []

        restriction = ItemPlacementHelpers.make_form_lambda(form.ValorForm, 2)
        self.assertFalse(restriction(inventory))

        inventory.append(form.ValorForm.id)
        self.assertTrue(restriction(inventory))

    def test_form_lambda_valor_3(self):
        inventory = []

        restriction = ItemPlacementHelpers.make_form_lambda(form.ValorForm, 3)
        self.assertFalse(restriction(inventory))

        inventory.append(form.ValorForm.id)
        self.assertTrue(restriction(inventory))

    def test_form_lambda_valor_4(self):
        inventory = []

        restriction = ItemPlacementHelpers.make_form_lambda(form.ValorForm, 4)
        self.assertFalse(restriction(inventory))

        inventory.append(form.ValorForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.LimitForm.id)
        self.assertTrue(restriction(inventory))

    def test_form_lambda_valor_5(self):
        inventory = []

        restriction = ItemPlacementHelpers.make_form_lambda(form.ValorForm, 5)
        self.assertFalse(restriction(inventory))

        inventory.append(form.ValorForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.LimitForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.WisdomForm.id)
        self.assertTrue(restriction(inventory))

    def test_form_lambda_valor_6(self):
        inventory = []

        restriction = ItemPlacementHelpers.make_form_lambda(form.ValorForm, 6)
        self.assertFalse(restriction(inventory))

        inventory.append(form.ValorForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.LimitForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.WisdomForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.FinalForm.id)
        self.assertTrue(restriction(inventory))

    def test_form_lambda_valor_7(self):
        inventory = []

        restriction = ItemPlacementHelpers.make_form_lambda(form.ValorForm, 7)
        self.assertFalse(restriction(inventory))

        inventory.append(form.ValorForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.LimitForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.WisdomForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.FinalForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.MasterForm.id)
        self.assertTrue(restriction(inventory))

    def test_form_lambda_nightmare_valor_2(self):
        inventory = []

        restriction = ItemPlacementHelpers.make_form_lambda_nightmare(form.ValorForm, 2)
        self.assertFalse(restriction(inventory))

        inventory.append(ability.AutoValor.id)
        self.assertTrue(restriction(inventory))

    def test_form_lambda_nightmare_valor_3(self):
        inventory = []

        restriction = ItemPlacementHelpers.make_form_lambda_nightmare(form.ValorForm, 3)
        self.assertFalse(restriction(inventory))

        inventory.append(form.ValorForm.id)
        self.assertTrue(restriction(inventory))

    def test_form_lambda_nightmare_valor_4(self):
        inventory = []

        restriction = ItemPlacementHelpers.make_form_lambda_nightmare(form.ValorForm, 4)
        self.assertFalse(restriction(inventory))

        inventory.append(form.MasterForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.LimitForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(ability.AutoValor.id)
        self.assertTrue(restriction(inventory))

    def test_form_lambda_nightmare_valor_5(self):
        inventory = []

        restriction = ItemPlacementHelpers.make_form_lambda_nightmare(form.ValorForm, 5)
        self.assertFalse(restriction(inventory))

        inventory.append(form.ValorForm.id)
        self.assertFalse(restriction(inventory))

        # Two forms is enough because you can force final
        inventory.append(form.LimitForm.id)
        self.assertTrue(restriction(inventory))

    def test_form_lambda_nightmare_valor_6(self):
        inventory = []

        restriction = ItemPlacementHelpers.make_form_lambda_nightmare(form.ValorForm, 6)
        self.assertFalse(restriction(inventory))

        inventory.append(ability.AutoValor.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.LimitForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.WisdomForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.FinalForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.MasterForm.id)
        self.assertTrue(restriction(inventory))

    def test_form_lambda_nightmare_valor_7(self):
        inventory = []

        restriction = ItemPlacementHelpers.make_form_lambda_nightmare(form.ValorForm, 7)
        self.assertFalse(restriction(inventory))

        inventory.append(form.ValorForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.LimitForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.WisdomForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.FinalForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.MasterForm.id)
        self.assertTrue(restriction(inventory))

    def test_form_lambda_nightmare_valor_2_no_final(self):
        inventory = []

        restriction = ItemPlacementHelpers.make_form_lambda_nightmare_no_final(form.ValorForm, 2)
        self.assertFalse(restriction(inventory))

        inventory.append(ability.AutoValor.id)
        self.assertTrue(restriction(inventory))

    def test_form_lambda_nightmare_valor_3_no_final(self):
        inventory = []

        restriction = ItemPlacementHelpers.make_form_lambda_nightmare_no_final(form.ValorForm, 3)
        self.assertFalse(restriction(inventory))

        inventory.append(form.ValorForm.id)
        self.assertTrue(restriction(inventory))

    def test_form_lambda_nightmare_valor_4_no_final(self):
        inventory = []

        restriction = ItemPlacementHelpers.make_form_lambda_nightmare_no_final(form.ValorForm, 4)
        self.assertFalse(restriction(inventory))

        inventory.append(form.MasterForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.LimitForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(ability.AutoValor.id)
        self.assertTrue(restriction(inventory))

    def test_form_lambda_nightmare_valor_5_no_final(self):
        inventory = []

        restriction = ItemPlacementHelpers.make_form_lambda_nightmare_no_final(form.ValorForm, 5)
        self.assertFalse(restriction(inventory))

        inventory.append(form.ValorForm.id)
        self.assertFalse(restriction(inventory))

        # Two forms is not enough because you can_not_ force final
        inventory.append(form.LimitForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.FinalForm.id)
        self.assertTrue(restriction(inventory))

    def test_form_lambda_nightmare_valor_6_no_final(self):
        inventory = []

        restriction = ItemPlacementHelpers.make_form_lambda_nightmare_no_final(form.ValorForm, 6)
        self.assertFalse(restriction(inventory))

        inventory.append(ability.AutoValor.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.LimitForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.WisdomForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.FinalForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.MasterForm.id)
        self.assertTrue(restriction(inventory))

    def test_form_lambda_nightmare_valor_7_no_final(self):
        inventory = []

        restriction = ItemPlacementHelpers.make_form_lambda_nightmare_no_final(form.ValorForm, 7)
        self.assertFalse(restriction(inventory))

        inventory.append(form.ValorForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.LimitForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.WisdomForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.FinalForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.MasterForm.id)
        self.assertTrue(restriction(inventory))

    def test_form_lambda_wisdom_5(self):
        inventory = []

        restriction = ItemPlacementHelpers.make_form_lambda(form.WisdomForm, 5)
        self.assertFalse(restriction(inventory))

        inventory.append(form.ValorForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.WisdomForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.LimitForm.id)
        self.assertTrue(restriction(inventory))

    def test_form_lambda_limit_6(self):
        inventory = []

        restriction = ItemPlacementHelpers.make_form_lambda(form.LimitForm, 6)
        self.assertFalse(restriction(inventory))

        inventory.append(form.ValorForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.LimitForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.WisdomForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.FinalForm.id)
        self.assertTrue(restriction(inventory))

    def test_form_lambda_master_7(self):
        inventory = []

        restriction = ItemPlacementHelpers.make_form_lambda(form.MasterForm, 7)
        self.assertFalse(restriction(inventory))

        inventory.append(form.ValorForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.LimitForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.MasterForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.WisdomForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.FinalForm.id)
        self.assertFalse(restriction(inventory))

        # give access to HT
        inventory.append(storyunlock.BoneFist.id)
        self.assertTrue(restriction(inventory))

    def test_form_lambda_final_5(self):
        inventory = []

        restriction = ItemPlacementHelpers.make_form_lambda(form.FinalForm, 5)
        self.assertFalse(restriction(inventory))

        inventory.append(form.ValorForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.LimitForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.FinalForm.id)
        self.assertFalse(restriction(inventory))
        
        # give access to TWTNW
        inventory.append(storyunlock.WayToTheDawn.id)
        self.assertTrue(restriction(inventory))

    def test_form_lambda_nightmare_final_7(self):
        inventory = []

        restriction = ItemPlacementHelpers.make_form_lambda_nightmare(form.FinalForm, 7)
        self.assertFalse(restriction(inventory))

        inventory.append(form.ValorForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.LimitForm.id)
        self.assertFalse(restriction(inventory))

        inventory.append(form.MasterForm.id)
        self.assertFalse(restriction(inventory))

        # We can force final here, so we only need the others
        inventory.append(form.WisdomForm.id)
        self.assertFalse(restriction(inventory))

        # give access to TWTNW
        inventory.append(storyunlock.WayToTheDawn.id)
        self.assertTrue(restriction(inventory))


if __name__ == '__main__':
    unittest.main()
