import random, os, zipfile

musicList = {
    "KH2": [
        {"name": "music050.win32.scd", "kind": "unknown"}, 
        {"name": "music051.win32.scd", "kind": "field"}, # Fragments of Sorrow
        {"name": "music052.win32.scd", "kind": "field"}, # The Afternoon Streets
        {"name": "music053.win32.scd", "kind": "battle"}, # Working Together
        {"name": "music054.win32.scd", "kind": "unknown"},
        {"name": "music055.win32.scd", "kind": "battle"}, #Deep Drive
        {"name": "music059.win32.scd", "kind": "battle"}, #A Fight to the Death
        {"name": "music060.win32.scd", "kind": "battle"}, #Darkness of the Unknown I
        {"name": "music061.win32.scd", "kind": "battle"}, #Darkness of the unknown II
        {"name": "music062.win32.scd", "kind": "battle"}, # Darkness of the Unknown III
        {"name": "music063.win32.scd", "kind": "battle"}, # The 13th Reflection
        {"name": "music064.win32.scd", "kind": "field"}, #What a Surprise
        {"name": "music065.win32.scd", "kind": "battle"}, # Happy Holidays
        {"name": "music066.win32.scd", "kind": "battle"},  # The other Promise
        {"name": "music067.win32.scd", "kind": "battle"}, # Rage Awakened
        {"name": "music068.win32.scd", "kind": "field"}, # Cavern of Remembrance
        {"name": "music069.win32.scd", "kind": "battle"}, # Deep Anxiety
        {"name": "music081.win32.scd", "kind": "battle"}, # Beneath the Ground
        {"name": "music082.win32.scd", "kind": "field"}, # The Escapade
        {"name": "music084.win32.scd", "kind": "battle"}, # Arabian Daydream
        {"name": "music085.win32.scd", "kind": "battle"}, # Byte Striking
        {"name": "music086.win32.scd", "kind": "battle"}, # Spooks of Halloween Town
        {"name": "music087.win32.scd", "kind": "battle"}, # Disappeared
        {"name": "music088.win32.scd", "kind": "field"}, # Sora's Theme
        {"name": "music089.win32.scd", "kind": "field"}, # Friends in my heart
        {"name": "music090.win32.scd", "kind": "field"}, # Riku's Theme
        {"name": "music091.win32.scd", "kind": "field"}, #Kairi's Theme
        {"name": "music092.win32.scd", "kind": "field"},# A Walk in Andante
        {"name": "music093.win32.scd", "kind": "field"}, # Villain's of a Sort
        {"name": "music094.win32.scd", "kind": "field"}, # Organization XIII
        {"name": "music095.win32.scd", "kind": "battle"}, # Apprehension
        {"name": "music096.win32.scd", "kind": "battle"}, # Courage
        {"name": "music097.win32.scd", "kind": "field"}, # Laughter and Merriment
        {"name": "music098.win32.scd", "kind": "field"}, # Hesitation
        {"name": "music099.win32.scd", "kind": "field"}, # Missing You
        {"name": "music100.win32.scd", "kind": "field"}, # The Underworld
        {"name": "music101.win32.scd", "kind": "battle"}, # Waltz of the Damned
        {"name": "music102.win32.scd", "kind": "battle"}, # What Lies Beneath
        {"name": "music103.win32.scd", "kind": "battle"}, # Olympus Coliseum
        {"name": "music104.win32.scd", "kind": "battle"}, # Dance of the Daring
        {"name": "music106.win32.scd", "kind": "field", "dmca": True}, # Under the Sea
        {"name": "music107.win32.scd", "kind": "battle"}, # Ursula's Revenge
        {"name": "music108.win32.scd", "kind": "field", "dmca": True}, # Part of your World
        {"name": "music109.win32.scd", "kind": "field"}, # A New Day is Dawning
        {"name": "music110.win32.scd", "kind": "battle"}, # The Encounter
        {"name": "music111.win32.scd", "kind": "battle"}, # Sinister Shadows
        {"name": "music112.win32.scd", "kind": "battle"}, # Fields of Honor 
        {"name": "music113.win32.scd", "kind": "field"}, # Swim This Way
        {"name": "music114.win32.scd", "kind": "battle"}, # Tension Rising
        {"name": "music115.win32.scd", "kind": "battle"}, # The Corrupted
        {"name": "music116.win32.scd", "kind": "field"}, # The Home of Dragons
        {"name": "music117.win32.scd", "kind": "battle"}, # Rowdy Rumble
        {"name": "music118.win32.scd", "kind": "field"}, # Lazy Afternoons
        {"name": "music119.win32.scd", "kind": "battle"}, # Sinister Sundown
        {"name": "music120.win32.scd", "kind": "unknown"}, 
        {"name": "music121.win32.scd", "kind": "field"}, # Desire for All That is Lost
        {"name": "music122.win32.scd", "kind": "field"}, # Atlantica Tutorial I
        {"name": "music123.win32.scd", "kind": "field"}, # Atlantica Tutorial II
        {"name": "music124.win32.scd", "kind": "field"}, # Atlantica Tutorial II.5
        {"name": "music125.win32.scd", "kind": "field"}, # Atlantica Tutorial Finish
        {"name": "music127.win32.scd", "kind": "field"}, # A Day in Agrabah
        {"name": "music128.win32.scd", "kind": "battle"}, # Arabian Dream
        {"name": "music129.win32.scd", "kind": "field"}, # Isn't It Lovely
        {"name": "music130.win32.scd", "kind": "field"}, # Atlantica tutorials Combined
        {"name": "music131.win32.scd", "kind": "battle"}, # Dance to the Death 
        {"name": "music132.win32.scd", "kind": "field", "dmca": True}, # Beauty and the Beast
        {"name": "music133.win32.scd", "kind": "field"}, # Magical Mystery
        {"name": "music134.win32.scd", "kind": "unknown"}, 
        {"name": "music135.win32.scd", "kind": "field"}, # Space Paranoids Theme
        {"name": "music136.win32.scd", "kind": "battle"}, # Byte Bashing
        {"name": "music137.win32.scd", "kind": "field"}, # A Twinkle in the Sky
        {"name": "music138.win32.scd", "kind": "field"}, # Shipmeisters' Shanty
        {"name": "music139.win32.scd", "kind": "field"}, # Gearing up
        {"name": "music141.win32.scd", "kind": "field"}, # Winnie the Pooh Theme
        {"name": "music142.win32.scd", "kind": "field"}, # Crossing the Finish Line
        {"name": "music143.win32.scd", "kind": "field"}, # Mickey Mouse Club March
        {"name": "music144.win32.scd", "kind": "field"}, # This is Halloween
        {"name": "music145.win32.scd", "kind": "battle"}, # Vim and Vigor
        {"name": "music146.win32.scd", "kind": "battle"}, # Roxas' Theme
        {"name": "music148.win32.scd", "kind": "field"}, # Blast Off
        {"name": "music149.win32.scd", "kind": "unknown"}, 
        {"name": "music151.win32.scd", "kind": "battle"}, # The 13th Struggle
        {"name": "music152.win32.scd", "kind": "field"}, # Reviving Hallow Bastion
        {"name": "music153.win32.scd", "kind": "battle"}, # Scherzo Di Notte
        {"name": "music154.win32.scd", "kind": "field"}, # Nights of the Cursed
        {"name": "music155.win32.scd", "kind": "battle"}, # He's a Pirate
        {"name": "music158.win32.scd", "kind": "field"}, # Bounce-o-Rama
        {"name": "music159.win32.scd", "kind": "field"}, # Bounce-o-Rama Ver 2
        {"name": "music164.win32.scd", "kind": "field"}, # Road to a Hero
        {"name": "music185.win32.scd", "kind": "battle"}, # The 13th Dilemma
        {"name": "music186.win32.scd", "kind": "field"}, # Adventures in the Savannah
        {"name": "music187.win32.scd", "kind": "battle"}, # Savannah Pride
        {"name": "music188.win32.scd", "kind": "battle"}, # One-Winged Angel
        {"name": "music189.win32.scd", "kind": "field"}, # Monochrome Dreams
        {"name": "music190.win32.scd", "kind": "battle"}, # Old Friends, Old Rivals
        {"name": "music506.win32.scd", "kind": "field", "dmca": True},
        {"name": "music507.win32.scd", "kind": "field"},
        {"name": "music508.win32.scd", "kind": "field", "dmca": True},
        {"name": "music509.win32.scd", "kind": "field"},
        {"name": "music513.win32.scd", "kind": "field"},
        {"name": "music517.win32.scd", "kind": "field"},
        {"name": "music521.win32.scd", "kind": "field"},
        {"name": "music530.win32.scd", "kind": "field"}],
    "KH1": [
        #some music in kh1 is found in .dat folders and others in .bgm folders and somtimes both.
        #the ones in both .dat and .bgm folders are duplicates so you can ignore one of those.
        {"name": "music099.bgm\\music099.win32.scd", "kind": "battle"},#Dissapeared
        {"name": "music101.dat\\music101.win32.scd", "kind": "field"}, #Deep Jungle
        {"name": "music102.dat\\music102.win32.scd", "kind": "battle"}, #Having a Wild Time
        {"name": "music103.bgm\\music103.win32.scd", "kind": "field"}, #Olympus Coliseum
        {"name": "music104.dat\\music104.win32.scd", "kind": "field"}, #Traverse Town
        {"name": "music105.dat\\music105.win32.scd", "kind": "field"}, #Destiny Islands
        {"name": "music110.bgm\\music110.win32.scd", "kind": "unknown"}, #Dearly Beloved
        {"name": "music111.bgm\\music111.win32.scd", "kind": "battle"}, #Shrouding Dark Cloud
        {"name": "music112.dat\\music112.win32.scd", "kind": "unknown"}, #Hand In Hand
        {"name": "music114.bgm\\music114.win32.scd", "kind": "unknown"}, #Unknown 1 [Heartless Has Come, Pt.3]
        {"name": "music116.dat\\music116.win32.scd", "kind": "field"}, #Welcome To Wonderland
        {"name": "music117.dat\\music117.win32.scd", "kind": "field"}, #A Very Small Wish
        {"name": "music118.bgm\\music118.win32.scd", "kind": "battle"}, #To Our Surprise
        {"name": "music119.dat\\music119.win32.scd", "kind": "battle"}, #Busting Up On The Beach
        {"name": "music120.bgm\\music120.win32.scd", "kind": "battle"}, #Go For It
        {"name": "music121.dat\\music121.win32.scd", "kind": "battle"}, #Monstrous Monstro
        {"name": "music122.dat\\music122.win32.scd", "kind": "unknown"}, #Blast Away Gummi Ship I
        {"name": "music123.dat\\music123.win32.scd", "kind": "unknown"}, #Blast Away Gummi Ship II
        {"name": "music124.dat\\music124.win32.scd", "kind": "unknown"}, #Shipmeisters Humoresque
        {"name": "music125.dat\\music125.win32.scd", "kind": "unknown"}, #Precious Stars In The Sky
        {"name": "music127.dat\\music127.win32.scd", "kind": "field"}, #A Day In Agrabah
        {"name": "music128.dat\\music128.win32.scd", "kind": "battle"}, #Arabian Dream
        {"name": "music129.dat\\music129.win32.scd", "kind": "field"}, #Captain Hook Pirate Ship
        {"name": "music130.dat\\music130.win32.scd", "kind": "field"}, #Never Land Sky
        {"name": "music131.dat\\music131.win32.scd", "kind": "battle"}, #Night Of Fate
        {"name": "music140.dat\\music140.win32.scd", "kind": "field"}, #Under The Sea
        {"name": "music141.dat\\music141.win32.scd", "kind": "field"}, #Winnie The Pooh
        {"name": "music142.bgm\\music142.win32.scd", "kind": "unknown"}, #Dive Into The Heart (Part 9)
        {"name": "music143.bgm\\music143.win32.scd", "kind": "field"}, #Mickey Mouse Club March
        {"name": "music144.dat\\music144.win32.scd", "kind": "field"}, #This Is Halloween
        {"name": "music145.bgm\\music145.win32.scd", "kind": "battle"}, #Destiny Force
        {"name": "music146.dat\\music146.win32.scd", "kind": "battle"}, #Pirate Gigue
        {"name": "music147.dat\\music147.win32.scd", "kind": "battle"}, #An Adventure In Atlantica
        {"name": "music148.dat\\music148.win32.scd", "kind": "unknown"}, #Blast Away Gummi Ship III
        {"name": "music149.dat\\music149.win32.scd", "kind": "battle"}, #Spooks Of Halloween Town
        {"name": "music150.bgm\\music150.win32.scd", "kind": "battle"}, #Squirming Evil
        {"name": "music151.bgm\\music151.win32.scd", "kind": "battle"}, #The Deep End
        {"name": "music152.dat\\music152.win32.scd", "kind": "field"}, #Hollow Bastion
        {"name": "music153.dat\\music153.win32.scd", "kind": "battle"}, #Scherzo Di Notte
        {"name": "music154.dat\\music154.win32.scd", "kind": "field"}, #End Of The World
        {"name": "music155.dat\\music155.win32.scd", "kind": "battle"}, #Fragments Of Sorrow
        {"name": "music156.bgm\\music156.win32.scd", "kind": "battle"}, #Guardando Nel Buio
        {"name": "music157.bgm\\music157.win32.scd", "kind": "unknown"}, #Holy Bananas
        {"name": "music158.bgm\\music158.win32.scd", "kind": "unknown"}, #Bounce-O-Rama
        {"name": "music160.bgm\\music160.win32.scd", "kind": "unknown"}, #Kairi I
        {"name": "music161.bgm\\music161.win32.scd", "kind": "unknown"}, #Kairi II
        {"name": "music162.bgm\\music162.win32.scd", "kind": "unknown"}, #Villains Of A Sort (Short)
        {"name": "music163.bgm\\music163.win32.scd", "kind": "unknown"}, #Villains Of A Sort 
        {"name": "music164.bgm\\music164.win32.scd", "kind": "battle"}, #Road To Hero
        {"name": "music165.bgm\\music165.win32.scd", "kind": "field"}, #This Is Halloween (Alternative)
        {"name": "music170.bgm\\music170.win32.scd", "kind": "unknown"}, #A Piece Of Peace
        {"name": "music172.bgm\\music172.win32.scd", "kind": "unknown"}, #A Walk In Adante
        {"name": "music173.bgm\\music173.win32.scd", "kind": "unknown"}, #No Time To Think
        {"name": "music174.bgm\\music174.win32.scd", "kind": "unknown"}, #An Intense Situation
        {"name": "music176.bgm\\music176.win32.scd", "kind": "unknown"}, #Friends In My Heart
        {"name": "music178.bgm\\music178.win32.scd", "kind": "unknown"}, #Treasured Memories
        {"name": "music180.bgm\\music180.win32.scd", "kind": "unknown"}, #Kairi III
        {"name": "music184.bgm\\music184.win32.scd", "kind": "unknown"}, #Merlin Magical House
        {"name": "music185.bgm\\music185.win32.scd", "kind": "battle"}, #Forze Del Male
        {"name": "music187.bgm\\music187.win32.scd", "kind": "unknown"}, #Just An Itty Bitty Too Much
        {"name": "music188.bgm\\music188.win32.scd", "kind": "unknown"}, #It Began With A Letter
        {"name": "music193.bgm\\music193.win32.scd", "kind": "unknown"}, #Dearly Beloved Reprise       
        {"name": "music196.bgm\\music196.win32.scd", "kind": "battle"}, #One Winged Angel
        {"name": "music197.bgm\\music197.win32.scd", "kind": "battle"} #Night On Blad Mountain
        #a few of the no intro duplicates removed along with BGMs that are short and don't loop.
        #{"name": "music194.bgm\\music194.win32.scd", "kind": "battle"}, #Guardando Nel Buio (No Intro)
        #{"name": "music097.bgm\\music097.win32.scd", "kind": "battle"}, #Dissapeared (No Intro)
        #{"name": "music098.bgm\\music098.win32.scd", "kind": "battle"}, #One Winged Angel (No Intro)
        #{"name": "music106.bgm\\music106.win32.scd", "kind": "unknown"}, #Where Is This (Part 1) (no loop)
        #{"name": "music107.bgm\\music107.win32.scd", "kind": "unknown"}, #Where Is This (Part 2) (no loop)
        #{"name": "music108.bgm\\music108.win32.scd", "kind": "unknown"}, #Where Is This (Part 3b) (no loop)
        #{"name": "music109.bgm\\music109.win32.scd", "kind": "unknown"}, #Where Is This (Part 4) (no loop)
        #{"name": "music113.bgm\\music113.win32.scd", "kind": "unknown"}, #The Heartless Has Come [Heartless Has Come, Pt.1] (no loop)
        #{"name": "music115.bgm\\music115.win32.scd", "kind": "unknown"}, #Where Is This (Part 3a) [Heartless Has Come, Pt.2] (no loop)
        #{"name": "music126.bgm\\music126.win32.scd", "kind": "unknown"}, #Turning The Key (no loop)
        #{"name": "music132.bgm\\music132.win32.scd", "kind": "unknown"}, #Dive Into The Heart (Parts 1-8) (would this actually work? there are 8 tracks in 1 here)
        #{"name": "music159.bgm\\music159.win32.scd", "kind": "unknown"}, #Once Upon a Time (no loop)
        #{"name": "music166.bgm\\music166.win32.scd", "kind": "unknown"}, #Strange Whispers (Part 5) (no loop)
        #{"name": "music167.bgm\\music167.win32.scd", "kind": "unknown"}, #Strange Whispers (Part 1) (no loop)
        #{"name": "music168.bgm\\music168.win32.scd", "kind": "unknown"}, #Strange Whispers
        #{"name": "music169.bgm\\music169.win32.scd", "kind": "unknown"}, #Strange Whispers (Part 3) (no loop)
        #{"name": "music171.bgm\\music171.win32.scd", "kind": "unknown"}, #Strange Whispers (Part 4) (no loop)
        #{"name": "music175.bgm\\music175.win32.scd", "kind": "unknown"}, #Unknown 3 [Kairi In Cabin] (no loop)
        #{"name": "music177.bgm\\music177.win32.scd", "kind": "unknown"}, #Tricksy Clock (no loop)
        #{"name": "music179.bgm\\music179.win32.scd", "kind": "unknown"}, #Miracle (no loop)
        #{"name": "music181.bgm\\music181.win32.scd", "kind": "unknown"}, #Hikari [Sora's Sacrifice] (no loop)
        #{"name": "music182.bgm\\music182.win32.scd", "kind": "unknown"}, #Mickey Mouse Club March (Intro) [Queen's Castle Drumroll] (no loop)
        #{"name": "music183.bgm\\music183.win32.scd", "kind": "unknown"}, #Oopsy-Daisy (no loop)
        #{"name": "music186.bgm\\music186.win32.scd", "kind": "unknown"}, #Unknown 2 [Plenty Of Hunny!] (no loop)
        #{"name": "music189.bgm\\music189.win32.scd", "kind": "unknown"}, #Blast Away Gummi Ship I (Sting 2) (no loop)
        #{"name": "music190.bgm\\music190.win32.scd", "kind": "unknown"}, #Blast Away Gummi Ship I (Sting) (no loop)
        #{"name": "music191.bgm\\music191.win32.scd", "kind": "unknown"}, #Beyond The Door (no loop)
        #{"name": "music192.bgm\\music192.win32.scd", "kind": "unknown"}, #Always On My Mind (Final Mix Version) (no loop)
        #{"name": "music100.win32.scd", "kind": "unknown"}, #empty 1kb file
        #{"name": "music137.win32.scd", "kind": "unknown"}, #empty 1kb file

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
        {"name": 'Title.win32.scd', "kind": "field"}],
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
        {"name": "130Mons_b.win32.scd", "kind": "battle"}],
    "DDD": [
        {"name": "bgm_001.win32.scd", "kind": "field"},
		{"name": "bgm_002.win32.scd", "kind": "field"},
		{"name": "bgm_003.win32.scd", "kind": "field"},
		{"name": "bgm_004.win32.scd", "kind": "field"},
		{"name": "bgm_005.win32.scd", "kind": "field"},
		{"name": "bgm_006.win32.scd", "kind": "field"},
		{"name": "bgm_007.win32.scd", "kind": "field"},
		{"name": "bgm_008.win32.scd", "kind": "battle"},
		{"name": "bgm_009.win32.scd", "kind": "field"},
		{"name": "bgm_010.win32.scd", "kind": "field"},
		{"name": "bgm_011.win32.scd", "kind": "field"},
		{"name": "bgm_012.win32.scd", "kind": "field"},
		{"name": "bgm_013.win32.scd", "kind": "field"},
		{"name": "bgm_014.win32.scd", "kind": "battle"},
		{"name": "bgm_015.win32.scd", "kind": "battle"},
		{"name": "bgm_016.win32.scd", "kind": "battle"},
		{"name": "bgm_017.win32.scd", "kind": "battle"},
		{"name": "bgm_018.win32.scd", "kind": "battle"},
		{"name": "bgm_019.win32.scd", "kind": "battle"},
		{"name": "bgm_020.win32.scd", "kind": "battle"},
		{"name": "bgm_021.win32.scd", "kind": "battle"},
		{"name": "bgm_022.win32.scd", "kind": "battle"},
		{"name": "bgm_023.win32.scd", "kind": "battle"},
		{"name": "bgm_024.win32.scd", "kind": "battle"},
		{"name": "bgm_025.win32.scd", "kind": "battle"},
		{"name": "bgm_026.win32.scd", "kind": "battle"},
		{"name": "bgm_027.win32.scd", "kind": "battle"},
		{"name": "bgm_028.win32.scd", "kind": "battle"},
		{"name": "bgm_029.win32.scd", "kind": "battle"},
		{"name": "bgm_030.win32.scd", "kind": "battle"},
		{"name": "bgm_031.win32.scd", "kind": "battle"},
		{"name": "bgm_032.win32.scd", "kind": "battle"},
		{"name": "bgm_033.win32.scd", "kind": "battle"},
		{"name": "bgm_034.win32.scd", "kind": "battle"},
		{"name": "bgm_035.win32.scd", "kind": "field"},
		{"name": "bgm_036.win32.scd", "kind": "field"},
		{"name": "bgm_037.win32.scd", "kind": "unknown"},
		{"name": "bgm_038.win32.scd", "kind": "unknown"},
		{"name": "bgm_039.win32.scd", "kind": "unknown"},
		{"name": "bgm_040.win32.scd", "kind": "unknown"},
		{"name": "bgm_041.win32.scd", "kind": "unknown"},
		{"name": "bgm_042.win32.scd", "kind": "unknown"},
		{"name": "bgm_043.win32.scd", "kind": "unknown"},
		{"name": "bgm_044.win32.scd", "kind": "unknown"},
		{"name": "bgm_045.win32.scd", "kind": "unknown"},
		{"name": "bgm_046.win32.scd", "kind": "unknown"},
		{"name": "bgm_047.win32.scd", "kind": "unknown"},
		{"name": "bgm_048.win32.scd", "kind": "unknown"},
		{"name": "bgm_050.win32.scd", "kind": "unknown"},
		{"name": "bgm_051.win32.scd", "kind": "unknown"},
		{"name": "bgm_052.win32.scd", "kind": "unknown"},
		{"name": "bgm_053.win32.scd", "kind": "battle"},
		{"name": "bgm_059.win32.scd", "kind": "unknown"},
		{"name": "bgm_060.win32.scd", "kind": "unknown"},
		{"name": "bgm_061.win32.scd", "kind": "unknown"},
		{"name": "bgm_062.win32.scd", "kind": "unknown"},
		{"name": "bgm_063.win32.scd", "kind": "unknown"},
		{"name": "bgm_065.win32.scd", "kind": "unknown"},
		{"name": "bgm_066.win32.scd", "kind": "unknown"},
		{"name": "bgm_067.win32.scd", "kind": "unknown"},
		{"name": "bgm_068.win32.scd", "kind": "battle"}, #twister -kingdom mix-
		{"name": "bgm_069.win32.scd", "kind": "battle"}, #calling -kingdom mix-
		{"name": "bgm_070.win32.scd", "kind": "unknown"},
		{"name": "bgm_071.win32.scd", "kind": "unknown"},
		{"name": "bgm_072.win32.scd", "kind": "unknown"},
		{"name": "bgm_073.win32.scd", "kind": "unknown"},
		{"name": "bgm_074.win32.scd", "kind": "unknown"},
		{"name": "bgm_075.win32.scd", "kind": "unknown"},
		{"name": "bgm_076.win32.scd", "kind": "unknown"},
		{"name": "bgm_077.win32.scd", "kind": "unknown"},
		{"name": "bgm_078.win32.scd", "kind": "unknown"},
		{"name": "bgm_083.win32.scd", "kind": "unknown"},
		{"name": "bgm_084.win32.scd", "kind": "unknown"},
		{"name": "bgm_085.win32.scd", "kind": "field"},
		{"name": "bgm_086.win32.scd", "kind": "battle"},
		{"name": "bgm_087.win32.scd", "kind": "battle"},
		{"name": "bgm_088.win32.scd", "kind": "battle"},
		{"name": "bgm_089.win32.scd", "kind": "field"},
		{"name": "bgm_091.win32.scd", "kind": "battle"},
		{"name": "bgm_093.win32.scd", "kind": "battle"},
		{"name": "bgm_094.win32.scd", "kind": "battle"},
		{"name": "bgm_095.win32.scd", "kind": "unknown"},
		{"name": "bgm_096.win32.scd", "kind": "unknown"},
		{"name": "bgm_097.win32.scd", "kind": "unknown"},
		{"name": "bgm_098.win32.scd", "kind": "battle"}, #twister
		{"name": "bgm_099.win32.scd", "kind": "battle"}, #calling
		{"name": "bgm_112.win32.scd", "kind": "unknown"},
		{"name": "bgm_113.win32.scd", "kind": "unknown"},
		{"name": "bgm_114.win32.scd", "kind": "unknown"},
		{"name": "bgm_115.win32.scd", "kind": "unknown"},
		{"name": "bgm_116.win32.scd", "kind": "battle"}],
}

