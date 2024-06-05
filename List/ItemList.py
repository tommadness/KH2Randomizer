import itertools
from typing import Optional, Iterable

from Class.itemClass import KH2Item
from List.configDict import itemRarity
from List.inventory import ability, accessory, armor, bonus, consumable, form, growth, keyblade, magic, \
    misc, map, proof, recipe, report, shield, staff, storyunlock, summon, synth
from List.inventory.ability import DonaldAbilities, GoofyAbilities, Ability
from List.inventory.keyblade import Keyblade
from List.location import weaponslot


class Items:

    @staticmethod
    def sora_lookup_table() -> dict[int, KH2Item]:
        """ Returns an _attempt_ at a comprehensive lookup table of item ID to item. May not include everything. """
        full_list = Items.getItemList()
        full_list.extend(Items.getStatItems())
        full_list.extend(Items.getDummyFormItems())
        full_list.append(Items.getPromiseCharm())
        full_list.append(Items.getTT1Jailbreak())
        full_list.append(Items.objectiveReportItem())
        full_list.extend(Items.getSupportAbilityList())
        full_list.extend(Items.getKeybladeAbilityList())
        full_list.extend(Items.getActionAbilityList())
        full_list.extend(Items.getLevelAbilityList())
        full_list.extend(Items.getJunkList(betterJunk=False))

        result = {}
        for item in full_list:
            item_id = item.Id
            if item_id not in result:
                result[item_id] = item
        return result

    @staticmethod
    def getItemList(story_unlocking_rarity: itemRarity = itemRarity.UNCOMMON) -> list[KH2Item]:
        return [
            KH2Item(proof.ProofOfConnection, itemRarity.MYTHIC),
            KH2Item(proof.ProofOfNonexistence, itemRarity.MYTHIC),
            KH2Item(proof.ProofOfPeace, itemRarity.MYTHIC),

            KH2Item(storyunlock.BattlefieldsOfWar, story_unlocking_rarity),
            KH2Item(storyunlock.BattlefieldsOfWar, story_unlocking_rarity),
            KH2Item(storyunlock.SwordOfTheAncestor, story_unlocking_rarity),
            KH2Item(storyunlock.SwordOfTheAncestor, story_unlocking_rarity),
            KH2Item(storyunlock.BeastsClaw, story_unlocking_rarity),
            KH2Item(storyunlock.BeastsClaw, story_unlocking_rarity),
            KH2Item(storyunlock.BoneFist, story_unlocking_rarity),
            KH2Item(storyunlock.BoneFist, story_unlocking_rarity),
            KH2Item(storyunlock.ProudFang, story_unlocking_rarity),
            KH2Item(storyunlock.ProudFang, story_unlocking_rarity),
            KH2Item(storyunlock.SkillAndCrossbones, story_unlocking_rarity),
            KH2Item(storyunlock.SkillAndCrossbones, story_unlocking_rarity),
            KH2Item(storyunlock.Scimitar, story_unlocking_rarity),
            KH2Item(storyunlock.Scimitar, story_unlocking_rarity),
            KH2Item(storyunlock.WayToTheDawn, story_unlocking_rarity),
            KH2Item(storyunlock.WayToTheDawn, story_unlocking_rarity),
            KH2Item(storyunlock.IdentityDisk, story_unlocking_rarity),
            KH2Item(storyunlock.IdentityDisk, story_unlocking_rarity),
            # KH2Item(storyunlock.TournamentPoster, story_unlocking_rarity),
            KH2Item(storyunlock.MembershipCard, story_unlocking_rarity),
            KH2Item(storyunlock.MembershipCard, story_unlocking_rarity),
            KH2Item(storyunlock.IceCream, story_unlocking_rarity),
            KH2Item(storyunlock.IceCream, story_unlocking_rarity),
            KH2Item(storyunlock.IceCream, story_unlocking_rarity),
            KH2Item(storyunlock.RoyalSummons, story_unlocking_rarity),
            KH2Item(storyunlock.RoyalSummons, story_unlocking_rarity),
            KH2Item(storyunlock.NaminesSketches, story_unlocking_rarity),

            KH2Item(report.AnsemReport1, itemRarity.UNCOMMON),
            KH2Item(report.AnsemReport2, itemRarity.UNCOMMON),
            KH2Item(report.AnsemReport3, itemRarity.UNCOMMON),
            KH2Item(report.AnsemReport4, itemRarity.UNCOMMON),
            KH2Item(report.AnsemReport5, itemRarity.UNCOMMON),
            KH2Item(report.AnsemReport6, itemRarity.UNCOMMON),
            KH2Item(report.AnsemReport7, itemRarity.UNCOMMON),
            KH2Item(report.AnsemReport8, itemRarity.UNCOMMON),
            KH2Item(report.AnsemReport9, itemRarity.UNCOMMON),
            KH2Item(report.AnsemReport10, itemRarity.UNCOMMON),
            KH2Item(report.AnsemReport11, itemRarity.UNCOMMON),
            KH2Item(report.AnsemReport12, itemRarity.UNCOMMON),
            KH2Item(report.AnsemReport13, itemRarity.UNCOMMON),

            KH2Item(magic.Fire, itemRarity.MYTHIC),
            KH2Item(magic.Fire, itemRarity.MYTHIC),
            KH2Item(magic.Fire, itemRarity.MYTHIC),

            KH2Item(magic.Blizzard, itemRarity.MYTHIC),
            KH2Item(magic.Blizzard, itemRarity.MYTHIC),
            KH2Item(magic.Blizzard, itemRarity.MYTHIC),

            KH2Item(magic.Thunder, itemRarity.MYTHIC),
            KH2Item(magic.Thunder, itemRarity.MYTHIC),
            KH2Item(magic.Thunder, itemRarity.MYTHIC),

            KH2Item(magic.Cure, itemRarity.MYTHIC),
            KH2Item(magic.Cure, itemRarity.MYTHIC),
            KH2Item(magic.Cure, itemRarity.MYTHIC),

            KH2Item(magic.Magnet, itemRarity.MYTHIC),
            KH2Item(magic.Magnet, itemRarity.MYTHIC),
            KH2Item(magic.Magnet, itemRarity.MYTHIC),

            KH2Item(magic.Reflect, itemRarity.MYTHIC),
            KH2Item(magic.Reflect, itemRarity.MYTHIC),
            KH2Item(magic.Reflect, itemRarity.MYTHIC),

            KH2Item(growth.HighJump1),
            KH2Item(growth.HighJump2, itemRarity.UNCOMMON),
            KH2Item(growth.HighJump3, itemRarity.RARE),
            KH2Item(growth.HighJumpMax, itemRarity.RARE),

            KH2Item(growth.QuickRun1),
            KH2Item(growth.QuickRun2, itemRarity.UNCOMMON),
            KH2Item(growth.QuickRun3, itemRarity.RARE),
            KH2Item(growth.QuickRunMax, itemRarity.RARE),

            KH2Item(growth.AerialDodge1),
            KH2Item(growth.AerialDodge2, itemRarity.UNCOMMON),
            KH2Item(growth.AerialDodge3, itemRarity.RARE),
            KH2Item(growth.AerialDodgeMax, itemRarity.RARE),

            KH2Item(growth.Glide1),
            KH2Item(growth.Glide2, itemRarity.UNCOMMON),
            KH2Item(growth.Glide3, itemRarity.RARE),
            KH2Item(growth.GlideMax, itemRarity.RARE),

            KH2Item(growth.DodgeRoll1),
            KH2Item(growth.DodgeRoll2, itemRarity.UNCOMMON),
            KH2Item(growth.DodgeRoll3, itemRarity.RARE),
            KH2Item(growth.DodgeRollMax, itemRarity.RARE),

            KH2Item(form.ValorForm, itemRarity.MYTHIC),
            KH2Item(form.WisdomForm, itemRarity.MYTHIC),
            KH2Item(form.FinalForm, itemRarity.MYTHIC),
            KH2Item(form.MasterForm, itemRarity.MYTHIC),
            KH2Item(form.LimitForm, itemRarity.MYTHIC),
            KH2Item(form.AntiForm, itemRarity.RARE),

            KH2Item(misc.TornPages, itemRarity.MYTHIC),
            KH2Item(misc.TornPages, itemRarity.MYTHIC),
            KH2Item(misc.TornPages, itemRarity.MYTHIC),
            KH2Item(misc.TornPages, itemRarity.MYTHIC),
            KH2Item(misc.TornPages, itemRarity.MYTHIC),

            KH2Item(summon.LampCharm, itemRarity.MYTHIC),
            KH2Item(summon.FeatherCharm, itemRarity.MYTHIC),
            KH2Item(summon.UkuleleCharm, itemRarity.MYTHIC),
            KH2Item(summon.BaseballCharm, itemRarity.MYTHIC),

            KH2Item(keyblade.Oathkeeper),
            KH2Item(keyblade.Oblivion),
            KH2Item(keyblade.StarSeeker),
            KH2Item(keyblade.HiddenDragon),
            KH2Item(keyblade.HerosCrest),
            KH2Item(keyblade.Monochrome),
            KH2Item(keyblade.FollowTheWind),
            KH2Item(keyblade.CircleOfLife),
            KH2Item(keyblade.PhotonDebugger),
            KH2Item(keyblade.GullWing),
            KH2Item(keyblade.RumblingRose),
            KH2Item(keyblade.GuardianSoul),
            KH2Item(keyblade.WishingLamp),
            KH2Item(keyblade.DecisivePumpkin),
            KH2Item(keyblade.SleepingLion),
            KH2Item(keyblade.SweetMemories),
            KH2Item(keyblade.MysteriousAbyss),
            KH2Item(keyblade.TwoBecomeOne),
            KH2Item(keyblade.FatalCrest),
            KH2Item(keyblade.BondOfFlame),
            KH2Item(keyblade.Fenrir),
            KH2Item(keyblade.UltimaWeapon),
            KH2Item(keyblade.WinnersProof),
            KH2Item(keyblade.Pureblood),

            KH2Item(staff.CenturionPlus, itemRarity.UNCOMMON),
            KH2Item(staff.MeteorStaff, itemRarity.UNCOMMON),
            KH2Item(staff.NobodyLance, itemRarity.UNCOMMON),
            KH2Item(staff.PreciousMushroom, itemRarity.UNCOMMON),
            KH2Item(staff.PreciousMushroomPlus, itemRarity.UNCOMMON),
            KH2Item(staff.PremiumMushroom, itemRarity.UNCOMMON),
            KH2Item(staff.RisingDragon, itemRarity.UNCOMMON),
            KH2Item(staff.SaveTheQueenPlus, itemRarity.UNCOMMON),
            KH2Item(staff.ShamansRelic, itemRarity.UNCOMMON),

            KH2Item(shield.AkashicRecord, itemRarity.UNCOMMON),
            KH2Item(shield.FrozenPridePlus, itemRarity.UNCOMMON),
            KH2Item(shield.GenjiShield, itemRarity.UNCOMMON),
            KH2Item(shield.MajesticMushroom, itemRarity.UNCOMMON),
            KH2Item(shield.MajesticMushroomPlus, itemRarity.UNCOMMON),
            KH2Item(shield.NobodyGuard, itemRarity.UNCOMMON),
            KH2Item(shield.OgreShield, itemRarity.UNCOMMON),
            KH2Item(shield.SaveTheKingPlus, itemRarity.UNCOMMON),
            KH2Item(shield.UltimateMushroom, itemRarity.UNCOMMON),

            KH2Item(accessory.AbilityRing),
            KH2Item(accessory.EngineersRing),
            KH2Item(accessory.TechniciansRing),
            KH2Item(accessory.SkillRing),
            KH2Item(accessory.SkillfulRing),
            KH2Item(accessory.ExpertsRing),
            KH2Item(accessory.MastersRing),
            KH2Item(accessory.CosmicRing),
            KH2Item(accessory.ExecutivesRing),
            KH2Item(accessory.SardonyxRing),
            KH2Item(accessory.TourmalineRing),
            KH2Item(accessory.AquamarineRing),
            KH2Item(accessory.GarnetRing),
            KH2Item(accessory.DiamondRing),
            KH2Item(accessory.SilverRing),
            KH2Item(accessory.GoldRing),
            KH2Item(accessory.PlatinumRing),
            KH2Item(accessory.MythrilRing),
            KH2Item(accessory.OrichalcumRing),
            KH2Item(accessory.SoldierEarring),
            KH2Item(accessory.FencerEarring, itemRarity.UNCOMMON),
            KH2Item(accessory.MageEarring),
            KH2Item(accessory.SlayerEarring, itemRarity.UNCOMMON),
            KH2Item(accessory.Medal),
            KH2Item(accessory.MoonAmulet, itemRarity.RARE),
            KH2Item(accessory.StarCharm, itemRarity.RARE),
            KH2Item(accessory.CosmicArts, itemRarity.RARE),
            KH2Item(accessory.ShadowArchive, itemRarity.UNCOMMON),
            KH2Item(accessory.ShadowArchivePlus, itemRarity.RARE),
            KH2Item(accessory.FullBloom, itemRarity.UNCOMMON),
            KH2Item(accessory.FullBloomPlus, itemRarity.RARE),
            KH2Item(accessory.DrawRing, itemRarity.UNCOMMON),
            KH2Item(accessory.LuckyRing),

            KH2Item(armor.ElvenBandanna),
            KH2Item(armor.DivineBandanna),
            KH2Item(armor.ProtectBelt),
            KH2Item(armor.GaiaBelt),
            KH2Item(armor.PowerBand),
            KH2Item(armor.BusterBand),
            KH2Item(armor.CosmicBelt),
            KH2Item(armor.FireBangle),
            KH2Item(armor.FiraBangle),
            KH2Item(armor.FiragaBangle),
            KH2Item(armor.FiragunBangle),
            KH2Item(armor.BlizzardArmlet),
            KH2Item(armor.BlizzaraArmlet),
            KH2Item(armor.BlizzagaArmlet),
            KH2Item(armor.BlizzagunArmlet),
            KH2Item(armor.ThunderTrinket),
            KH2Item(armor.ThundaraTrinket),
            KH2Item(armor.ThundagaTrinket),
            KH2Item(armor.ThundagunTrinket),
            KH2Item(armor.ShockCharm),
            KH2Item(armor.ShockCharmPlus, itemRarity.UNCOMMON),
            KH2Item(armor.ShadowAnklet),
            KH2Item(armor.DarkAnklet),
            KH2Item(armor.MidnightAnklet),
            KH2Item(armor.ChaosAnklet),
            KH2Item(armor.ChampionBelt),
            KH2Item(armor.AbasChain),
            KH2Item(armor.AegisChain),
            KH2Item(armor.Acrisius),
            KH2Item(armor.AcrisiusPlus),
            KH2Item(armor.CosmicChain),
            KH2Item(armor.PetiteRibbon, itemRarity.RARE),
            KH2Item(armor.Ribbon, itemRarity.RARE),
            KH2Item(armor.GrandRibbon, itemRarity.RARE),

            KH2Item(misc.MunnyPouchMickey, itemRarity.RARE),
            KH2Item(misc.MunnyPouchOlette, itemRarity.RARE),

            KH2Item(misc.HadesCupTrophy, itemRarity.UNCOMMON),
            KH2Item(misc.UnknownDisk, itemRarity.UNCOMMON),

            # KH2Item(misc.CrystalOrb), # removing for objectives
            KH2Item(misc.SeifersTrophy),
            KH2Item(misc.OlympusStone, itemRarity.UNCOMMON),
            KH2Item(misc.AuronsStatue),
            KH2Item(misc.CursedMedallion),
            KH2Item(misc.Present),
            KH2Item(misc.DecoyPresents),
            KH2Item(misc.StruggleTrophy),

            KH2Item(recipe.MegaRecipe),
            KH2Item(recipe.StarRecipe),
            KH2Item(recipe.RecoveryRecipe),
            KH2Item(recipe.SkillRecipe),
            KH2Item(recipe.GuardRecipe),
            KH2Item(recipe.RoadToDiscovery),
            KH2Item(recipe.StrengthBeyondStrength),
            KH2Item(recipe.BookOfShadows),
            KH2Item(recipe.CloakedThunder),
            KH2Item(recipe.EternalBlossom),
            KH2Item(recipe.RareDocument),
            KH2Item(recipe.StyleRecipe),
            KH2Item(recipe.MoonRecipe),
            KH2Item(recipe.QueenRecipe),
            KH2Item(recipe.KingRecipe),
            KH2Item(recipe.UltimateRecipe),

            KH2Item(map.TowerMap),
            KH2Item(map.TwilightTownMap),
            KH2Item(map.SunsetHillMap),
            KH2Item(map.MansionMap),
            KH2Item(map.CastlePerimeterMap),
            KH2Item(map.GreatMawMap),
            KH2Item(map.MarketplaceMap),
            KH2Item(map.DarkRemembranceMap),
            KH2Item(map.DepthsOfRemembranceMap),
            KH2Item(map.GardenOfAssemblageMap),
            KH2Item(map.CastleMap),
            KH2Item(map.BasementMap),
            KH2Item(map.CastleWallsMap),
            KH2Item(map.UnderworldMap),
            KH2Item(map.CavernsMap),
            KH2Item(map.ColiseumMap),
            KH2Item(map.CaveOfWondersMap),
            KH2Item(map.RuinsMap),
            KH2Item(map.AgrabahMap),
            KH2Item(map.PalaceMap),
            KH2Item(map.EncampmentAreaMap),
            KH2Item(map.VillageAreaMap),
            KH2Item(map.HundredAcreWoodMap),
            KH2Item(map.PigletsHowseMap),
            KH2Item(map.RabbitsHowseMap),
            KH2Item(map.KangasHowseMap),
            KH2Item(map.SpookyCaveMap),
            KH2Item(map.StarryHillMap),
            KH2Item(map.SavannahMap),
            KH2Item(map.PrideRockMap),
            KH2Item(map.OasisMap),
            KH2Item(map.UnderseaKingdomMap),
            KH2Item(map.DisneyCastleMap),
            KH2Item(map.CornerstoneHillMap),
            KH2Item(map.WindowOfTimeMap),
            KH2Item(map.LilliputMap),
            KH2Item(map.BuildingSiteMap),
            KH2Item(map.MickeysHouseMap),
            KH2Item(map.HalloweenTownMap),
            KH2Item(map.ChristmasTownMap),
            KH2Item(map.CurlyHillMap),
            KH2Item(map.NavalMap),
            KH2Item(map.IslaDeMuertaMap),
            KH2Item(map.ShipGraveyardMap),
            KH2Item(map.InterceptorMap),
            KH2Item(map.BlackPearlMap),
            KH2Item(map.PitCellAreaMap),
            KH2Item(map.IoTowerMap),
            KH2Item(map.CentralComputerCoreMap),
            KH2Item(map.SolarSailerSimulationMap),
            KH2Item(map.DarkCityMap),
            KH2Item(map.CastleThatNeverWasMap),
        ]

    @staticmethod
    def getStatItems() -> list[KH2Item]:
        """Get different dummy items that represent stat bonuses (Dummy 23, 24, 25, 26, 27, 16)"""
        return list(itertools.repeat(KH2Item(bonus.MaxHpUp), 20)) + \
            list(itertools.repeat(KH2Item(bonus.MaxMpUp), 4)) + \
            list(itertools.repeat(KH2Item(bonus.DriveGaugeUp, itemRarity.RARE), 6)) + \
            list(itertools.repeat(KH2Item(bonus.ArmorSlotUp, itemRarity.UNCOMMON), 3)) + \
            list(itertools.repeat(KH2Item(bonus.AccessorySlotUp, itemRarity.UNCOMMON), 3)) + \
            list(itertools.repeat(KH2Item(bonus.ItemSlotUp, itemRarity.UNCOMMON), 5))

    @staticmethod
    def getPromiseCharm() -> KH2Item:
        return KH2Item(misc.PromiseCharm, itemRarity.MYTHIC)

    @staticmethod
    def getDummyFormItems() -> list[KH2Item]:
        return [
            KH2Item(form.DummyFinalForm, Rarity=itemRarity.MYTHIC),
            KH2Item(form.DummyValorForm, Rarity=itemRarity.MYTHIC)
        ]
    
    @staticmethod
    def getFormToDummyMap() -> dict[int,int]:
        return {form.ValorForm.id:form.DummyValorForm.id,
                form.FinalForm.id:form.DummyFinalForm.id,}

    @staticmethod
    def getTT1Jailbreak() -> KH2Item:
        return KH2Item(misc.Poster)

    @staticmethod
    def getSupportAbilityList() -> list[KH2Item]:
        return [
            KH2Item(ability.Scan),
            KH2Item(ability.AerialRecovery),
            KH2Item(ability.ComboMaster, itemRarity.RARE),
            KH2Item(ability.ComboPlus),
            KH2Item(ability.ComboPlus),
            KH2Item(ability.AirComboPlus),
            KH2Item(ability.AirComboPlus),
            KH2Item(ability.ReactionBoost),
            KH2Item(ability.FinishingPlus, itemRarity.RARE),
            KH2Item(ability.FormBoost, itemRarity.UNCOMMON),
            KH2Item(ability.FormBoost, itemRarity.UNCOMMON),
            KH2Item(ability.SummonBoost),
            KH2Item(ability.Draw, itemRarity.UNCOMMON),
            KH2Item(ability.Draw, itemRarity.UNCOMMON),
            KH2Item(ability.LuckyLucky),
            KH2Item(ability.LuckyLucky),
            KH2Item(ability.LuckyLucky),
            KH2Item(ability.MpRage),
            KH2Item(ability.MpHaste),
            KH2Item(ability.MpHastera),
            KH2Item(ability.MpHastega),
            KH2Item(ability.Defender),
            KH2Item(ability.NoExperience),
        ]
    @staticmethod
    def getKeybladeAbilityList() -> list[KH2Item]:
        return [
            KH2Item(ability.Scan),
            KH2Item(ability.ComboPlus),
            KH2Item(ability.AirComboPlus),
            KH2Item(ability.ComboBoost, itemRarity.UNCOMMON),
            KH2Item(ability.AirComboBoost, itemRarity.UNCOMMON),
            KH2Item(ability.ReactionBoost),
            KH2Item(ability.FinishingPlus, itemRarity.RARE),
            KH2Item(ability.NegativeCombo, itemRarity.RARE),
            KH2Item(ability.BerserkCharge, itemRarity.UNCOMMON),
            KH2Item(ability.DamageDrive),
            KH2Item(ability.DriveBoost),
            KH2Item(ability.FormBoost, itemRarity.UNCOMMON),
            KH2Item(ability.ExperienceBoost, itemRarity.RARE),
            KH2Item(ability.Draw, itemRarity.UNCOMMON),
            KH2Item(ability.Jackpot),
            KH2Item(ability.DriveConverter, itemRarity.UNCOMMON),
            KH2Item(ability.FireBoost),
            KH2Item(ability.BlizzardBoost),
            KH2Item(ability.ThunderBoost),
            KH2Item(ability.ItemBoost, itemRarity.UNCOMMON),
            KH2Item(ability.MpRage),
            KH2Item(ability.MpHaste),
            KH2Item(ability.MpHastera),
            KH2Item(ability.MpHastega),
            KH2Item(ability.DamageControl),
            KH2Item(ability.NoExperience),
            KH2Item(ability.LightAndDarkness, itemRarity.RARE),
        ]

    @staticmethod
    def getLevelAbilityList() -> list[KH2Item]:
        return [
            KH2Item(ability.ComboBoost, itemRarity.UNCOMMON),
            KH2Item(ability.ExperienceBoost, itemRarity.RARE),
            KH2Item(ability.MagicLockOn),
            KH2Item(ability.ReactionBoost),
            KH2Item(ability.ItemBoost, itemRarity.UNCOMMON),
            KH2Item(ability.LeafBracer),
            KH2Item(ability.FireBoost),
            KH2Item(ability.DriveBoost),
            KH2Item(ability.Draw, itemRarity.UNCOMMON),
            KH2Item(ability.CombinationBoost),
            KH2Item(ability.DamageDrive),
            KH2Item(ability.AirComboBoost, itemRarity.UNCOMMON),
            KH2Item(ability.BlizzardBoost),
            KH2Item(ability.DriveConverter, itemRarity.UNCOMMON),
            KH2Item(ability.NegativeCombo, itemRarity.RARE),
            KH2Item(ability.OnceMore, itemRarity.MYTHIC),
            KH2Item(ability.FinishingPlus, itemRarity.RARE),
            KH2Item(ability.ThunderBoost),
            KH2Item(ability.Defender),
            KH2Item(ability.BerserkCharge, itemRarity.UNCOMMON),
            KH2Item(ability.Jackpot),
            KH2Item(ability.SecondChance, itemRarity.MYTHIC),
            KH2Item(ability.DamageControl),
        ]

    @staticmethod
    def getActionAbilityList() -> list[KH2Item]:
        return [
            KH2Item(ability.Guard),
            KH2Item(ability.UpperSlash),
            KH2Item(ability.HorizontalSlash, itemRarity.RARE),
            KH2Item(ability.FinishingLeap, itemRarity.RARE),
            KH2Item(ability.RetaliatingSlash),
            KH2Item(ability.Slapshot, itemRarity.UNCOMMON),
            KH2Item(ability.DodgeSlash),
            KH2Item(ability.FlashStep, itemRarity.RARE),
            KH2Item(ability.SlideDash, itemRarity.RARE),
            KH2Item(ability.VicinityBreak),
            KH2Item(ability.GuardBreak, itemRarity.RARE),
            KH2Item(ability.Explosion, itemRarity.RARE),
            KH2Item(ability.AerialSweep, itemRarity.UNCOMMON),
            KH2Item(ability.AerialDive, itemRarity.RARE),
            KH2Item(ability.AerialSpiral, itemRarity.RARE),
            KH2Item(ability.AerialFinish),
            KH2Item(ability.MagnetBurst, itemRarity.RARE),
            KH2Item(ability.Counterguard),
            KH2Item(ability.AutoValor, itemRarity.UNCOMMON),
            KH2Item(ability.AutoWisdom, itemRarity.UNCOMMON),
            KH2Item(ability.AutoLimitForm, itemRarity.UNCOMMON),
            KH2Item(ability.AutoMaster, itemRarity.UNCOMMON),
            KH2Item(ability.AutoFinal, itemRarity.UNCOMMON),
            KH2Item(ability.AutoSummon, itemRarity.UNCOMMON),
            KH2Item(ability.TrinityLimit, itemRarity.RARE),
        ]

    @staticmethod
    def sort_ability_items(abilities: Iterable[KH2Item]) -> list[KH2Item]:
        def key_function(ability_item: KH2Item) -> int:
            inventory_item = ability_item.item
            if isinstance(inventory_item, Ability):
                return inventory_item.sort_index
            else:
                return 999999
        return sorted(abilities, key=key_function)

    @staticmethod
    def getNullItem() -> KH2Item:
        return KH2Item(misc.NullItem)

    # @staticmethod
    # def sharedMultiItem() -> KH2Item:
    #     return KH2Item(misc.SharedMultiworldItem)
    @staticmethod
    def objectiveReportItem() -> KH2Item:
        return KH2Item(misc.ObjectiveReport)


    @staticmethod
    def objectiveItem() -> KH2Item:
        return KH2Item(misc.ObjectiveItem)
    
    @staticmethod
    def emblemItem() -> KH2Item:
        return KH2Item(misc.EmblemItem)

    @staticmethod
    def weaponslot_id_to_keyblade_item(location_id: int) -> Optional[Keyblade]:
        slot_id_to_keyblade = {
            weaponslot.LocationId.KingdomKeyD: None,
            weaponslot.LocationId.AlphaWeapon: None,
            weaponslot.LocationId.OmegaWeapon: None,
            weaponslot.LocationId.KingdomKey: None,
            weaponslot.LocationId.Oathkeeper: keyblade.Oathkeeper,
            weaponslot.LocationId.Oblivion: keyblade.Oblivion,
            weaponslot.LocationId.StarSeeker: keyblade.StarSeeker,
            weaponslot.LocationId.HiddenDragon: keyblade.HiddenDragon,
            weaponslot.LocationId.HerosCrest: keyblade.HerosCrest,
            weaponslot.LocationId.Monochrome: keyblade.Monochrome,
            weaponslot.LocationId.FollowTheWind: keyblade.FollowTheWind,
            weaponslot.LocationId.CircleOfLife: keyblade.CircleOfLife,
            weaponslot.LocationId.PhotonDebugger: keyblade.PhotonDebugger,
            weaponslot.LocationId.GullWing: keyblade.GullWing,
            weaponslot.LocationId.RumblingRose: keyblade.RumblingRose,
            weaponslot.LocationId.GuardianSoul: keyblade.GuardianSoul,
            weaponslot.LocationId.WishingLamp: keyblade.WishingLamp,
            weaponslot.LocationId.DecisivePumpkin: keyblade.DecisivePumpkin,
            weaponslot.LocationId.SweetMemories: keyblade.SweetMemories,
            weaponslot.LocationId.MysteriousAbyss: keyblade.MysteriousAbyss,
            weaponslot.LocationId.SleepingLion: keyblade.SleepingLion,
            weaponslot.LocationId.BondOfFlame: keyblade.BondOfFlame,
            weaponslot.LocationId.TwoBecomeOne: keyblade.TwoBecomeOne,
            weaponslot.LocationId.FatalCrest: keyblade.FatalCrest,
            weaponslot.LocationId.Fenrir: keyblade.Fenrir,
            weaponslot.LocationId.UltimaWeapon: keyblade.UltimaWeapon,
            weaponslot.LocationId.WinnersProof: keyblade.WinnersProof,
            weaponslot.LocationId.Pureblood: keyblade.Pureblood
        }
        return slot_id_to_keyblade[location_id]

    @staticmethod
    def getJunkList(betterJunk) -> list[KH2Item]:
        if betterJunk:
            return [
                KH2Item(consumable.Potion),
                KH2Item(consumable.HiPotion),
                KH2Item(consumable.Ether),
                KH2Item(consumable.Elixir, itemRarity.UNCOMMON),
                KH2Item(consumable.MegaPotion),
                KH2Item(consumable.MegaEther),
                KH2Item(consumable.Megalixir, itemRarity.UNCOMMON),
                KH2Item(consumable.Tent),
                KH2Item(consumable.DriveRecovery, itemRarity.UNCOMMON),
                KH2Item(consumable.HighDriveRecovery, itemRarity.UNCOMMON),
                KH2Item(consumable.PowerBoost),
                KH2Item(consumable.MagicBoost),
                KH2Item(consumable.DefenseBoost),
                KH2Item(consumable.ApBoost),
            ]
        return [
            KH2Item(synth.BlazingShard),
            KH2Item(synth.BlazingStone),
            KH2Item(synth.BlazingGem),
            KH2Item(synth.BlazingCrystal),
            KH2Item(synth.FrostShard),
            KH2Item(synth.FrostStone),
            KH2Item(synth.FrostGem),
            KH2Item(synth.FrostCrystal),
            KH2Item(synth.LightningShard),
            KH2Item(synth.LightningStone),
            KH2Item(synth.LightningGem),
            KH2Item(synth.LightningCrystal),
            KH2Item(synth.LucidShard),
            KH2Item(synth.LucidStone),
            KH2Item(synth.LucidGem),
            KH2Item(synth.LucidCrystal),
            KH2Item(synth.PowerShard),
            KH2Item(synth.PowerStone),
            KH2Item(synth.PowerGem),
            KH2Item(synth.PowerCrystal),
            KH2Item(synth.DarkShard),
            KH2Item(synth.DarkStone),
            KH2Item(synth.DarkGem),
            KH2Item(synth.DarkCrystal),
            KH2Item(synth.DenseShard),
            KH2Item(synth.DenseStone),
            KH2Item(synth.DenseGem),
            KH2Item(synth.DenseCrystal),
            KH2Item(synth.TwilightShard),
            KH2Item(synth.TwilightStone),
            KH2Item(synth.TwilightGem),
            KH2Item(synth.TwilightCrystal),
            KH2Item(synth.MythrilShard),
            KH2Item(synth.MythrilStone),
            KH2Item(synth.MythrilGem),
            KH2Item(synth.MythrilCrystal),
            KH2Item(synth.RemembranceShard),
            KH2Item(synth.RemembranceStone),
            KH2Item(synth.RemembranceGem),
            KH2Item(synth.RemembranceCrystal),
            KH2Item(synth.TranquilityShard),
            KH2Item(synth.TranquilityStone),
            KH2Item(synth.TranquilityGem),
            KH2Item(synth.TranquilityCrystal),
            KH2Item(synth.BrightShard),
            KH2Item(synth.BrightStone),
            KH2Item(synth.BrightGem),
            KH2Item(synth.BrightCrystal),
            KH2Item(synth.EnergyShard),
            KH2Item(synth.EnergyStone),
            KH2Item(synth.EnergyGem),
            KH2Item(synth.EnergyCrystal),
            KH2Item(synth.SerenityShard),
            KH2Item(synth.SerenityStone),
            KH2Item(synth.SerenityGem),
            KH2Item(synth.SerenityCrystal),
            KH2Item(synth.LostIllusion),
            KH2Item(synth.ManifestIllusion),
            KH2Item(synth.Orichalcum),
            KH2Item(synth.OrichalcumPlus),
            KH2Item(consumable.Potion),
            KH2Item(consumable.HiPotion),
            KH2Item(consumable.Ether),
            KH2Item(consumable.Elixir, itemRarity.UNCOMMON),
            KH2Item(consumable.MegaPotion),
            KH2Item(consumable.MegaEther),
            KH2Item(consumable.Megalixir, itemRarity.UNCOMMON),
            KH2Item(consumable.Tent),
            KH2Item(consumable.DriveRecovery, itemRarity.UNCOMMON),
            KH2Item(consumable.HighDriveRecovery, itemRarity.UNCOMMON),
            KH2Item(consumable.PowerBoost),
            KH2Item(consumable.MagicBoost),
            KH2Item(consumable.DefenseBoost),
            KH2Item(consumable.ApBoost),
        ]

    @staticmethod
    def getSynthRequirementsList() -> list[KH2Item]:
        return [
            KH2Item(synth.BlazingShard),
            KH2Item(synth.BlazingStone),
            KH2Item(synth.BlazingGem),
            KH2Item(synth.BlazingCrystal),
            KH2Item(synth.FrostShard),
            KH2Item(synth.FrostStone),
            KH2Item(synth.FrostGem),
            KH2Item(synth.FrostCrystal),
            KH2Item(synth.LightningShard),
            KH2Item(synth.LightningStone),
            KH2Item(synth.LightningGem),
            KH2Item(synth.LightningCrystal),
            KH2Item(synth.LucidShard),
            KH2Item(synth.LucidStone),
            KH2Item(synth.LucidGem),
            KH2Item(synth.LucidCrystal),
            KH2Item(synth.PowerShard),
            KH2Item(synth.PowerStone),
            KH2Item(synth.PowerGem),
            KH2Item(synth.PowerCrystal),
            KH2Item(synth.DarkShard),
            KH2Item(synth.DarkStone),
            KH2Item(synth.DarkGem),
            KH2Item(synth.DarkCrystal),
            KH2Item(synth.DenseShard),
            KH2Item(synth.DenseStone),
            KH2Item(synth.DenseGem),
            KH2Item(synth.DenseCrystal),
            KH2Item(synth.TwilightShard),
            KH2Item(synth.TwilightStone),
            KH2Item(synth.TwilightGem),
            KH2Item(synth.TwilightCrystal),
            # may be able to bring these back if the class of item is known
            # KH2Item(synth.BrightShard),
            # KH2Item(synth.BrightStone),
            # KH2Item(synth.BrightGem),
            # KH2Item(synth.BrightCrystal),
            # KH2Item(synth.EnergyShard),
            # KH2Item(synth.EnergyStone),
            # KH2Item(synth.EnergyGem),
            # KH2Item(synth.EnergyCrystal),
        ]

    @staticmethod
    def donald_ability_list() -> list[KH2Item]:
        return [
            KH2Item(DonaldAbilities.DonaldFire),
            KH2Item(DonaldAbilities.DonaldBlizzard),
            KH2Item(DonaldAbilities.DonaldThunder),
            KH2Item(DonaldAbilities.DonaldCure),
            KH2Item(DonaldAbilities.Fantasia),
            KH2Item(DonaldAbilities.FlareForce),
            KH2Item(DonaldAbilities.MpRage),
            KH2Item(DonaldAbilities.Jackpot),
            KH2Item(DonaldAbilities.LuckyLucky),
            KH2Item(DonaldAbilities.FireBoost),
            KH2Item(DonaldAbilities.BlizzardBoost),
            KH2Item(DonaldAbilities.ThunderBoost),
            KH2Item(DonaldAbilities.FireBoost),
            KH2Item(DonaldAbilities.BlizzardBoost),
            KH2Item(DonaldAbilities.ThunderBoost),
            KH2Item(DonaldAbilities.MpRage),
            KH2Item(DonaldAbilities.MpHastera),
            KH2Item(DonaldAbilities.AutoLimitParty),
            KH2Item(DonaldAbilities.HyperHealing),
            KH2Item(DonaldAbilities.AutoHealing),
            KH2Item(DonaldAbilities.MpHastega),
            KH2Item(DonaldAbilities.ItemBoost),
            KH2Item(DonaldAbilities.DamageControl),
            KH2Item(DonaldAbilities.HyperHealing),
            KH2Item(DonaldAbilities.MpRage),
            KH2Item(DonaldAbilities.MpHaste),
            KH2Item(DonaldAbilities.MpHastera),
            KH2Item(DonaldAbilities.MpHastega),
            KH2Item(DonaldAbilities.MpHaste),
            KH2Item(DonaldAbilities.DamageControl),
            KH2Item(DonaldAbilities.MpHastera),
            KH2Item(DonaldAbilities.Draw),
        ]

    @staticmethod
    def goofy_ability_list() -> list[KH2Item]:
        return [
            KH2Item(GoofyAbilities.GoofyTornado),
            KH2Item(GoofyAbilities.GoofyTurbo),
            KH2Item(GoofyAbilities.GoofyBash),
            KH2Item(GoofyAbilities.TornadoFusion),
            KH2Item(GoofyAbilities.Teamwork),
            KH2Item(GoofyAbilities.Draw),
            KH2Item(GoofyAbilities.Jackpot),
            KH2Item(GoofyAbilities.LuckyLucky),
            KH2Item(GoofyAbilities.ItemBoost),
            KH2Item(GoofyAbilities.MpRage),
            KH2Item(GoofyAbilities.Defender),
            KH2Item(GoofyAbilities.DamageControl),
            KH2Item(GoofyAbilities.AutoLimitParty),
            KH2Item(GoofyAbilities.SecondChance),
            KH2Item(GoofyAbilities.OnceMore),
            KH2Item(GoofyAbilities.AutoChange),
            KH2Item(GoofyAbilities.HyperHealing),
            KH2Item(GoofyAbilities.AutoHealing),
            KH2Item(GoofyAbilities.Defender),
            KH2Item(GoofyAbilities.HyperHealing),
            KH2Item(GoofyAbilities.MpHaste),
            KH2Item(GoofyAbilities.MpHastera),
            KH2Item(GoofyAbilities.MpRage),
            KH2Item(GoofyAbilities.MpHastega),
            KH2Item(GoofyAbilities.ItemBoost),
            KH2Item(GoofyAbilities.DamageControl),
            KH2Item(GoofyAbilities.Protect),
            KH2Item(GoofyAbilities.Protera),
            KH2Item(GoofyAbilities.Protega),
            KH2Item(GoofyAbilities.DamageControl),
            KH2Item(GoofyAbilities.Protect),
            KH2Item(GoofyAbilities.Protera),
            KH2Item(GoofyAbilities.Protega),
        ]
