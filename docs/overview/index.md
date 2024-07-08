# Overview

* [Notable Randomizer Changes](#notable-randomizer-changes)
* [Win Conditions](#win-conditions)
* [Known Issues](#known-issues)

## Notable Randomizer Changes

Some of these are specific changes made for randomizer, others are just things that can only happen in randomizer due to
having tools you weren't otherwise meant to have in certain parts of the game.

### General

* Sora starts the game with a Drive Gauge of 5 rather than 3 so that all Drive Forms can be used as soon as they are
  obtained
* Finding a Munny Pouch gives you 5,000 munny
* Final Form is an obtainable item, though Final Form can still be obtained in its normal fashion
    * Randomizer removes the restriction that usually requires the player to progress past Roxas in The World That Never
      Was before Final Form can be unlocked
* The Promise Charm item, if enabled, opens a path to the final boss fights if the Promise Charm is obtained, in
  addition to satisfying the [Final Door Requirement](../glossary/index.md#final-door-requirement). This path also
  contains several Bulky Vendor enemies that can be used to level grind quickly.

### Save Warping

Because there is no world map from which to choose a spawn point, the player is placed at an appropriate save point
when (re-)entering a world based on story progression. This can be exploited in a few places in randomizer to save some
time by leaving a world and re-entering to be "warped" to the next location. The warps that can save time include but
are not limited to:

* After the "fight" with Beast, leaving Beast's Castle and re-entering places you in Belle's room
* After triggering the Rumbling Rose cutscene, leaving Beast's Castle and re-entering places you in the Parlor
* After entering the Courtyard, leaving Disney Castle and re-entering places you in the Library
* After triggering the cutscene by entering the Nothing's Call room, leaving The World That Never Was and re-entering
  places you at Twilight's View
    * This particular save warp does bypass two treasure chests, so is usually only utilized if a player is trying to
      get to the end of the game as quickly as possible
* After Auron gets on the boat to the Underdrome with Pain and Panic, leaving Olympus Coliseum and re-entering places
  you at Cave Of the Dead - Inner Chamber

### The World That Never Was

* The door to the final fights is locked until the seed's configured
  [Final Door Requirement](../glossary/index.md#final-door-requirement) is satisfied
* The Dragon Xemnas fight is removed
* Final Xemnas (and Data Final Xemnas) can be defeated without Xemnas using the "laser dome" desperation move. This can
  be done by depleting all his health before he has a chance to start the laser dome move.

### Land of Dragons

* If you have the tools to gain enough height, you can jump over a cutscene trigger before the Shan-Yu fight and enter
  the Throne Room to acquire its many treasure chests early

### Halloween Town

* Oogie Boogie has fewer forced HP gates and cycles

### Agrabah

* The shadow Jafar chase sequences when riding the magic carpet are shortened slightly

### Olympus Coliseum

* Obtaining the Olympus Stone item unlocks the Drive Gauge in the underworld, allowing Drive Forms and Summons to be
  used
* Obtaining the Hades Cup Trophy item unlocks all Underdrome Cups early
* Only one Pete fight is required (the timed fight is removed)

### Pride Lands

* Lion Sora starts the game with the Dash ability, rather than obtaining it later
* The second battle with the hyenas only requires one hyena to be defeated, rather than all three

### Hollow Bastion / Radiant Garden

* A checkpoint is added after the Demyx fight
    * This means if you die in the subsequent "Final Fantasy" fights, you do not need to re-fight Demyx
    * This also allows Sora to use Wisdom Form for Final Fantasy fights since Donald is in the party at this time (and
      those fights are a great place to earn levels for Wisdom Form)
* The Proof of Peace unlocks the two rewards given by Mushroom XIII. Simply talk to the Mushrooms after obtaining the
  Proof of Peace to obtain the rewards.
* The Unknown Disk unlocks the Heartless Manufactory early
* A loading zone is added in an out-of-bounds area of the Cavern of Remembrance to prevent Sora from falling
  infinitely (effectively softlocking the game).
    * This area of the cavern is used in a technique called "CoR skip" where players clip out-of-bounds in order to
      bypass difficult fights in this area
    * Instead of falling forever, once Sora hits this added loading zone, the game warps Sora back to the entrance to
      the cavern

### Disney Castle

* The Proof of Connection unlocks the battle with Lingering Will

### Space Paranoids

* The initial Light Cycle race is removed
* Master Control Program has reduced health
* After defeating Master Control Program, the Solar Sailer Heartless fight is skipped, allowing you to travel back and
  forth without needing to fight again each time

### 100 Acre Wood

* The minigames for A Blustery Rescue and Hunny Slider are sped up

### Simulated Twilight Town (STT)

* Choose any of the jobs and quit right after the starting timer to progress the story on Day 2
    * It is not required to actually complete a job, nor is it required to go talk to Hayner to progress the story
* The Seven Wonders minigames on Day 5 are removed
* Limit Form can be used as Roxas if it has been obtained (Roxas turns into Limit Form Sora)
    * In most areas of STT, reverting from Limit Form will leave you with a full Drive Gauge
* Roxas can use High Jump, Quick Run, Aerial Dodge, and Glide even though his model does not have animations for those
  abilities. Dodge Roll cannot be used (the randomizer un-equips Dodge Roll once you enter STT).
    * As of release 2.1, the randomizer seed generator has a "Roxas Magic/Movement/Trinity" option that, when enabled,
      ports Sora's movement animations to Roxas, therefore allowing Roxas to use all of the movement abilities properly,
      as well as magic and Trinity Limit.

## Win Conditions

The community has come up with several common variations on how to "win" the game. Several common ones are outlined
here.

### Beat Final Xemnas

The primary goal is to defeat Final Xemnas (the normal final boss of the game) at the end of The World That Never Was.
However, the door to the final battles remains locked until the
[Final Door Requirement](../glossary/index.md#final-door-requirement) for the seed is satisfied.

If the Promise Charm item is enabled for the seed, once the Promise Charm is obtained and the Final Door Requirement is
satisfied, the computer at the center of the Garden of Assemblage opens a path to skip over The World That Never Was and
go straight to the final fight gauntlet. This path also contains several Bulky Vendor enemies that give large amounts of
experience points for a way to gain levels quickly.

### All Blue Numbers (ABN)

The goal is to obtain all items designated as Important Checks for the seed. Since the original version of the item
tracker used a blue number to designate all Important Checks are found in a location, the player knows every Important
Check in the game is found once all numbers in the tracker are "blue".

* The original hint system for this win condition is the [Shananas](../hints/shananas) hint system which simply counts
  the number of Important Checks found in each location.
* The [Points](../hints/points) hint system can also be used for this win condition. In this variant, the numbers in the tracker
  will all end up at 0 (as well as being "blue") once all Important Checks in the game are found.

Some variations of this win condition consider the game won immediately once the final Important Check is found and
shown on the tracker. Other variations also require Final Xemnas to be defeated after all Important Checks are found.

### Hit List

The player is given a certain number of objectives to fulfill (usually defeating either certain story bosses or
superbosses). The goal is to fulfill all or a subset of these objectives.

Some variations of this win condition consider the game won immediately once the final Hit List objective is fulfilled.
Other variations also require Final Xemnas to be defeated after all required Hit List objectives are fulfilled.

### Bingo

The player is given a Bingo board and must complete several tasks to fill in squares on the board, either to make one or
more lines of Bingo, or to fill in all squares on the board (known as Blackout Bingo).

### Timed Points

The goal is to earn as many points as possible within a designated time limit (one hour being the most commonly used
time limit). Points are earned by obtaining items in the game as well as accomplishing certain tasks in the game (such
as defeating bosses).

This mode is often used with random boss/enemy placement.

## Known Issues

Some of these issues exist in the base game, while others are specific to the randomizer.

### Halloween Town

* Using the finisher of Dance Call to kill The Experiment causes the game to crash. It's often recommended to outright
  avoid using Dance Call to finish this fight.
    * As of release 1.53.5, the Garden of Assemblage mod has implemented a fix for this crash.

### Twilight Town

* Using the Trinity Limit finisher on the Station Nobodies fight can sometimes cause the game to crash. A suggested
  workaround is to kill the first 3-4 waves of enemies before starting Trinity Limit (or just don't use Trinity Limit at
  all in this fight).
    * As of release 1.53.5, the Garden of Assemblage mod has implemented a fix for this crash.
    
### Hollow Bastion / Radiant Garden

* On the PCSX2 Emulator version of the game, the game sometimes crashes when obtaining the rewards from Mushroom XIII.
  It is recommended to save and/or create a save state before talking to the Mushrooms.

### Port Royal

* On the PC versions of the game, the game sometimes crashes when choosing a location on the map (commonly known as
  "map crash"). It is recommended to save anytime you're about to talk to Jack on the ship to choose a destination.
    * As of release 2.1, the randomizer seed generator has a "Remove Port Royal Map Select" option that, when enabled,
      replaces the map location selection screen with simple text options, hopefully preventing the crash altogether.

### Simulated Twilight Town (STT)

* Roxas will T-pose if you use Dodge Roll or Trinity Limit (the randomizer un-equips these abilities once you enter STT,
  so this is semi-difficult to do accidentally)
* Being in Limit Form when Twilight Thorn starts the Reaction command sequence will softlock the game, as Sora does not
  have animations for the Reaction commands in this fight

Note that as of release 2.1, the randomizer seed generator has a "Roxas Magic/Movement/Trinity" option that, when
enabled, ports Sora's animations to Roxas, eliminating these T-poses/softlocks.