musicPaths = {
    "KH2": "bgm",
    "KH1": "..\\kh1\\remastered\\amusic",
    "BBS": "..\\bbs\\sound\\win\\bgm",
    "RECOM": "..\\recom\\STREAM\\0001",
    "DDD": "..\\ddd\\sound\\jp\\output\\BGM",
    "CUSTOM": "..\\custom"
}
class RandomBGM():
    @staticmethod
    def randomizeBGM(selections, platform):
        options = {
            "games": [s for s in selections if s in musicList or s.startswith("CUSTOM")],
            "options": [s for s in selections if not (s in musicList or s.startswith("CUSTOM"))]
        }
        if not platform == "PC" or len(options["games"]) < 1:
            return ""
        
        BGMList = {"battle": [], "field": []}
        for game in options["games"]:
            if game.startswith("CUSTOM"):
                nsongs = int(game.split(" ")[-1]) 
                for i in range(nsongs):
                    kind = "battle" # default
                    if "Randomize Field and Battle Music Separately" in options["options"]:
                        kind = random.choice(["field", "battle"])
                    BGMList[kind].append({"name": "custom_{}.scd".format(i), "kind": kind, "game": "CUSTOM"})
            else:
                for song in musicList[game]:
                    if "DMCA-SAFE" in options["options"] and song.get("dmca", False):
                        continue
                    kind = "battle" # default
                    if "Randomize Field and Battle Music Separately" in options["options"]:
                        kind = song.get("kind", "battle")
                    if kind == "unknown":
                        kind = random.choice(["field", "battle"])
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
            "DDD"
            # "CUSTOM 5", 
            # "CUSTOM 10",
            # "CUSTOM 25",
            # "CUSTOM 100"
        ]