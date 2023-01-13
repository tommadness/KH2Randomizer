The randomizer community has the primary tracker as well as some novelty ones for other game modes.

* [KhTracker](#KHTracker)
    * [Instructions](#Instructions)
* [Battleship Tracker](#Battleship-Tracker)
    * [Battleship Instructions](#Instructions)
    * [Bingo Instructions](#Instructions)
    * [Boss Enemy Instructions](#Instructions)
    * [Maze Mode Instructions](#Instructions)
    * [Hitlist Instructions](#Instructions)

# KHTracker

When playing the randomizer, it can be helpful to see everything you collect, what worlds you found the checks in, and your in-game stats. Everything that the tracker can display is annotated in the image below and will be referenced throughout the remainder of this page. 

<img src="static/annotated_tracker.png" width="600">
Note: The exact layout and check inclusions are subject to change from version to version.

### World Labels

The tracker displays all of the worlds that you may encounter while playing the randomizer. The image below showcases all of the locations where checks may potentially be found and their commonplace shorthand. The shorthand is included because many times streamers may say "I'm going to OC" instead of "I'm going to Olympus Coliseum."

<img src="static/world_labels.png" width="480">

Now that all of the locations are known, it is important to know you will not always encounter a location when playing a seed. For example, Atlantica and Puzzles & Synthesis are rarely included in any seed. In the randomizer generator, one can remove any worlds from the check pool, meaning that those worlds would not contain any important checks. The tracker will have access to this information when you load a seed in and remove those worlds from the tracker layout. So, for example, the image below showcases what the tracker looks like when I only want Disney worlds in the pool.

<img src="static/filtered_tracker.png" width="480">

### Check Labels

The section of the tracker beneath the worlds where all the checks are located are called _important checks_. These are checks that will track on the tracker to the appropriate world once you collect it in game.

Note that while all the possible important checks are included in the image above, not all of them show up in various settings. For example, anti-form, munny pouches, Olympus Stone, Hades Cup, Unknown Disk, and Promise Charm are frequently omitted from seed settings. Additionally, the visit unlocks are not always turned on for certain settings. When turned on, you must find the world specific party member weapon to progress onwards to the second visit of each world. For example, to progress further than the Hydra fight in Olympus Coliseum, you must find Auron's weapon - Battlefields of War - to continue onwards. When these visit unlocking items are off, you are free to go wherever you please and those checks will disappear from the tracker. 

### Changing Image Styles

The tracker comes decked out with many styling features. These features do not change how the tracker functions at all, but does change the layout and visuals. Under "Image Visuals" you can change the world, progression, and check icon visuals to your liking.

### Instructions

The tracker can be downloaded from [here](https://github.com/Dee-Ayy/KH2Tracker/releases) if you do not have it already. Scroll to the version you want to download and download the ".exe" file only. In the event your computer tries to protect you from the file, select "More Info" and then "Run anyway."

To use the KH2 Tracker, open the tracker by clicking on the KhTracker ".exe" file. Once the tracker loads, go to "Options > Load Hints" and select the appropriate hints extension (most likely Kh2 Randomizer seed). Select the appropriate file once the file explorer window opens (most likely the randoseed zip you just generated). Once the seed is loaded in, launch KH2. It's good practice to confirm that the seed hash displayed in the start game menu matches the seed hash displayed on the tracker once the seed is loaded in. After this, go to "Options" > "Start [Method] Tracking" where [Method] is the version (PCSX2/PC Port) of KH2 you are playing on. Make sure the tracker confirms that the autotracking has started. You will be able to tell because either the PCSX2 or PC icon (in green) will show up. Now you're good to start a seed!

#### Saving and Loading Seeds

In the event you want to save your randomizer progress to continue it at a later time, go to "Options" > "Save Current Progress" and save the resulting ".txt" file in a location you'll remember. Later on, to load it back into the tracker, go to "Options" > "Load Tracker Progress." If you have not done a new randomizer seed since saving, you can use the autosave mod to load back into your seed. Otherwise, make sure to make a hard save in KH2 before closing out your randomizer.

# Battleship Tracker

The randomizer community has found several new ways to enjoy the randomizer that calls for some novelty trackers. At the moment, the only documented one is the Battleship Tracker though others may arise in the future. The Battleship tracker can be used to play custom game modes such as (but not limited to) Battleships, Boss Enemy Bingo, and Hitlist. The tracker can be found and installed [here](https://github.com/roromaniac/KH2FM-Rando-Battleship/releases). Unless you want to playtest the newest version of the tracker, it is recommended you utilize the latest stable release.

### Instructions for Battleship

### Instructions for Bingo

### Instructions for Boss Enemy

### Instructions for Maze Mode

### Instructions for Hitlist

To generate a hitlist seed, open the tracker and navigate to "Actions" > "Load Preset". An explorer window should open up in your presets folder. Select "hitlist.txt". For your first time loading in the preset, the tracker will not change size and the images may appear stretched. Resize the tracker window so that the images are of the appropriate size; resizing the tracker window will save the tracker size and position for each particular preset, so your hitlist tracker will default to the new position and sizing the next time you elect to play hitlist. 

As of (1/13/2023), the tracker does not support autotracking for hitlist, though it _is currently in development_. **Do not use autotracking with hitlist** because the tracker will not prevent you from doing so. However, it will track all the non-data versions of boss fights because the autotracker at the moment does not distinguish between data and original versions of Organization XIII fights.
