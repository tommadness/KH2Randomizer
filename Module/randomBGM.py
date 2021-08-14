import random, os, zipfile

class RandomBGM():
    def randomizeBGM(options, platform):
        # JUST FOR TESTING
        options = {
            "games": ["KH2"],
            "options": []
        }

        if not platform == "PC" or len(options["games"]) < 1:
            return ""
        
        musicPaths = {
            "KH2": "bgm",
            "KH1": "..\\kh1\\TOBEFOUND",
            "BBS": "..\\bbs\\TOBEFOUND",
            "RECOM": "..\\recom\\TOBEFOUND",
            "CUSTOM": "..\\custom"
        }
        musicList = {
            "KH2": [
                {"name": "music050.win32.scd", "kind": "unknown"}, 
                {"name": "music051.win32.scd", "kind": "field"}, # Fragments of Sorrow
                {"name": "music052.win32.scd", "kind": "battle"}, # The Afternoon Streets
                {"name": "music053.win32.scd", "kind": "battle"}, # Working Together
                {"name": "music054.win32.scd", "kind": "battle"},
                {"name": "music055.win32.scd", "kind": "battle"}, #Deep Drive
                {"name": "music059.win32.scd", "kind": "battle"}, #A Fight to the Death
                {"name": "music060.win32.scd", "kind": "battle"}, #Darkness of the Unkown I
                {"name": "music061.win32.scd", "kind": "battle"}, #Darkness of the unknown II
                {"name": "music062.win32.scd", "kind": "battle"}, # Darkness of the Unknown III
                {"name": "music063.win32.scd", "kind": "battle"}, # The 13th Reflection
                {"name": "music064.win32.scd", "kind": "battle"}, #What a Surprise
                {"name": "music065.win32.scd", "kind": "battle"}, # Happy Holidays
                {"name": "music066.win32.scd", "kind": "battle"},  # The other Promise
                {"name": "music067.win32.scd", "kind": "battle"}, # Rage Awakened
                {"name": "music068.win32.scd", "kind": "battle"}, # Cavern of Remembrance
                {"name": "music069.win32.scd", "kind": "battle"}, # Deep Anxiety
                {"name": "music081.win32.scd", "kind": "battle"}, # Beneath the Ground
                {"name": "music082.win32.scd", "kind": "battle"}, # The Escapade
                {"name": "music084.win32.scd", "kind": "battle"}, # Arabian Daydream
                {"name": "music085.win32.scd", "kind": "battle"}, # Byte Striking
                {"name": "music086.win32.scd", "kind": "battle"}, # Spooks of Halloween Town
                {"name": "music087.win32.scd", "kind": "battle"}, # Disappeared
                {"name": "music088.win32.scd", "kind": "battle"}, # Sora's Theme
                {"name": "music089.win32.scd", "kind": "battle"}, # Friends in my heart
                {"name": "music090.win32.scd", "kind": "battle"}, # Riku's Theme
                {"name": "music091.win32.scd", "kind": "battle"}, #Kairi's Theme
                {"name": "music092.win32.scd", "kind": "battle"},# A Walk in Andante
                {"name": "music093.win32.scd", "kind": "battle"}, # Villain's of a Sort
                {"name": "music094.win32.scd", "kind": "battle"}, # Organization XIII
                {"name": "music095.win32.scd", "kind": "battle"}, # Apprehension
                {"name": "music096.win32.scd", "kind": "battle"}, # Courage
                {"name": "music097.win32.scd", "kind": "battle"}, # Laughter and Merriment
                {"name": "music098.win32.scd", "kind": "battle"}, # Hesitation
                {"name": "music099.win32.scd", "kind": "battle"}, # Missing You
                {"name": "music100.win32.scd", "kind": "battle"}, # The Underworld
                {"name": "music101.win32.scd", "kind": "battle"}, # Waltz of the Damned
                {"name": "music102.win32.scd", "kind": "battle"}, # What Lies Beneath
                {"name": "music103.win32.scd", "kind": "battle"}, # Olympus Coliseum
                {"name": "music104.win32.scd", "kind": "battle"}, # Dance of the Daring
                {"name": "music106.win32.scd", "kind": "battle", "dmca": True}, # Under the Sea
                {"name": "music107.win32.scd", "kind": "battle"}, # Ursula's Revenge
                {"name": "music108.win32.scd", "kind": "battle", "dmca": True}, # Part of your World
                {"name": "music109.win32.scd", "kind": "battle"}, # A New Day is Dawning
                {"name": "music110.win32.scd", "kind": "battle"}, # The Encounter
                {"name": "music111.win32.scd", "kind": "battle"}, # Sinister Shadows
                {"name": "music112.win32.scd", "kind": "battle"}, # Fields of Honor 
                {"name": "music113.win32.scd", "kind": "battle"}, # Swim This Way
                {"name": "music114.win32.scd", "kind": "battle"}, # Tension Rising
                {"name": "music115.win32.scd", "kind": "battle"}, # The Corrupted
                {"name": "music116.win32.scd", "kind": "battle"}, # The Home of Dragons
                {"name": "music117.win32.scd", "kind": "battle"}, # Rowdy Rumble
                {"name": "music118.win32.scd", "kind": "battle"}, # Lazy Afternoons
                {"name": "music119.win32.scd", "kind": "battle"}, # Sinister Sundown
                {"name": "music120.win32.scd", "kind": "battle"}, 
                {"name": "music121.win32.scd", "kind": "battle"}, # Desire for All That is Lost
                {"name": "music122.win32.scd", "kind": "battle"}, # Atlantica Tutorial I
                {"name": "music123.win32.scd", "kind": "battle"}, # Atlantica Tutorial II
                {"name": "music124.win32.scd", "kind": "battle"}, # Atlantica Tutorial II.5
                {"name": "music125.win32.scd", "kind": "battle"}, # Atlantica Tutorial Finish
                {"name": "music127.win32.scd", "kind": "battle"}, # A Day in Agrabah
                {"name": "music128.win32.scd", "kind": "battle"}, # Arabian Dream
                {"name": "music129.win32.scd", "kind": "battle"}, # Isn't It Lovely
                {"name": "music130.win32.scd", "kind": "battle"}, # Atlantica tutorials Combined
                {"name": "music131.win32.scd", "kind": "battle"}, # Dance to the Death 
                {"name": "music132.win32.scd", "kind": "battle", "dmca": True}, # Beauty and the Beast
                {"name": "music133.win32.scd", "kind": "battle"}, # Magical Mystery
                {"name": "music134.win32.scd", "kind": "battle"}, 
                {"name": "music135.win32.scd", "kind": "battle"}, # Space Paranoids Theme
                {"name": "music136.win32.scd", "kind": "battle"}, # Byte Bashing
                {"name": "music137.win32.scd", "kind": "battle"}, # A Twinkle in the Sky
                {"name": "music138.win32.scd", "kind": "battle"}, # Shipmeisters' Shanty
                {"name": "music139.win32.scd", "kind": "battle"}, # Gearing up
                {"name": "music141.win32.scd", "kind": "battle"}, # Winnie the Pooh Theme
                {"name": "music142.win32.scd", "kind": "battle"}, # Crossing the Finish Line
                {"name": "music143.win32.scd", "kind": "battle"}, # Mickey Mouse Club March
                {"name": "music144.win32.scd", "kind": "battle"}, # This is Halloween
                {"name": "music145.win32.scd", "kind": "battle"}, # Vim and Vigor
                {"name": "music146.win32.scd", "kind": "battle"}, # Roxas' Theme
                {"name": "music148.win32.scd", "kind": "battle"}, # Blast Off
                {"name": "music149.win32.scd", "kind": "battle"}, 
                {"name": "music151.win32.scd", "kind": "battle"}, # The 13th Struggle
                {"name": "music152.win32.scd", "kind": "battle"}, # Reviving Hallow Bastion
                {"name": "music153.win32.scd", "kind": "battle"}, # Scherzo Di Notte
                {"name": "music154.win32.scd", "kind": "battle"}, # Nights of the Cursed
                {"name": "music155.win32.scd", "kind": "battle"}, # He's a Pirate
                {"name": "music158.win32.scd", "kind": "battle"}, # Bounce-o-Rama
                {"name": "music159.win32.scd", "kind": "battle"}, # Bounce-o-Rama Ver 2
                {"name": "music164.win32.scd", "kind": "battle"}, # Road to a Hero
                {"name": "music185.win32.scd", "kind": "battle"}, # The 13th Dilemma
                {"name": "music186.win32.scd", "kind": "battle"}, # Adventures in the Savannah
                {"name": "music187.win32.scd", "kind": "battle"}, # Savannah Pride
                {"name": "music188.win32.scd", "kind": "battle"}, # One-Winged Angel
                {"name": "music189.win32.scd", "kind": "battle"}, # Monochrome Dreams
                {"name": "music190.win32.scd", "kind": "battle"}, # Old Friends, Old Rivals
                {"name": "music506.win32.scd", "kind": "battle", "dmca": True},
                {"name": "music507.win32.scd", "kind": "battle"},
                {"name": "music508.win32.scd", "kind": "battle", "dmca": True},
                {"name": "music509.win32.scd", "kind": "battle"},
                {"name": "music513.win32.scd", "kind": "battle"},
                {"name": "music517.win32.scd", "kind": "battle"},
                {"name": "music521.win32.scd", "kind": "battle"},
                {"name": "music530.win32.scd", "kind": "battle"}],
            "KH1": [
                {"name": "music097.win32.scd", "kind": "battle"},
                {"name": "music098.win32.scd", "kind": "battle"},
                {"name": "music099.win32.scd", "kind": "battle"},
                {"name": "music100.win32.scd", "kind": "battle"},
                {"name": "music101.win32.scd", "kind": "battle"},
                {"name": "music102.win32.scd", "kind": "battle"},
                {"name": "music103.win32.scd", "kind": "battle"},
                {"name": "music104.win32.scd", "kind": "battle"},
                {"name": "music105.win32.scd", "kind": "battle"},
                {"name": "music106.win32.scd", "kind": "battle"},
                {"name": "music107.win32.scd", "kind": "battle"},
                {"name": "music108.win32.scd", "kind": "battle"},
                {"name": "music109.win32.scd", "kind": "battle"},
                {"name": "music110.win32.scd", "kind": "battle"},
                {"name": "music111.win32.scd", "kind": "battle"},
                {"name": "music112.win32.scd", "kind": "battle"},
                {"name": "music113.win32.scd", "kind": "battle"},
                {"name": "music114.win32.scd", "kind": "battle"},
                {"name": "music115.win32.scd", "kind": "battle"},
                {"name": "music116.win32.scd", "kind": "battle"},
                {"name": "music117.win32.scd", "kind": "battle"},
                {"name": "music118.win32.scd", "kind": "battle"},
                {"name": "music119.win32.scd", "kind": "battle"},
                {"name": "music120.win32.scd", "kind": "battle"},
                {"name": "music121.win32.scd", "kind": "battle"},
                {"name": "music122.win32.scd", "kind": "battle"},
                {"name": "music123.win32.scd", "kind": "battle"},
                {"name": "music124.win32.scd", "kind": "battle"},
                {"name": "music125.win32.scd", "kind": "battle"},
                {"name": "music126.win32.scd", "kind": "battle"},
                {"name": "music127.win32.scd", "kind": "battle"},
                {"name": "music128.win32.scd", "kind": "battle"},
                {"name": "music129.win32.scd", "kind": "battle"},
                {"name": "music130.win32.scd", "kind": "battle"},
                {"name": "music131.win32.scd", "kind": "battle"},
                {"name": "music132.win32.scd", "kind": "battle"},
                {"name": "music137.win32.scd", "kind": "battle"},
                {"name": "music140.win32.scd", "kind": "battle"},
                {"name": "music141.win32.scd", "kind": "battle"},
                {"name": "music142.win32.scd", "kind": "battle"},
                {"name": "music143.win32.scd", "kind": "battle"},
                {"name": "music144.win32.scd", "kind": "battle"},
                {"name": "music145.win32.scd", "kind": "battle"},
                {"name": "music146.win32.scd", "kind": "battle"},
                {"name": "music147.win32.scd", "kind": "battle"},
                {"name": "music148.win32.scd", "kind": "battle"},
                {"name": "music149.win32.scd", "kind": "battle"},
                {"name": "music150.win32.scd", "kind": "battle"},
                {"name": "music151.win32.scd", "kind": "battle"},
                {"name": "music152.win32.scd", "kind": "battle"},
                {"name": "music153.win32.scd", "kind": "battle"},
                {"name": "music154.win32.scd", "kind": "battle"},
                {"name": "music155.win32.scd", "kind": "battle"},
                {"name": "music156.win32.scd", "kind": "battle"},
                {"name": "music157.win32.scd", "kind": "battle"},
                {"name": "music158.win32.scd", "kind": "battle"},
                {"name": "music159.win32.scd", "kind": "battle"},
                {"name": "music160.win32.scd", "kind": "battle"},
                {"name": "music161.win32.scd", "kind": "battle"},
                {"name": "music162.win32.scd", "kind": "battle"},
                {"name": "music163.win32.scd", "kind": "battle"},
                {"name": "music164.win32.scd", "kind": "battle"},
                {"name": "music165.win32.scd", "kind": "battle"},
                {"name": "music166.win32.scd", "kind": "battle"},
                {"name": "music167.win32.scd", "kind": "battle"},
                {"name": "music168.win32.scd", "kind": "battle"},
                {"name": "music169.win32.scd", "kind": "battle"},
                {"name": "music170.win32.scd", "kind": "battle"},
                {"name": "music171.win32.scd", "kind": "battle"},
                {"name": "music172.win32.scd", "kind": "battle"},
                {"name": "music173.win32.scd", "kind": "battle"},
                {"name": "music174.win32.scd", "kind": "battle"},
                {"name": "music175.win32.scd", "kind": "battle"},
                {"name": "music176.win32.scd", "kind": "battle"},
                {"name": "music177.win32.scd", "kind": "battle"},
                {"name": "music178.win32.scd", "kind": "battle"},
                {"name": "music179.win32.scd", "kind": "battle"},
                {"name": "music180.win32.scd", "kind": "battle"},
                {"name": "music181.win32.scd", "kind": "battle"},
                {"name": "music182.win32.scd", "kind": "battle"},
                {"name": "music183.win32.scd", "kind": "battle"},
                {"name": "music184.win32.scd", "kind": "battle"},
                {"name": "music185.win32.scd", "kind": "battle"},
                {"name": "music186.win32.scd", "kind": "battle"},
                {"name": "music187.win32.scd", "kind": "battle"},
                {"name": "music188.win32.scd", "kind": "battle"},
                {"name": "music189.win32.scd", "kind": "battle"},
                {"name": "music190.win32.scd", "kind": "battle"},
                {"name": "music191.win32.scd", "kind": "battle"},
                {"name": "music192.win32.scd", "kind": "battle"},
                {"name": "music193.win32.scd", "kind": "battle"},
                {"name": "music194.win32.scd", "kind": "battle"},
                {"name": "music196.win32.scd", "kind": "battle"},
                {"name": "music197.win32.scd", "kind": "battle"}
            ],
            "RECOM": [
                {"name": '01F_Town_B.win32.scd', "kind": "battle"},
                {"name": '01F_Town_F.win32.scd', "kind": "field"},
                {"name": '03F_Hercul.win32.scd', "kind": "field"},
                {"name": '03F_Hercules_B.win32.scd', "kind": "battle"},
                {"name": '12_Event_Yuttari.win32.scd', "kind": "field"},
                {"name": '13_Event_Namine.win32.scd', "kind": "field"},
                {"name": '14_Event_Odayaka.win32.scd', "kind": "field"},
                {"name": '15_Event_XIII.win32.scd', "kind": "field"},
                {"name": '16_XIIIBoss1.win32.scd', "kind": "battle"},
                {"name": '17_Halloween_F.win32.scd', "kind": "field"},
                {"name": '18_Helloween_B.win32.scd', "kind": "battle"},
                {"name": '19_Alice_Field.win32.scd', "kind": "field"},
                {"name": '20_Event_13thFloor.win32.scd', "kind": "field"},
                {"name": '21_Alice_Battle.win32.scd', "kind": "battle"},
                {"name": '22_PeterPan_Field.win32.scd', "kind": "field"},
                {"name": '23_PeterPan_Battle.win32.scd', "kind": "battle"},
                {"name": '24_Pinocchio_Field.win32.scd', "kind": "field"},
                {"name": '25_Aladdin_F.win32.scd', "kind": "field"},
                {"name": '26_Aladdin_B.win32.scd', "kind": "battle"},
                {"name": '27_Pinocchio_B.win32.scd', "kind": "battle"},
                {"name": '28_Forget_F.win32.scd', "kind": "field"},
                {"name": '29_Forget_B.win32.scd', "kind": "battle"},
                {"name": '30_Twilight_F.win32.scd', "kind": "field"},
                {"name": '31_Twilight_B.win32.scd', "kind": "battle"},
                {"name": '32_Destiny_F.win32.scd', "kind": "field"},
                {"name": '33_Destiny_B.win32.scd', "kind": "battle"},
                {"name": '34_Boss_RikuAnsem.win32.scd', "kind": "battle"},
                {"name": '35_Boss_NiseRiku.win32.scd', "kind": "battle"},
                {"name": '36_WinnieThePooh.win32.scd', "kind": "field"},
                {"name": '37_LastBoss1.win32.scd', "kind": "battle"},
                {"name": '38_UnderTheSea.win32.scd', "kind": "field"},
                {"name": '39_LittleMermaid_B.win32.scd', "kind": "battle"},
                {"name": '40_LastBoss2.win32.scd', "kind": "battle"},
                {"name": '41_LastBoss3.win32.scd', "kind": "battle"},
                {"name": '42_Hollow_F.win32.scd', "kind": "field"},
                {"name": '43_Hollow_B.win32.scd', "kind": "battle"},
                {"name": '44_PooGame1.win32.scd', "kind": "field"},
                {"name": '45_PoohGame2.win32.scd', "kind": "field"},
                {"name": 'Boss1.win32.scd', "kind": "battle"},
                {"name": 'Boss2_World.win32.scd', "kind": "battle"},
                {"name": 'Event1_Kinpak.win32.scd', "kind": "field"},
                {"name": 'Event2_.win32.scd', "kind": "field"},
                {"name": 'Event4.win32.scd', "kind": "field"},
                {"name": 'Event_Unrest.win32.scd', "kind": "field"},
                {"name": 'Title.win32.scd', "kind": "field"}
                ],
            "BBS": [
                {"name": "001sinde_f.win32.scd", "kind": "field"},
                {"name": "002sinde_b.win32.scd", "kind": "battle"},
                {"name": "003nemure_f.win32.scd", "kind": "field"},
                {"name": "004nemure_b.win32.scd", "kind": "battle"},
                {"name": "005syugyo_f.win32.scd", "kind": "field"},
                {"name": "006syugyo_b.win32.scd", "kind": "battle"},
                {"name": "007shira_f.win32.scd", "kind": "field"},
                {"name": "008shira_b.win32.scd", "kind": "battle"},
                {"name": "009raydi_f.win32.scd", "kind": "field"},
                {"name": "010raydi_b.win32.scd", "kind": "battle"},
                {"name": "011distow_f.win32.scd", "kind": "field"},
                {"name": "012distow_b.win32.scd", "kind": "battle"},
                {"name": "013never_f.win32.scd", "kind": "field"},
                {"name": "014never_b.win32.scd", "kind": "battle"},
                {"name": "015herc_f.win32.scd", "kind": "field"},
                {"name": "016herc_b.win32.scd", "kind": "battle"},
                {"name": "017riro_f.win32.scd", "kind": "field"},
                {"name": "018riro_b.win32.scd", "kind": "battle"},
                {"name": "019iensid_f.win32.scd", "kind": "field"},
                {"name": "020iensid_b.win32.scd", "kind": "battle"},
                {"name": "021kouya_f.win32.scd", "kind": "field"},
                {"name": "022disice_f.win32.scd", "kind": "field"},
                {"name": "023tsusin_f.win32.scd", "kind": "field"},
                {"name": "030youki.win32.scd", "kind": "field"},
                {"name": "031isamashi.win32.scd", "kind": "field"},
                {"name": "032odayaka.win32.scd", "kind": "field"},
                {"name": "033fuon.win32.scd", "kind": "field"},
                {"name": "034kanasii.win32.scd", "kind": "field"},
                {"name": "035kinpaku.win32.scd", "kind": "field"},
                {"name": "036seisin.win32.scd", "kind": "field"},
                {"name": "037yami.win32.scd", "kind": "field"},
                {"name": "038ria_deai.win32.scd", "kind": "field"},
                {"name": "040anba_b1.win32.scd", "kind": "battle"},
                {"name": "041anba_b2.win32.scd", "kind": "battle"},
                {"name": "042dis_b1.win32.scd", "kind": "battle"},
                {"name": "043dis_b2.win32.scd", "kind": "battle"},
                {"name": "044vanita_b.win32.scd", "kind": "battle"},
                {"name": "045anthem_b.win32.scd", "kind": "battle"},
                {"name": "046last_b1.win32.scd", "kind": "battle"},
                {"name": "047last_b2.win32.scd", "kind": "battle"},
                {"name": "048hanyo_b1.win32.scd", "kind": "battle"},
                {"name": "049hanyo_b2.win32.scd", "kind": "battle"},
                {"name": "050title.win32.scd", "kind": "field"},
                {"name": "051worldmap.win32.scd", "kind": "field"},
                {"name": "060tera.win32.scd", "kind": "field"},
                {"name": "061aqua.win32.scd", "kind": "field"},
                {"name": "062ven.win32.scd", "kind": "field"},
                {"name": "063kairi1.win32.scd", "kind": "field"},
                {"name": "066peet.win32.scd", "kind": "field"},
                {"name": "067disvill.win32.scd", "kind": "field"},
                {"name": "068zea.win32.scd", "kind": "field"},
                {"name": "069braig.win32.scd", "kind": "field"},
                {"name": "070key_l.win32.scd", "kind": "field"},
                {"name": "071key_d.win32.scd", "kind": "field"},
                {"name": "072key_l_d.win32.scd", "kind": "field"},
                {"name": "073kizuna.win32.scd", "kind": "field"},
                {"name": "074zack.win32.scd", "kind": "field"},
                {"name": "100ice1_128.win32.scd", "kind": "field"},
                {"name": "101ice1_132.win32.scd", "kind": "field"},
                {"name": "102ice_2.win32.scd", "kind": "field"},
                {"name": "103fruit.win32.scd", "kind": "field"},
                {"name": "104dice.win32.scd", "kind": "field"},
                {"name": "105poomini.win32.scd", "kind": "field"},
                {"name": "106cartrace.win32.scd", "kind": "field"},
                {"name": "107syugyo.win32.scd", "kind": "field"},
                {"name": "108riro.win32.scd", "kind": "field"},
                {"name": "109training.win32.scd", "kind": "field"},
                {"name": "110han_bt1.win32.scd", "kind": "battle"},
                {"name": "111han_bt2.win32.scd", "kind": "battle"},
                {"name": "112rage_bt.win32.scd", "kind": "battle"},
                {"name": "113kh1tit.win32.scd", "kind": "field"},
                {"name": "114raceview.win32.scd", "kind": "field"},
                {"name": "115boss.win32.scd", "kind": "battle"},
                {"name": "116icon.win32.scd", "kind": "field"},
                {"name": "117short_l2.win32.scd", "kind": "field"},
                {"name": "118gumi.win32.scd", "kind": "field"},
                {"name": "119desti.win32.scd", "kind": "field"},
                {"name": "120hand.win32.scd", "kind": "field"},
                {"name": "122nazono.win32.scd", "kind": "field"},
                {"name": "123rev.win32.scd", "kind": "field"},
                {"name": "124dp_amb.win32.scd", "kind": "field"},
                {"name": "125yami_f.win32.scd", "kind": "field"},
                {"name": "126yami_b.win32.scd", "kind": "battle"},
                {"name": "127Xeha_b.win32.scd", "kind": "battle"},
                {"name": "128Eraqu_b.win32.scd", "kind": "battle"},
                {"name": "129Pure_b.win32.scd", "kind": "battle"},
                {"name": "130Mons_b.win32.scd", "kind": "battle"}
            ],
        }
        BGMList = {"battle": [], "field": []}
        for game in options["games"]:
            for song in musicList[game]:
                if "DMCA-SAFE" in options["options"] and song.get("dmca", False):
                    continue
                kind = "battle" # default
                if "Randomize Field and Battle Music Separately" in options["options"]:
                    kind = song.get("kind", "battle")
                song["game"] = game
                BGMList[kind].append(song)

        def _getMusicAsset(original_song, new_song):
            return {
                "name": "bgm\\{original}".format(original=original_song["name"]),
                "method": "copy",
                "source": [{"name": "{newPath}\\{newBGM}".format(newPath = musicPaths[new_song["game"]], newBGM = new_song["name"]), "type":"internal"}]
            }

        shuffledBattle = BGMList["battle"][:]
        shuffledField = BGMList["field"][:]
        random.shuffle(shuffledBattle)
        random.shuffle(shuffledField)
        numBattle = 0
        numField = 0
        BGMAssets = []
        for i in range(len(musicList["KH2"])):
            original_song = musicList["KH2"][i]
            kind = original_song.get("kind", "battle")

            if "Randomize Field and Battle Music Separately" in options["options"] and kind == "field":
                new_song = shuffledField[numField % len(shuffledField)]
                numField += 1
            else:
                new_song = shuffledBattle[numBattle % len(shuffledBattle)]
                numBattle += 1

            BGMAssets.append(_getMusicAsset(original_song, new_song))
        return BGMAssets

    def getOptions():
        return [
            "DMCA-SAFE",
            "Randomize Field and Battle Music Separately"
        ]

    def getGames():
        return [
            "KH2",
            "KH1",
            "BBS",
            "RECOM",  
            "Custom"
        ]
