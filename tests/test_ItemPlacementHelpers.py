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

    def test_auron_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.auron_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.BattlefieldsOfWar.id)
        self.assertTrue(restriction(inventory))

    def test_mulan_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.mulan_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.SwordOfTheAncestor.id)
        self.assertTrue(restriction(inventory))

    def test_beast_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.beast_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.BeastsClaw.id)
        self.assertTrue(restriction(inventory))

    def test_jack_ht_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.jack_ht_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.BoneFist.id)
        self.assertTrue(restriction(inventory))

    def test_simba_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.simba_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.ProudFang.id)
        self.assertTrue(restriction(inventory))

    def test_jack_pr_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.jack_pr_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.SkillAndCrossbones.id)
        self.assertTrue(restriction(inventory))

    def test_aladdin_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.aladdin_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.Scimitar.id)
        self.assertTrue(restriction(inventory))

    def test_tron_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.tron_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.IdentityDisk.id)
        self.assertTrue(restriction(inventory))

    # def test_riku_check(self):
    #     inventory = []
    #
    #     restriction = ItemPlacementHelpers.riku_check
    #     self.assertFalse(restriction(inventory))
    #
    #     inventory.append(storyunlock.WayToTheDawn.id)
    #     self.assertTrue(restriction(inventory))

    def test_tt2_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.tt2_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.Picture.id)
        self.assertTrue(restriction(inventory))

    def test_tt3_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.tt3_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.IceCream.id)
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.Picture.id)
        self.assertTrue(restriction(inventory))

    def test_hb_check(self):
        inventory = []

        restriction = ItemPlacementHelpers.hb_check
        self.assertFalse(restriction(inventory))

        inventory.append(storyunlock.MembershipCard.id)
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
        self.assertTrue(restriction(inventory))


if __name__ == '__main__':
    unittest.main()
