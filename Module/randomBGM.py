import random, os, zipfile

musicList = {
    "KH2": [
        {"name": "bgm\\music050.win32.scd", "kind": "field"}, # Destati
        {"name": "bgm\\music051.win32.scd", "kind": "battle"}, # Fragments of Sorrow
        {"name": "bgm\\music052.win32.scd", "kind": "field"}, # The Afternoon Streets
        {"name": "bgm\\music053.win32.scd", "kind": "battle"}, # Working Together
        {"name": "bgm\\music054.win32.scd", "kind": "field"}, #Sacred Moon
        {"name": "bgm\\music055.win32.scd", "kind": "battle"}, #Deep Drive
        {"name": "bgm\\music059.win32.scd", "kind": "battle"}, #A Fight to the Death
        {"name": "bgm\\music060.win32.scd", "kind": "battle"}, #Darkness of the Unknown I
        {"name": "bgm\\music061.win32.scd", "kind": "battle"}, #Darkness of the unknown II
        {"name": "bgm\\music062.win32.scd", "kind": "battle"}, # Darkness of the Unknown III
        {"name": "bgm\\music063.win32.scd", "kind": "battle"}, # The 13th Reflection
        {"name": "bgm\\music064.win32.scd", "kind": "field"}, #What a Surprise
        {"name": "bgm\\music065.win32.scd", "kind": "battle"}, # Happy Holidays
        {"name": "bgm\\music066.win32.scd", "kind": "battle"},  # The other Promise
        {"name": "bgm\\music067.win32.scd", "kind": "battle"}, # Rage Awakened
        {"name": "bgm\\music068.win32.scd", "kind": "field"}, # Cavern of Remembrance
        {"name": "bgm\\music069.win32.scd", "kind": "battle"}, # Deep Anxiety
        {"name": "bgm\\music081.win32.scd", "kind": "battle"}, # Beneath the Ground A
        {"name": "bgm\\music082.win32.scd", "kind": "field"}, # The Escapade
        {"name": "bgm\\music084.win32.scd", "kind": "battle"}, # Arabian Daydream
        {"name": "bgm\\music085.win32.scd", "kind": "battle"}, # Byte Striking
        {"name": "bgm\\music086.win32.scd", "kind": "battle"}, # Spooks of Halloween Town
        {"name": "bgm\\music087.win32.scd", "kind": "battle"}, # Disappeared
        {"name": "bgm\\music088.win32.scd", "kind": "cutscene"}, # Sora's Theme
        {"name": "bgm\\music089.win32.scd", "kind": "cutscene"}, # Friends in my heart
        {"name": "bgm\\music090.win32.scd", "kind": "cutscene"}, # Riku's Theme
        {"name": "bgm\\music091.win32.scd", "kind": "cutscene"}, #Kairi's Theme
        {"name": "bgm\\music092.win32.scd", "kind": "cutscene"},# A Walk in Andante
        {"name": "bgm\\music093.win32.scd", "kind": "cutscene"}, # Villain's of a Sort
        {"name": "bgm\\music094.win32.scd", "kind": "cutscene"}, # Organization XIII
        {"name": "bgm\\music095.win32.scd", "kind": "cutscene"}, # Apprehension
        {"name": "bgm\\music096.win32.scd", "kind": "cutscene"}, # Courage
        {"name": "bgm\\music097.win32.scd", "kind": "cutscene"}, # Laughter and Merriment
        {"name": "bgm\\music098.win32.scd", "kind": "cutscene"}, # Hesitation
        {"name": "bgm\\music099.win32.scd", "kind": "cutscene"}, # Missing You
        {"name": "bgm\\music100.win32.scd", "kind": "field"}, # The Underworld
        {"name": "bgm\\music101.win32.scd", "kind": "field"}, # Waltz of the Damned
        {"name": "bgm\\music102.win32.scd", "kind": "battle"}, # What Lies Beneath
        {"name": "bgm\\music103.win32.scd", "kind": "field"}, # Olympus Coliseum
        {"name": "bgm\\music104.win32.scd", "kind": "battle"}, # Dance of the Daring
        {"name": "bgm\\music106.win32.scd", "kind": "field", "dmca": True}, # Under the Sea
        {"name": "bgm\\music107.win32.scd", "kind": "battle"}, # Ursula's Revenge
        {"name": "bgm\\music108.win32.scd", "kind": "field", "dmca": True}, # Part of your World
        {"name": "bgm\\music109.win32.scd", "kind": "field"}, # A New Day is Dawning
        {"name": "bgm\\music110.win32.scd", "kind": "battle"}, # The Encounter
        {"name": "bgm\\music111.win32.scd", "kind": "battle"}, # Sinister Shadows
        {"name": "bgm\\music112.win32.scd", "kind": "battle"}, # Fields of Honor 
        {"name": "bgm\\music113.win32.scd", "kind": "field"}, # Swim This Way
        {"name": "bgm\\music114.win32.scd", "kind": "battle"}, # Tension Rising
        {"name": "bgm\\music115.win32.scd", "kind": "battle"}, # The Corrupted
        {"name": "bgm\\music116.win32.scd", "kind": "field"}, # The Home of Dragons
        {"name": "bgm\\music117.win32.scd", "kind": "battle"}, # Rowdy Rumble
        {"name": "bgm\\music118.win32.scd", "kind": "field"}, # Lazy Afternoons
        {"name": "bgm\\music119.win32.scd", "kind": "battle"}, # Sinister Sundown
        {"name": "bgm\\music120.win32.scd", "kind": "battle"}, #benieth the Ground B
        {"name": "bgm\\music121.win32.scd", "kind": "battle"}, # Desire for All That is Lost
        {"name": "bgm\\music122.win32.scd", "kind": "field"}, # Atlantica Tutorial I
        {"name": "bgm\\music123.win32.scd", "kind": "field"}, # Atlantica Tutorial II
        #{"name": "bgm\\music124.win32.scd", "kind": "field"}, # Atlantica Tutorial II.5 (no loop)
        #{"name": "bgm\\music125.win32.scd", "kind": "field"}, # Atlantica Tutorial Finish (short no loop)
        {"name": "bgm\\music127.win32.scd", "kind": "field"}, # A Day in Agrabah
        {"name": "bgm\\music128.win32.scd", "kind": "battle"}, # Arabian Dream
        {"name": "bgm\\music129.win32.scd", "kind": "field"}, # Isn't It Lovely
        #{"name": "bgm\\music130.win32.scd", "kind": "field"}, # Atlantica tutorials Combined (no loop)
        {"name": "bgm\\music131.win32.scd", "kind": "battle"}, # Dance to the Death 
        #{"name": "bgm\\music132.win32.scd", "kind": "cutscene", "dmca": True}, # Beauty and the Beast (short no loop)
        {"name": "bgm\\music133.win32.scd", "kind": "field"}, # Magical Mystery
        {"name": "bgm\\music134.win32.scd", "kind": "battle"}, #Working Together
        {"name": "bgm\\music135.win32.scd", "kind": "field"}, # Space Paranoids Theme
        {"name": "bgm\\music136.win32.scd", "kind": "battle"}, # Byte Bashing
        {"name": "bgm\\music137.win32.scd", "kind": "field"}, # A Twinkle in the Sky
        {"name": "bgm\\music138.win32.scd", "kind": "battle"}, # Shipmeisters' Shanty
        {"name": "bgm\\music139.win32.scd", "kind": "field"}, # Gearing up
        {"name": "bgm\\music141.win32.scd", "kind": "field"}, # Winnie the Pooh Theme
        {"name": "bgm\\music142.win32.scd", "kind": "field"}, # Crossing the Finish Line
        {"name": "bgm\\music143.win32.scd", "kind": "field"}, # Mickey Mouse Club March
        {"name": "bgm\\music144.win32.scd", "kind": "field"}, # This is Halloween
        {"name": "bgm\\music145.win32.scd", "kind": "battle"}, # Vim and Vigor
        {"name": "bgm\\music146.win32.scd", "kind": "cutscene"}, # Roxas' Theme
        {"name": "bgm\\music148.win32.scd", "kind": "field"}, # Blast Off
        {"name": "bgm\\music149.win32.scd", "kind": "battle"}, #Sppoks of Halloween (Variation)
        {"name": "bgm\\music151.win32.scd", "kind": "battle"}, # The 13th Struggle
        {"name": "bgm\\music152.win32.scd", "kind": "field"}, # Reviving Hallow Bastion
        {"name": "bgm\\music153.win32.scd", "kind": "battle"}, # Scherzo Di Notte
        {"name": "bgm\\music154.win32.scd", "kind": "field"}, # Nights of the Cursed
        {"name": "bgm\\music155.win32.scd", "kind": "battle"}, # He's a Pirate
        {"name": "bgm\\music158.win32.scd", "kind": "field"}, # Bounce-o-Rama
        {"name": "bgm\\music159.win32.scd", "kind": "battle"}, # Bounce-o-Rama Ver 2
        {"name": "bgm\\music164.win32.scd", "kind": "battle"}, # Road to a Hero
        {"name": "bgm\\music185.win32.scd", "kind": "battle"}, # The 13th Dilemma
        {"name": "bgm\\music186.win32.scd", "kind": "field"}, # Adventures in the Savannah
        {"name": "bgm\\music187.win32.scd", "kind": "battle"}, # Savannah Pride
        {"name": "bgm\\music188.win32.scd", "kind": "battle"}, # One-Winged Angel
        {"name": "bgm\\music189.win32.scd", "kind": "field"}, # Monochrome Dreams
        {"name": "bgm\\music190.win32.scd", "kind": "battle"}, # Old Friends, Old Rivals
        {"name": "bgm\\music506.win32.scd", "kind": "field", "dmca": True}, #Under The Sea
        {"name": "bgm\\music507.win32.scd", "kind": "battle"}, #Ursula Revenge
        {"name": "bgm\\music508.win32.scd", "kind": "field", "dmca": True}, #Part Of Your World
        {"name": "bgm\\music509.win32.scd", "kind": "field"}, #A New Day Is Dawning
        {"name": "bgm\\music513.win32.scd", "kind": "field"}, #Swim This Way
        {"name": "bgm\\music517.win32.scd", "kind": "battle"}, #Rowdy Rumble (Timeless River)
        {"name": "bgm\\music521.win32.scd", "kind": "battle"}, #Desire For All That Lost (Timeless River)
        {"name": "bgm\\music530.win32.scd", "kind": "battle"}, #He's A Pirate 
        {"name": "vagstream\\End_Piano.win32.scd", "kind": "title"}, #Dearly Beloved Reprise
        {"name": "vagstream\\GM1_Asteroid.win32.scd", "kind": "battle"}, #Asteroids Attack
        {"name": "vagstream\\GM2_Highway.win32.scd", "kind": "battle"}, #Hazardous Highway
        {"name": "vagstream\\GM3_Cloud.win32.scd", "kind": "battle"}, #Cloudchasers
        {"name": "vagstream\\GM4_Floating.win32.scd", "kind": "battle"}, #Floating in Bliss
        {"name": "vagstream\\GM5_Senkan.win32.scd", "kind": "battle"}, #Battleship Bravery
        {"name": "vagstream\\Title.win32.scd", "kind": "title"}], #Dearly Beloved
    "KH1": [
        #some music in kh1 is found in .dat folders and others in .bgm folders and somtimes both.
        #the ones in both .dat and .bgm folders are duplicates so you can ignore one of those.
        {"name": "music099.bgm\\music099.win32.scd", "kind": "battle"},#Dissapeared
        {"name": "music101.dat\\music101.win32.scd", "kind": "field"}, #Deep Jungle
        {"name": "music102.dat\\music102.win32.scd", "kind": "battle"}, #Having a Wild Time
        {"name": "music103.bgm\\music103.win32.scd", "kind": "field"}, #Olympus Coliseum
        {"name": "music104.dat\\music104.win32.scd", "kind": "field"}, #Traverse Town
        {"name": "music105.dat\\music105.win32.scd", "kind": "field"}, #Destiny Islands
        {"name": "music110.bgm\\music110.win32.scd", "kind": "title"}, #Dearly Beloved
        {"name": "music111.bgm\\music111.win32.scd", "kind": "battle"}, #Shrouding Dark Cloud
        {"name": "music112.dat\\music112.win32.scd", "kind": "battle"}, #Hand In Hand
        {"name": "music114.bgm\\music114.win32.scd", "kind": "cutscene"}, #Unknown 1 [Heartless Has Come, Pt.3]
        {"name": "music116.dat\\music116.win32.scd", "kind": "field"}, #Welcome To Wonderland
        {"name": "music117.dat\\music117.win32.scd", "kind": "field"}, #A Very Small Wish
        {"name": "music118.bgm\\music118.win32.scd", "kind": "battle"}, #To Our Surprise
        {"name": "music119.dat\\music119.win32.scd", "kind": "battle"}, #Busting Up On The Beach
        {"name": "music120.bgm\\music120.win32.scd", "kind": "battle"}, #Go For It
        {"name": "music121.dat\\music121.win32.scd", "kind": "battle"}, #Monstrous Monstro
        {"name": "music122.dat\\music122.win32.scd", "kind": "battle"}, #Blast Away Gummi Ship I
        {"name": "music123.dat\\music123.win32.scd", "kind": "battle"}, #Blast Away Gummi Ship II
        {"name": "music124.dat\\music124.win32.scd", "kind": "field"}, #Shipmeisters Humoresque
        {"name": "music125.dat\\music125.win32.scd", "kind": "field"}, #Precious Stars In The Sky
        {"name": "music127.dat\\music127.win32.scd", "kind": "field"}, #A Day In Agrabah
        {"name": "music128.dat\\music128.win32.scd", "kind": "battle"}, #Arabian Dream
        {"name": "music129.dat\\music129.win32.scd", "kind": "field"}, #Captain Hook Pirate Ship
        {"name": "music130.dat\\music130.win32.scd", "kind": "field"}, #Never Land Sky
        {"name": "music131.dat\\music131.win32.scd", "kind": "battle"}, #Night Of Fate
        {"name": "music140.dat\\music140.win32.scd", "kind": "field", "dmca": True}, #Under The Sea
        {"name": "music141.dat\\music141.win32.scd", "kind": "field"}, #Winnie The Pooh
        {"name": "music142.bgm\\music142.win32.scd", "kind": "cutscene"}, #Dive Into The Heart (Part 9)
        {"name": "music143.bgm\\music143.win32.scd", "kind": "cutscene"}, #Mickey Mouse Club March
        {"name": "music144.dat\\music144.win32.scd", "kind": "field"}, #This Is Halloween
        {"name": "music145.bgm\\music145.win32.scd", "kind": "battle"}, #Destiny Force
        {"name": "music146.dat\\music146.win32.scd", "kind": "battle"}, #Pirate Gigue
        {"name": "music147.dat\\music147.win32.scd", "kind": "battle"}, #An Adventure In Atlantica
        {"name": "music148.dat\\music148.win32.scd", "kind": "battle"}, #Blast Away Gummi Ship III
        {"name": "music149.dat\\music149.win32.scd", "kind": "battle"}, #Spooks Of Halloween Town
        {"name": "music150.bgm\\music150.win32.scd", "kind": "battle"}, #Squirming Evil
        {"name": "music151.bgm\\music151.win32.scd", "kind": "battle"}, #The Deep End
        {"name": "music152.dat\\music152.win32.scd", "kind": "field"}, #Hollow Bastion
        {"name": "music153.dat\\music153.win32.scd", "kind": "battle"}, #Scherzo Di Notte
        {"name": "music154.dat\\music154.win32.scd", "kind": "field"}, #End Of The World
        {"name": "music155.dat\\music155.win32.scd", "kind": "battle"}, #Fragments Of Sorrow
        {"name": "music156.bgm\\music156.win32.scd", "kind": "battle"}, #Guardando Nel Buio
        {"name": "music157.bgm\\music157.win32.scd", "kind": "battle"}, #Holy Bananas
        {"name": "music158.bgm\\music158.win32.scd", "kind": "field"}, #Bounce-O-Rama
        {"name": "music160.bgm\\music160.win32.scd", "kind": "cutscene"}, #Kairi I
        {"name": "music161.bgm\\music161.win32.scd", "kind": "cutscene"}, #Kairi II
        {"name": "music163.bgm\\music163.win32.scd", "kind": "cutscene"}, #Villains Of A Sort 
        {"name": "music164.bgm\\music164.win32.scd", "kind": "battle"}, #Road To Hero
        {"name": "music165.bgm\\music165.win32.scd", "kind": "field"}, #This Is Halloween (Alternative)
        {"name": "music170.bgm\\music170.win32.scd", "kind": "cutscene"}, #A Piece Of Peace
        {"name": "music172.bgm\\music172.win32.scd", "kind": "cutscene"}, #A Walk In Adante
        {"name": "music173.bgm\\music173.win32.scd", "kind": "battle"}, #No Time To Think
        {"name": "music174.bgm\\music174.win32.scd", "kind": "battle"}, #An Intense Situation
        {"name": "music176.bgm\\music176.win32.scd", "kind": "cutscene"}, #Friends In My Heart
        {"name": "music178.bgm\\music178.win32.scd", "kind": "cutscene"}, #Treasured Memories
        {"name": "music180.bgm\\music180.win32.scd", "kind": "cutscene"}, #Kairi III
        {"name": "music184.bgm\\music184.win32.scd", "kind": "field"}, #Merlin Magical House
        {"name": "music185.bgm\\music185.win32.scd", "kind": "battle"}, #Forze Del Male
        {"name": "music187.bgm\\music187.win32.scd", "kind": "cutscene"}, #Just An Itty Bitty Too Much
        {"name": "music188.bgm\\music188.win32.scd", "kind": "cutscene"}, #It Began With A Letter
        {"name": "music193.bgm\\music193.win32.scd", "kind": "title"}, #Dearly Beloved Reprise       
        {"name": "music196.bgm\\music196.win32.scd", "kind": "battle"}, #One Winged Angel
        {"name": "music197.bgm\\music197.win32.scd", "kind": "battle", "dmca": True} #Night On Blad Mountain
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
        #{"name": "music162.bgm\\music162.win32.scd", "kind": "unknown"}, #Villains Of A Sort (Short)
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
        {"name": '12_Event_Yuttari.win32.scd', "kind": "cutscene"},
        {"name": '13_Event_Namine.win32.scd', "kind": "cutscene"},
        {"name": '14_Event_Odayaka.win32.scd', "kind": "cutscene"},
        {"name": '15_Event_XIII.win32.scd', "kind": "cutscene"},
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
        {"name": '38_UnderTheSea.win32.scd', "kind": "field", "dmca": True},
        {"name": '39_LittleMermaid_B.win32.scd', "kind": "battle"},
        {"name": '40_LastBoss2.win32.scd', "kind": "battle"},
        {"name": '41_LastBoss3.win32.scd', "kind": "battle"},
        {"name": '42_Hollow_F.win32.scd', "kind": "field"},
        {"name": '43_Hollow_B.win32.scd', "kind": "battle"},
        {"name": '44_PooGame1.win32.scd', "kind": "field"},
        {"name": '45_PoohGame2.win32.scd', "kind": "battle"},
        {"name": 'Boss1.win32.scd', "kind": "battle"},
        {"name": 'Boss2_World.win32.scd', "kind": "battle"},
        {"name": 'Event1_Kinpak.win32.scd', "kind": "cutscene"},
        {"name": 'Event2_.win32.scd', "kind": "battle"},
        {"name": 'Event4.win32.scd', "kind": "cutscene"},
        {"name": 'Event_Unrest.win32.scd', "kind": "cutscene"},
        {"name": 'Title.win32.scd', "kind": "title"}],
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
        {"name": "030youki.win32.scd", "kind": "cutscene"},
        {"name": "031isamashi.win32.scd", "kind": "cutscene"},
        {"name": "032odayaka.win32.scd", "kind": "cutscene"},
        {"name": "033fuon.win32.scd", "kind": "cutscene"},
        {"name": "034kanasii.win32.scd", "kind": "cutscene"},
        {"name": "035kinpaku.win32.scd", "kind": "cutscene"},
        {"name": "036seisin.win32.scd", "kind": "field"},
        {"name": "037yami.win32.scd", "kind": "cutscene"},
        {"name": "038ria_deai.win32.scd", "kind": "cutscene"},
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
        {"name": "050title.win32.scd", "kind": "title"},
        {"name": "051worldmap.win32.scd", "kind": "field"},
        {"name": "060tera.win32.scd", "kind": "cutscene"},
        {"name": "061aqua.win32.scd", "kind": "cutscene"},
        {"name": "062ven.win32.scd", "kind": "cutscene"},
        {"name": "063kairi1.win32.scd", "kind": "cutscene"},
        {"name": "066peet.win32.scd", "kind": "cutscene"},
        {"name": "067disvill.win32.scd", "kind": "cutscene"},
        {"name": "068zea.win32.scd", "kind": "cutscene"},
        {"name": "069braig.win32.scd", "kind": "cutscene"},
        {"name": "070key_l.win32.scd", "kind": "cutscene"},
        {"name": "071key_d.win32.scd", "kind": "cutscene"},
        {"name": "072key_l_d.win32.scd", "kind": "cutscene"},
        {"name": "073kizuna.win32.scd", "kind": "cutscene"},
        {"name": "074zack.win32.scd", "kind": "cutscene"},
        {"name": "100ice1_128.win32.scd", "kind": "field"},
        {"name": "101ice1_132.win32.scd", "kind": "field"},
        {"name": "102ice_2.win32.scd", "kind": "field"},
        {"name": "103fruit.win32.scd", "kind": "field"},
        {"name": "104dice.win32.scd", "kind": "field"},
        {"name": "105poomini.win32.scd", "kind": "field"},
        {"name": "106cartrace.win32.scd", "kind": "battle"},
        {"name": "107syugyo.win32.scd", "kind": "field"},
        {"name": "108riro.win32.scd", "kind": "field"},
        {"name": "109training.win32.scd", "kind": "battle"},
        {"name": "110han_bt1.win32.scd", "kind": "battle"},
        {"name": "111han_bt2.win32.scd", "kind": "battle"},
        {"name": "112rage_bt.win32.scd", "kind": "battle"},
        {"name": "113kh1tit.win32.scd", "kind": "title"},
        {"name": "114raceview.win32.scd", "kind": "field"},
        {"name": "115boss.win32.scd", "kind": "battle"},
        #{"name": "116icon.win32.scd", "kind": "field"}, #intro to dearly beloved (psp xmb ver.) (short and doesn't loop)
        {"name": "117short_l2.win32.scd", "kind": "field"},
        {"name": "118gumi.win32.scd", "kind": "field"},
        {"name": "119desti.win32.scd", "kind": "field"},
        {"name": "120hand.win32.scd", "kind": "battle"},
        {"name": "122nazono.win32.scd", "kind": "battle"}, #mysterious figure boss theme
        #{"name": "123rev.win32.scd", "kind": "field"}, #mysterious figure boss theme reversed (loops but is only 3s)
        {"name": "124dp_amb.win32.scd", "kind": "field"}, #destroyed land of departure
        {"name": "125yami_f.win32.scd", "kind": "field"},
        {"name": "126yami_b.win32.scd", "kind": "battle"},
        {"name": "127Xeha_b.win32.scd", "kind": "battle"},
        {"name": "128Eraqu_b.win32.scd", "kind": "battle"},
        {"name": "129Pure_b.win32.scd", "kind": "battle"},
        {"name": "130Mons_b.win32.scd", "kind": "battle"} #Monstro
        ],
    "DDD": [
        {"name": "bgm_001.win32.scd", "kind": "field"}, # Traverse in Trance (Traverse Town Field Music)
		{"name": "bgm_002.win32.scd", "kind": "field"}, # One for All (Country of the Musketeers Field Music)
		{"name": "bgm_003.win32.scd", "kind": "field"}, # The Fun Fair (Prankster's Paradise Field Music)
		{"name": "bgm_004.win32.scd", "kind": "field"}, # A Very Small Wish (Monstro Field Music)
		{"name": "bgm_005.win32.scd", "kind": "field", "dmca": True}, # Symphony No. 6 Pastoral Op. 68 (Sora's Symphony of Sorcery Music)
		{"name": "bgm_006.win32.scd", "kind": "field", "dmca": True}, # The Nutcracker Suite Op. 71 (Riku's Symphony of Sorcery Music)
		{"name": "bgm_007.win32.scd", "kind": "field", "dmca": True}, # L'Apprenti Sorcier (Symphony of Sorcery Music)
		{"name": "bgm_008.win32.scd", "kind": "battle", "dmca": True}, # Night on Bald Mountain
		{"name": "bgm_009.win32.scd", "kind": "field"}, # La Cloche (La Cité des Cloches Field Music)
		{"name": "bgm_010.win32.scd", "kind": "field"}, # Magical Mystery (Mysterious Tower Field Music)
		{"name": "bgm_011.win32.scd", "kind": "field"}, # Access the Grid (The Grid Field Music)
		{"name": "bgm_012.win32.scd", "kind": "field"}, # Sacred Distance (KH3D The World That Never Was Field Music)
		{"name": "bgm_013.win32.scd", "kind": "field"}, # Sacred Moon (KH2 The World That Never Was Field Music)
		{"name": "bgm_014.win32.scd", "kind": "battle"}, # Hand to Hand (Traverse Town Battle Music)
		{"name": "bgm_015.win32.scd", "kind": "battle"}, # All for One (Country of the Musketeers Battle Music)
		{"name": "bgm_016.win32.scd", "kind": "battle"}, # Prankster's Party (Prankster's Paradise Battle Music)
		{"name": "bgm_017.win32.scd", "kind": "battle"}, # Monstrous Monstro (Monstro Battle Music)
		{"name": "bgm_018.win32.scd", "kind": "battle"}, # Le Sanctuaire (La Cité des Cloches Field Music)
		{"name": "bgm_019.win32.scd", "kind": "battle"}, # Working Together (Mysterious Tower Field Music)
		{"name": "bgm_020.win32.scd", "kind": "battle"}, # Digital Domination (The Grid Battle Music)
		{"name": "bgm_021.win32.scd", "kind": "battle"}, # Deep Drop (KH3D The World That Never Was Battle Music)
		{"name": "bgm_022.win32.scd", "kind": "battle"}, # Deep Drive (KH2 The World That Never Was Battle Music)
		{"name": "bgm_023.win32.scd", "kind": "battle"}, # Majestic Wings
		{"name": "bgm_024.win32.scd", "kind": "battle"}, # UNTAMABLE
		{"name": "bgm_025.win32.scd", "kind": "battle"}, # Ice-hot Lobster
		{"name": "bgm_026.win32.scd", "kind": "battle"}, # Gigabyte Mantis
		{"name": "bgm_027.win32.scd", "kind": "battle"}, # Rowdy Rumble
		{"name": "bgm_028.win32.scd", "kind": "battle"}, # The Encounter -Birth by Sleep Version-
		{"name": "bgm_029.win32.scd", "kind": "battle"}, # L'Oscurità dell' Ignoto
		{"name": "bgm_030.win32.scd", "kind": "battle"}, # L'Eminenza Oscura I 
		{"name": "bgm_031.win32.scd", "kind": "battle"}, # L'Eminenza Oscura II
		{"name": "bgm_032.win32.scd", "kind": "battle"}, # L'Impeto Oscuro
		{"name": "bgm_033.win32.scd", "kind": "battle"}, # Destiny's Force
		{"name": "bgm_034.win32.scd", "kind": "battle"}, # Shrouding Dark Cloud
		{"name": "bgm_035.win32.scd", "kind": "field"}, # Dream Matchup
		{"name": "bgm_036.win32.scd", "kind": "field"}, # The Flick Finalist
		{"name": "bgm_037.win32.scd", "kind": "field"}, # The World of Dream Drops (World Map Music)
		{"name": "bgm_038.win32.scd", "kind": "title"}, # Dearly Beloved (Dream Drop Distance Version)
		{"name": "bgm_039.win32.scd", "kind": "cutscene"}, # Innocent Times
		{"name": "bgm_040.win32.scd", "kind": "cutscene"}, # Cheers for the Brave
		{"name": "bgm_041.win32.scd", "kind": "cutscene"}, # Peaceful Hearts
		{"name": "bgm_042.win32.scd", "kind": "cutscene"}, # Drops of Poison
		{"name": "bgm_043.win32.scd", "kind": "cutscene"}, # Tears of the Light
		{"name": "bgm_044.win32.scd", "kind": "cutscene"}, # Shaded Truths
		{"name": "bgm_045.win32.scd", "kind": "cutscene"}, # Broken Reality
		{"name": "bgm_046.win32.scd", "kind": "cutscene"}, # Ever After
		{"name": "bgm_047.win32.scd", "kind": "cutscene"}, # Sora
		{"name": "bgm_048.win32.scd", "kind": "cutscene"}, # Riku
		{"name": "bgm_050.win32.scd", "kind": "battle"}, # Road to a Hero
		{"name": "bgm_051.win32.scd", "kind": "cutscene"}, # Villains of a Sort
		{"name": "bgm_052.win32.scd", "kind": "cutscene"}, # Strange Whispers
		{"name": "bgm_053.win32.scd", "kind": "battle"}, # Night of Fate
		{"name": "bgm_059.win32.scd", "kind": "cutscene"}, # The Key of Light
		{"name": "bgm_060.win32.scd", "kind": "cutscene"}, # The Key of Darkness
		{"name": "bgm_061.win32.scd", "kind": "cutscene"}, # Xehanort
		{"name": "bgm_062.win32.scd", "kind": "cutscene"}, # Xehanort -The Early Years-
		{"name": "bgm_063.win32.scd", "kind": "cutscene"}, # Xigbar
		{"name": "bgm_065.win32.scd", "kind": "cutscene"}, # Organization XIII
		{"name": "bgm_066.win32.scd", "kind": "cutscene"}, # Destiny's Union
		{"name": "bgm_067.win32.scd", "kind": "field"}, # Dream Eaters
		{"name": "bgm_068.win32.scd", "kind": "battle"}, # TWISTER -KINGDOM MIX-
		{"name": "bgm_069.win32.scd", "kind": "battle"}, # CALLING -KINGDOM MIX- (No Intro)
		{"name": "bgm_070.win32.scd", "kind": "title"}, # Dearly Beloved (End of Symphony of Sorcery Cutscene 1)
		{"name": "bgm_071.win32.scd", "kind": "title"}, # Dearly Beloved (End of Symphony of Sorcery Cutscene 2)
		{"name": "bgm_072.win32.scd", "kind": "field", "dmca": True}, # Symphony of Sorcery Music
		{"name": "bgm_073.win32.scd", "kind": "field", "dmca": True}, # Symphony of Sorcery Music (Spellican Battle Music)
		{"name": "bgm_074.win32.scd", "kind": "field", "dmca": True}, # Symphony of Sorcery Music
		{"name": "bgm_075.win32.scd", "kind": "field"}, # The Dream
		{"name": "bgm_076.win32.scd", "kind": "cutscene"}, # The Nightmare
		{"name": "bgm_077.win32.scd", "kind": "cutscene"}, # Link to All
		{"name": "bgm_078.win32.scd", "kind": "cutscene"}, # Distant from You...
		{"name": "bgm_083.win32.scd", "kind": "field"}, # Sweet Spirits
		{"name": "bgm_084.win32.scd", "kind": "field"}, # Ready to Rush
		{"name": "bgm_085.win32.scd", "kind": "field"}, # Victor's Pride
		{"name": "bgm_086.win32.scd", "kind": "battle"}, # Keyblade Cycle
		{"name": "bgm_087.win32.scd", "kind": "battle"}, # Storm Diver
		{"name": "bgm_088.win32.scd", "kind": "battle"}, # Wild Blue
		{"name": "bgm_089.win32.scd", "kind": "field"}, # My Heart's Descent
		#{"name": "bgm_091.win32.scd", "kind": "battle"}, # Dream Drop Distance -The Next Awakening- (no loop)
		{"name": "bgm_093.win32.scd", "kind": "battle"}, # The Eye of Darkness
		{"name": "bgm_094.win32.scd", "kind": "battle"}, # The Dread of Night
		{"name": "bgm_095.win32.scd", "kind": "unknown"}, # SOMEDAY -KINGDOM MIX-
		#{"name": "bgm_096.win32.scd", "kind": "unknown"}, # Hand in Hand (KH2 Ending Version)
		#{"name": "bgm_097.win32.scd", "kind": "unknown"}, # Oopsy-Daisy
		{"name": "bgm_098.win32.scd", "kind": "battle"}, # TWISTER -KINGDOM MIX-
		{"name": "bgm_099.win32.scd", "kind": "battle"}, # CALLING -KINGDOM MIX- (With Intro)
		#{"name": "bgm_112.win32.scd", "kind": "title"}, # Dearly Beloved (Kingdom Hearts II Version)
		#{"name": "bgm_113.win32.scd", "kind": "title"}, # Dearly Beloved -Reprise-
		{"name": "bgm_114.win32.scd", "kind": "cutscene"}, # Roxas
		{"name": "bgm_115.win32.scd", "kind": "cutscene"}, # Ventus
		{"name": "bgm_116.win32.scd", "kind": "battle"}], # Rinzler Recompiled
    "MOVIES": [
        #Recoded
		#{"name": "bgm_000.win32.scd", "kind": "field"}, # Destiny's Union (From Birth by Sleep)
		#{"name": "bgm_001.win32.scd", "kind": "field"}, # A Day in Agrabah
		#{"name": "bgm_002.win32.scd", "kind": "field"}, # A Walk in Andante
		#{"name": "bgm_003.win32.scd", "kind": "battle"}, # Apprehension (From Original KH2)
		#{"name": "bgm_004.win32.scd", "kind": "battle"}, # Arabian Dream (From Original KH2)
		#{"name": "bgm_005.win32.scd", "kind": "battle"}, # Courage (From Original KH2)
 		{"name": "bgm_006.win32.scd", "kind": "title"}, # Dearly Beloved (Re:coded Version)
 		{"name": "bgm_007.win32.scd", "kind": "field"}, # Destiny Islands (From Original KH1)
 		{"name": "bgm_008.win32.scd", "kind": "field"}, # Destati (Orchestrated Version) (Length: 5:49)
		#{"name": "bgm_009.win32.scd", "kind": "battle"}, # Destiny's Force (From Original KH1)
		#{"name": "bgm_010.win32.scd", "kind": "field"}, # Dive into the Heart -Destati- (From KH1) (Length: 9:56)
		#{"name": "bgm_011.win32.scd", "kind": "field"}, # Friends in My Heart (From Original KH1)
 		{"name": "bgm_012.win32.scd", "kind": "battle"}, # Guardando nel buio (From Original KH1)
		#{"name": "bgm_013.win32.scd", "kind": "field"}, # Hollow Bastion
		#{"name": "bgm_014.win32.scd", "kind": "field"}, # It Began with a Letter
		#{"name": "bgm_015.win32.scd", "kind": "field"}, # Link to All
 		{"name": "bgm_016.win32.scd", "kind": "battle"}, # Night of Fate (From Original KH1)
		#{"name": "bgm_017.win32.scd", "kind": "field"}, # Namine
		#{"name": "bgm_018.win32.scd", "kind": "battle"}, # No Time to Think (From Original KH1)
		#{"name": "bgm_019.win32.scd", "kind": "field"}, # Olympus Coliseum (From Original KH1)
		#{"name": "bgm_020.win32.scd", "kind": "field"}, # Organization XIII (From Original KH2)
		#{"name": "bgm_021.win32.scd", "kind": "field"}, # Riku (From Original KH2)
		#{"name": "bgm_022.win32.scd", "kind": "battle"}, # Rowdy Rumble (From Original KH2)
		#{"name": "bgm_023.win32.scd", "kind": "field"}, # Roxas (From Original KH2)
		#{"name": "bgm_024.win32.scd", "kind": "battle"}, # Scherzo Di Notte (From Original KH1)
		#{"name": "bgm_025.win32.scd", "kind": "battle"}, # Shrouding Dark Cloud (From Original KH1)
 		{"name": "bgm_026.win32.scd", "kind": "battle"}, # Squirming Evil (From Original KH1)
		#{"name": "bgm_027.win32.scd", "kind": "field"}, # Strange Whispers (From Original KH1)
		#{"name": "bgm_028.win32.scd", "kind": "battle"}, # To Our Surprise (From Original KH1)
 		{"name": "bgm_029.win32.scd", "kind": "field"}, # Traverse Town (From Original KH1)
		#{"name": "bgm_030.win32.scd", "kind": "field"}, # Villains of a Sort
		#{"name": "bgm_031.win32.scd", "kind": "battle"}, # Vim & Vigor
		#{"name": "bgm_032.win32.scd", "kind": "field"}, # Welcome to Wonderland (From Original KH1)
		#{"name": "bgm_033.win32.scd", "kind": "field"}, # Castle Oblivion
		#{"name": "bgm_034.win32.scd", "kind": "field"}, # Dive into the Heart -Destati- (From KH2)
		#{"name": "bgm_035.win32.scd", "kind": "field"}, # Dearly Beloved -Reprise-
 		{"name": "bgm_036.win32.scd", "kind": "battle"}, # Forze Del Male (From Original KH1)
        #Days
 		{"name": "bgm_201.win32.scd", "kind": "title"}, # Dearly Beloved (358/2 Days Version)
		#{"name": "bgm_202.win32.scd", "kind": "battle"}, # Sinister Sundown
		#{"name": "bgm_203.win32.scd", "kind": "field"}, # Lazy Afternoons
		#{"name": "bgm_204.win32.scd", "kind": "battle"}, # Destiny's Force
		#{"name": "bgm_205.win32.scd", "kind": "field"}, # Welcome to Wonderland
		#{"name": "bgm_206.win32.scd", "kind": "battle"}, # To Our Surprise
		#{"name": "bgm_207.win32.scd", "kind": "field"}, # Olympus Coliseum
		#{"name": "bgm_208.win32.scd", "kind": "battle"}, # Go for It!
		#{"name": "bgm_209.win32.scd", "kind": "field"}, # This is Halloween
		#{"name": "bgm_210.win32.scd", "kind": "battle"}, # Spooks of Halloween Town
		#{"name": "bgm_211.win32.scd", "kind": "field"}, # A Day in Agrabah
		#{"name": "bgm_212.win32.scd", "kind": "battle"}, # Arabian Dream
 		{"name": "bgm_213.win32.scd", "kind": "field"}, # Mystic Moon
 		{"name": "bgm_214.win32.scd", "kind": "battle"}, # Critical Drive
 		{"name": "bgm_215.win32.scd", "kind": "field"}, # Sacred Moon (358/2 Days Version)
		#{"name": "bgm_216.win32.scd", "kind": "field"}, # Waltz of the Damned
		#{"name": "bgm_217.win32.scd", "kind": "battle"}, # Dance of the Daring
		#{"name": "bgm_218.win32.scd", "kind": "field"}, # Organization XIII (From Original KH2)
		#{"name": "bgm_219.win32.scd", "kind": "field"}, # Roxas
 		{"name": "bgm_220.win32.scd", "kind": "battle"}, # Tension Rising (From Original KH2)
		#{"name": "bgm_221.win32.scd", "kind": "battle"}, # Rowdy Rumble
 		{"name": "bgm_222.win32.scd", "kind": "field"}, # Musique pour la tristesse de Xion (Xion's Theme)
		#{"name": "bgm_223.win32.scd", "kind": "battle"}, # Shrouding Dark Cloud
		#{"name": "bgm_224.win32.scd", "kind": "battle"}, # Vim & Vigor (From Original KH2)
		#{"name": "bgm_225.win32.scd", "kind": "field"}, # Riku (From Original KH2)
		#{"name": "bgm_226.win32.scd", "kind": "field"}, # Strange Whispers
		#{"name": "bgm_227.win32.scd", "kind": "battle"}, # Apprehension
		#{"name": "bgm_228.win32.scd", "kind": "field"}, # Friends in My Heart
		#{"name": "bgm_229.win32.scd", "kind": "field"}, # Missing You (From Original KH2)
 		{"name": "bgm_230.win32.scd", "kind": "field"}, # Xemnas
 		{"name": "bgm_231.win32.scd", "kind": "field"}, # Secret of Neverland
 		{"name": "bgm_232.win32.scd", "kind": "battle"}, # Crossing to Neverland
 		{"name": "bgm_233.win32.scd", "kind": "field"}, # At Dusk, I Will Think of You...
 		{"name": "bgm_234.win32.scd", "kind": "battle"}, # Fight and Away
 		{"name": "bgm_235.win32.scd", "kind": "battle"}, # Another Side -Battle Ver.-
 		{"name": "bgm_236.win32.scd", "kind": "battle"}, # Vector to the Heavens
		#{"name": "bgm_237.win32.scd", "kind": "field"}, # Dearly Beloved -Reprise-
		#{"name": "bgm_238.win32.scd", "kind": "field"}, # Treasured Memories
		#{"name": "bgm_239.win32.scd", "kind": "battle"}, # Face It! (From Re:Chain of Memories)
		#{"name": "bgm_240.win32.scd", "kind": "field"}, # Kairi III
		#{"name": "bgm_241.win32.scd", "kind": "field"}, # Treasured Memories (Same Version as bgm_238.win32.scd)
		#{"name": "bgm_242.win32.scd", "kind": "field"}, # Disquieting (From Re:Chain of Memories)
		#{"name": "bgm_243.win32.scd", "kind": "battle"}, # The Other Promise (From Original KH2)
 		{"name": "bgm_244.win32.scd", "kind": "field"}, # Another Side (No Intro)
 		{"name": "bgm_245.win32.scd", "kind": "battle"}, # Another Side -Battle Ver.- (No Intro)
 		{"name": "bgm_255.win32.scd", "kind": "title"}], # Dearly Beloved (Kingdom Hearts HD 1.5 + 2.5 ReMiX Launcher Version)
    "CUSTOM": [],
}

