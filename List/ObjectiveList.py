from dataclasses import dataclass
from enum import Enum

class ObjectiveType(str, Enum):
    BOSS = "Boss"
    WORLDPROGRESS = "WorldProgress"
    FIGHT = "Fight"

class ObjectiveDifficulty(str, Enum):
    EARLY = "Early"
    MIDDLE = "Middle"
    LATE = "Late"
    LATEST = "Latest"

@dataclass (frozen=True)
class KH2Objective:
    Name: str
    Location: Enum
    Type: ObjectiveType
    Difficulty: ObjectiveDifficulty = ObjectiveDifficulty.EARLY

def get_full_objective_list():
    from List.location import (simulatedtwilighttown,twilighttown,hollowbastion,landofdragons,
                            beastscastle,disneycastle,portroyal,agrabah,halloweentown,
                            pridelands, spaceparanoids, worldthatneverwas, olympuscoliseum,
                            hundredacrewood, atlantica, formlevel,puzzlereward)
    return [
        # STT
        KH2Objective("Defeat Twilight Thorn",simulatedtwilighttown.CheckLocation.TwilightThorn,ObjectiveType.BOSS),
        KH2Objective("Defeat Axel I",simulatedtwilighttown.CheckLocation.Axel1,ObjectiveType.FIGHT),
        KH2Objective("Fight Setzer",simulatedtwilighttown.CheckLocation.StruggleTrophy,ObjectiveType.FIGHT),
        KH2Objective("Defeat Axel II",simulatedtwilighttown.CheckLocation.Axel2,ObjectiveType.BOSS),
        # TT
        KH2Objective("Talk to the 3 Fairies",twilighttown.CheckLocation.ValorForm,ObjectiveType.WORLDPROGRESS),
        KH2Objective("Defeat Sandlot Berserkers",twilighttown.CheckLocation.SeifersTrophy,ObjectiveType.FIGHT,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Fight alongside Axel",twilighttown.CheckLocation.BetwixtAndBetween,ObjectiveType.FIGHT,ObjectiveDifficulty.LATE),
        # HB
        KH2Objective("Defend the Bailey",hollowbastion.CheckLocation.Bailey,ObjectiveType.FIGHT),
        KH2Objective("Defeat Demyx",hollowbastion.CheckLocation.DemyxHollowBastion,ObjectiveType.BOSS,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Stop the 1000 Heartless",hollowbastion.CheckLocation.ThousandHeartless,ObjectiveType.FIGHT,ObjectiveDifficulty.LATE),
        # CoR
        KH2Objective("Reach the end of Cavern of Remembrance",hollowbastion.CheckLocation.CorMineshaftUpperLevelApBoost,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.LATE),
        KH2Objective("Reach the end of Transport of Remembrance",hollowbastion.CheckLocation.TransportToRemembrance,ObjectiveType.FIGHT,ObjectiveDifficulty.LATEST),
        # LoD
        KH2Objective("Climb the Mountain Trail",landofdragons.CheckLocation.VillageCaveAreaMap,ObjectiveType.WORLDPROGRESS),
        KH2Objective("Fight the Enemies in Village Cave",landofdragons.CheckLocation.VillageCaveBonus,ObjectiveType.FIGHT),
        KH2Objective("Defeat Shan Yu",landofdragons.CheckLocation.ShanYuBonus,ObjectiveType.BOSS,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Defeat Stormrider",landofdragons.CheckLocation.StormRiderBonus,ObjectiveType.BOSS,ObjectiveDifficulty.LATE),
        # BC
        KH2Objective("Defeat Thresholder",beastscastle.CheckLocation.Thresholder,ObjectiveType.BOSS),
        KH2Objective("Help Beast",beastscastle.CheckLocation.Beast,ObjectiveType.WORLDPROGRESS),
        KH2Objective("Defeat Dark Thorn",beastscastle.CheckLocation.DarkThorn,ObjectiveType.BOSS,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Defeat Xaldin",beastscastle.CheckLocation.XaldinBonus,ObjectiveType.BOSS,ObjectiveDifficulty.LATE),
        # DC
        KH2Objective("Escort Queen Minnie",disneycastle.CheckLocation.MinnieEscort,ObjectiveType.WORLDPROGRESS),
        KH2Objective("Fight through Windows of Time",disneycastle.CheckLocation.WindowOfTimeMap,ObjectiveType.FIGHT,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Stop Pete from Escaping",disneycastle.CheckLocation.BoatPete,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Defeat Future Pete",disneycastle.CheckLocation.MinnieEscort,ObjectiveType.BOSS,ObjectiveDifficulty.LATE),
        # PR
        KH2Objective("Stall for time on Isla de Muerta",portroyal.CheckLocation.IslaDeMuertaMap,ObjectiveType.WORLDPROGRESS),
        KH2Objective("Defend the Interceptor from pirates",portroyal.CheckLocation.BoatFight,ObjectiveType.FIGHT),
        KH2Objective("Stop the explosive barrels",portroyal.CheckLocation.InterceptorBarrels,ObjectiveType.WORLDPROGRESS),
        KH2Objective("Defeat Barbossa",portroyal.CheckLocation.Barbossa,ObjectiveType.BOSS,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Defeat Grim Reaper I",portroyal.CheckLocation.GrimReaper1,ObjectiveType.BOSS,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Defeat Grim Reaper II",portroyal.CheckLocation.GrimReaper2,ObjectiveType.BOSS,ObjectiveDifficulty.LATE),
        # AG
        KH2Objective("Escort Abu",agrabah.CheckLocation.AbuEscort,ObjectiveType.WORLDPROGRESS),
        KH2Objective("Survive the Treasure Room Ambush",agrabah.CheckLocation.TreasureRoomBonus,ObjectiveType.FIGHT,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Defeat the Elemental Lords",agrabah.CheckLocation.ElementalLordsBonus,ObjectiveType.BOSS,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Defeat Genie Jafar",agrabah.CheckLocation.TreasureRoomBonus,ObjectiveType.BOSS,ObjectiveDifficulty.LATE),
        # HT
        KH2Objective("Defeat Prison Keeper",halloweentown.CheckLocation.PrisonKeeper,ObjectiveType.BOSS),
        KH2Objective("Defeat Oogie Boogie",halloweentown.CheckLocation.OogieBoogie,ObjectiveType.BOSS,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Capture Lock Shock and Barrel",halloweentown.CheckLocation.LockShockBarrel,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Find the stolen presents",halloweentown.CheckLocation.Present,ObjectiveType.FIGHT,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Create decoy presents",halloweentown.CheckLocation.DecoyPresents,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Defeat the Experiment",halloweentown.CheckLocation.Experiment,ObjectiveType.BOSS,ObjectiveDifficulty.LATE),
        # PL
        KH2Objective("Reunite with Simba",pridelands.CheckLocation.CircleOfLife,ObjectiveType.WORLDPROGRESS),
        KH2Objective("Rescue Timon and Pumbaa",pridelands.CheckLocation.Hyenas1,ObjectiveType.WORLDPROGRESS),
        KH2Objective("Defeat Scar",pridelands.CheckLocation.Scar,ObjectiveType.BOSS,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Get info about the ghost of Scar from Hyenas",pridelands.CheckLocation.Hyenas2,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Defeat Groundshaker",pridelands.CheckLocation.Groundshaker,ObjectiveType.BOSS,ObjectiveDifficulty.LATE),
        # SP
        KH2Objective("Survive the Dataspace Attack",spaceparanoids.CheckLocation.ScreensBonus,ObjectiveType.FIGHT),
        KH2Objective("Defeat Hostile Program",spaceparanoids.CheckLocation.ScreensBonus,ObjectiveType.BOSS,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Ride the Solar Sailor",spaceparanoids.CheckLocation.SolarSailerBonus,ObjectiveType.FIGHT,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Defeat MCP",spaceparanoids.CheckLocation.ScreensBonus,ObjectiveType.BOSS,ObjectiveDifficulty.LATE),
        # TWTNW
        KH2Objective("Defeat Roxas",worldthatneverwas.CheckLocation.Roxas,ObjectiveType.BOSS),
        KH2Objective("Defeat Xigbar",worldthatneverwas.CheckLocation.XigbarBonus,ObjectiveType.BOSS,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Defeat Luxord",worldthatneverwas.CheckLocation.LuxordBonus,ObjectiveType.BOSS,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Defeat Saix",worldthatneverwas.CheckLocation.SaixBonus,ObjectiveType.BOSS,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Defeat Xemnas",worldthatneverwas.CheckLocation.Xemnas1Bonus,ObjectiveType.BOSS,ObjectiveDifficulty.LATE),
        # OC
        KH2Objective("Defeat Cerberus",olympuscoliseum.CheckLocation.Cerberus,ObjectiveType.BOSS),
        KH2Objective("Train with Phil",olympuscoliseum.CheckLocation.Urns,ObjectiveType.WORLDPROGRESS),
        KH2Objective("Defeat Pete at The Lock",olympuscoliseum.CheckLocation.PeteOlympusColiseum,ObjectiveType.FIGHT,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Defeat Hydra",olympuscoliseum.CheckLocation.Hydra,ObjectiveType.BOSS,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Defeat the Ambush in Hades Chamber",olympuscoliseum.CheckLocation.AuronssStatue,ObjectiveType.FIGHT,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Defeat Hades",olympuscoliseum.CheckLocation.Hades,ObjectiveType.BOSS,ObjectiveDifficulty.LATE),
        # Cups
        KH2Objective("Win the Pain and Panic Cup",olympuscoliseum.CheckLocation.PainPanicCupProtectBelt,ObjectiveType.FIGHT),
        KH2Objective("Win the Cerberus Cup",olympuscoliseum.CheckLocation.CerberusCupRisingDragon,ObjectiveType.FIGHT,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Win the Titan Cup",olympuscoliseum.CheckLocation.TitanCupGenjiShield,ObjectiveType.FIGHT,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Win the Goddess of Fate Cup",olympuscoliseum.CheckLocation.GoddessOfFateCupFatalCrest,ObjectiveType.FIGHT,ObjectiveDifficulty.LATE),
        # HAW
        KH2Objective("Rescue Pooh from the Spooky Cave",hundredacrewood.CheckLocation.SweetMemories,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.LATE),
        KH2Objective("Help Pooh out of the pot of hunny",hundredacrewood.CheckLocation.StarryHillCureElement,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.LATEST),
        # AT
        KH2Objective("Relearn to swim",atlantica.CheckLocation.UnderseaKingdomMap,ObjectiveType.WORLDPROGRESS),
        KH2Objective("Defeat Ursula",atlantica.CheckLocation.MysteriousAbyss,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.LATE),
        KH2Objective("Participate the New Day Musical",atlantica.CheckLocation.MusicalBlizzardElement,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.LATEST),
        # FORM
        KH2Objective("Reach Valor Level 3",formlevel.CheckLocation.Valor3,ObjectiveType.WORLDPROGRESS),
        KH2Objective("Reach Valor Level 5",formlevel.CheckLocation.Valor5,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Reach Valor Level 7",formlevel.CheckLocation.Valor7,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.LATE),
        KH2Objective("Reach Wisdom Level 3",formlevel.CheckLocation.Wisdom3,ObjectiveType.WORLDPROGRESS),
        KH2Objective("Reach Wisdom Level 5",formlevel.CheckLocation.Wisdom5,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Reach Wisdom Level 7",formlevel.CheckLocation.Wisdom7,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.LATE),
        KH2Objective("Reach Limit Level 3",formlevel.CheckLocation.Limit3,ObjectiveType.WORLDPROGRESS),
        KH2Objective("Reach Limit Level 5",formlevel.CheckLocation.Limit5,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Reach Limit Level 7",formlevel.CheckLocation.Limit7,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.LATE),
        KH2Objective("Reach Master Level 3",formlevel.CheckLocation.Master3,ObjectiveType.WORLDPROGRESS),
        KH2Objective("Reach Master Level 5",formlevel.CheckLocation.Master5,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Reach Master Level 7",formlevel.CheckLocation.Master7,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.LATE),
        KH2Objective("Reach Final Level 3",formlevel.CheckLocation.Final3,ObjectiveType.WORLDPROGRESS),
        KH2Objective("Reach Final Level 5",formlevel.CheckLocation.Final5,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Reach Final Level 7",formlevel.CheckLocation.Final7,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.LATE),
        # Puzzle
        KH2Objective("Complete the Awakening Puzzle",puzzlereward.CheckLocation.AwakeningApBoost,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Complete the Heart Puzzle",puzzlereward.CheckLocation.HeartSerenityCrystal,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.MIDDLE),
        KH2Objective("Complete the Duality Puzzle",puzzlereward.CheckLocation.DualityRareDocument,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.LATE),
        KH2Objective("Complete the Frontier Puzzle",puzzlereward.CheckLocation.FrontierManifestIllusion,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.LATE),
        KH2Objective("Complete the Daylight Puzzle",puzzlereward.CheckLocation.DaylightExecutivesRing,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.LATEST),
        KH2Objective("Complete the Sunset Puzzle",puzzlereward.CheckLocation.SunsetGrandRibbon,ObjectiveType.WORLDPROGRESS,ObjectiveDifficulty.LATEST),
        # Superbosses
        KH2Objective("Defeat Sephiroth",hollowbastion.CheckLocation.SephirothBonus,ObjectiveType.BOSS,ObjectiveDifficulty.LATEST),
        KH2Objective("Defeat Lingering Will",disneycastle.CheckLocation.LingeringWillBonus,ObjectiveType.BOSS,ObjectiveDifficulty.LATEST),
        KH2Objective("Defeat Data Roxas",simulatedtwilighttown.CheckLocation.DataRoxasMagicBoost,ObjectiveType.BOSS,ObjectiveDifficulty.LATEST),
        KH2Objective("Defeat Data Demyx",hollowbastion.CheckLocation.DataDemyxApBoost,ObjectiveType.BOSS,ObjectiveDifficulty.LATEST),
        KH2Objective("Defeat Data Xigbar",landofdragons.CheckLocation.DataXigbarDefenseBoost,ObjectiveType.BOSS,ObjectiveDifficulty.LATEST),
        KH2Objective("Defeat Data Saix",pridelands.CheckLocation.DataSaix,ObjectiveType.BOSS,ObjectiveDifficulty.LATEST),
        KH2Objective("Defeat Data Axel",twilighttown.CheckLocation.DataAxelMagicBoost,ObjectiveType.BOSS,ObjectiveDifficulty.LATEST),
        KH2Objective("Defeat Data Xaldin",beastscastle.CheckLocation.DataXaldin,ObjectiveType.BOSS,ObjectiveDifficulty.LATEST),
        KH2Objective("Defeat Data Luxord",portroyal.CheckLocation.DataLuxordApBoost,ObjectiveType.BOSS,ObjectiveDifficulty.LATEST),
        KH2Objective("Defeat Data Xemnas",worldthatneverwas.CheckLocation.DataXemnas,ObjectiveType.BOSS,ObjectiveDifficulty.LATEST),
        KH2Objective("Defeat Data Zexion",olympuscoliseum.CheckLocation.DataZexionLostIllusion,ObjectiveType.BOSS,ObjectiveDifficulty.LATEST),
        KH2Objective("Defeat Data Vexen",halloweentown.CheckLocation.DataVexen,ObjectiveType.BOSS,ObjectiveDifficulty.LATEST),
        KH2Objective("Defeat Data Larxene",spaceparanoids.CheckLocation.DataLarxeneLostIllusion,ObjectiveType.BOSS,ObjectiveDifficulty.LATEST),
        KH2Objective("Defeat Data Lexaeus",agrabah.CheckLocation.DataLexaeus,ObjectiveType.BOSS,ObjectiveDifficulty.LATEST),
        KH2Objective("Defeat Data Marluxia",disneycastle.CheckLocation.DataMarluxiaLostIllusion,ObjectiveType.BOSS,ObjectiveDifficulty.LATEST),
        # AS
        KH2Objective("Defeat AS Zexion",olympuscoliseum.CheckLocation.ZexionBonus,ObjectiveType.BOSS,ObjectiveDifficulty.LATEST),
        KH2Objective("Defeat AS Vexen",halloweentown.CheckLocation.VexenBonus,ObjectiveType.BOSS,ObjectiveDifficulty.LATEST),
        KH2Objective("Defeat AS Larxene",spaceparanoids.CheckLocation.LarxeneBonus,ObjectiveType.BOSS,ObjectiveDifficulty.LATEST),
        KH2Objective("Defeat AS Lexaeus",agrabah.CheckLocation.LexaeusBonus,ObjectiveType.BOSS,ObjectiveDifficulty.LATEST),
        KH2Objective("Defeat AS Marluxia",disneycastle.CheckLocation.MarluxiaBonus,ObjectiveType.BOSS,ObjectiveDifficulty.LATEST),
        
    ]