musicPaths = {
    "KH2": "",
    "KH1": "..\\kh1\\remastered\\amusic\\",
    "BBS": "..\\bbs\\sound\\win\\bgm\\",
    "RECOM": "..\\recom\\STREAM\\0001\\",
    "DDD": "..\\ddd\\sound\\jp\\output\\BGM\\",
    "MOVIES": "..\\mare\\sound\\",
    "CUSTOM": "..\\custom\\"
}
class RandomBGM():
    @staticmethod
    def randomizeBGM(selections, platform):
    
        #for testing. you would want a option to set these to whatever number you want on the site.
        #if we don't care about categories then we could just set one number and set all tracks to "unknown" or something.
        #customlistf = 13
        #customlistb = 7
        #Uses the numbrers above to build the dict with appropriate categories.
        #for i in range(customlistf):
        #    musicList["CUSTOM"].append({"name": "custom_f_{}.scd".format(f'{i+1:03d}'), "kind": "field"})
        #for i in range(customlistb):
        #    musicList["CUSTOM"].append({"name": "custom_b_{}.scd".format(f'{i+1:03d}'), "kind": "battle"})
        #print (musicList["CUSTOM"]),
        
        options = {
            #we don't need to separate CUSTOM from everything else anymore i think.
            "games": [s for s in selections if s in musicList],
            "options": [s for s in selections if not (s in musicList)]
        }
        
        if not platform == "PC" or len(options["games"]) < 1:
            return ""
        
        BGMList = {"battle": [], "field": [], "title":[], "cutscene": []}
        for game in options["games"]:
            for song in musicList[game]:
                if "DMCA-SAFE" in options["options"] and song.get("dmca", False):
                    continue
                kind = "battle" #default
                category = song.get("kind") #current song
                #sort bgm as field first if splitFB is true.
                if "Randomize Field and Battle Music Separately" in options["options"] and category != "battle":
                    kind = "field"
                #give "unknown" and "cutscene" bgm a random kind.
                if "Randomize Field and Battle Music Separately" in options["options"] and (category == "unknown" or category == "cutscene"):
                    kind = random.choice(["field", "battle"])
                #separate dearly beloved bgms
                if "Randomize Dearly Beloved Separately" in options["options"] and category == "title":
                    kind = "title"
                #separate cutscene bgms
                if "Randomize Cutscene Music Separately" in options["options"] and category == "cutscene":
                    kind = "cutscene"
                song["game"] = game
                BGMList[kind].append(song)
        #print (BGMList["title"]),

        def _getMusicAsset(original_song, new_song):
            return {
                "name": "{original}".format(original=original_song["name"]),
                "method": "copy",
                "source": [{"name": "{newPath}{newBGM}".format(newPath = musicPaths[new_song["game"]], newBGM = new_song["name"]), "type":"internal"}]
            }
            
        #get lists and shuffle them
        shuffledBattle = BGMList["battle"][:]
        shuffledField = BGMList["field"][:]
        shuffledTitle = BGMList["title"][:]
        shuffledScene = BGMList["cutscene"][:]
        random.shuffle(shuffledBattle)
        random.shuffle(shuffledField)
        random.shuffle(shuffledTitle)
        random.shuffle(shuffledScene)
        numBattle = 0
        numField = 0
        numTitle = 0
        numScene = 0
        BGMAssets = []
        for i in range(len(musicList["KH2"])):
            original_song = musicList["KH2"][i]
            kind = original_song.get("kind")
            if "Randomize Cutscene Music Separately" in options["options"] and kind == "cutscene":
                new_song = shuffledScene[numScene % len(shuffledScene)]
                numScene += 1
            elif "Randomize Dearly Beloved Separately" in options["options"] and kind == "title":
                new_song = shuffledTitle[numTitle % len(shuffledTitle)]
                numTitle += 1
            elif "Randomize Field and Battle Music Separately" in options["options"] and (kind == "field" or kind == "title" or kind == "cutscene"):
                new_song = shuffledField[numField % len(shuffledField)]
                numField += 1
            else:
                new_song = shuffledBattle[numBattle % len(shuffledBattle)]
                numBattle += 1
            BGMAssets.append(_getMusicAsset(original_song, new_song))
            ##debug final sorting
            #testFB = True if "Randomize Field and Battle Music Separately" in options["options"] else False
            #testDB = True if "Randomize Dearly Beloved Separately" in options["options"] else False
            #testCS = True if "Randomize Cutscene Music Separately" in options["options"] else False
            ##check field
            #if testFB and original_song["kind"] == "field" or testDB and original_song["kind"] == "field" and (testDB == False or testCS == False):
            #    if new_song["kind"] != "field":
            #        if testDB and new_song["kind"] == "title" or testCS and new_song["kind"] == "cutscene":
            #            print ("Bad Field Match! Orig = " + original_song["kind"] + " | New = " + new_song["kind"])
            ##check battle
            #if testFB and original_song["kind"] == "battle":
            #    if new_song["kind"] != "battle":
            #        if testCS and new_song["kind"] == "cutscene":
            #            print ("Bad Battle Match! Orig = " + original_song["kind"] + " | New = " + new_song["kind"])
            ##check title
            #if testDB and original_song["kind"] == "title":
            #    if new_song["kind"] != "title":
            #        print ("Bad Title Match! Orig = " + original_song["kind"] + " | New = " + new_song["kind"])
            ##check cutscene
            #if testCS and original_song["kind"] == "cutscene":
            #    if new_song["kind"] != "cutscene":
            #        print ("Bad Cutscene Match! Orig = " + original_song["kind"] + " | New = " + new_song["kind"])
            #if new_song["kind"] == "unknown":
            #    print ("Orig = " + original_song["kind"] + " | New = " + new_song["kind"])
        return BGMAssets

    def getOptions():
        return [
            "DMCA-SAFE",
            "Randomize Field and Battle Music Separately",
            "Randomize Dearly Beloved Separately",
            "Randomize Cutscene Music Separately"
        ]

    def getGames():
        return [
            "KH2",
            "KH1",
            "BBS",
            "RECOM",
            "DDD",
            "MOVIES"
            #framework already done for this option. just needs options on the site to set the number of tracks to use
            #"CUSTOM"
        ]
