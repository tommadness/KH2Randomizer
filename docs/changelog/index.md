# Changelog

## 3.2.2 (2026-04-23)

Features
* Helper buttons for Visit Unlocks, Equipment, Junk Items, Growth, and Magic to make selection easier
* Seed copy button in spoiler logs

Bugfixes
* DDD Music Randomization looks at the correct folder
* Drive Objectives now can be customized
* Boss/Enemy Only seeds no longer carry extra unrelated modifications.

## 3.2.1 (2026-04-04)

Hotfix to battle level scaling for final fights

## 3.2.0 (2026-04-04)

Features
* Vanilla Keyblade abilities and stats options
* Battle Level Scaling based on Spheres (scaling based on logical access)
* Battle Level Setting to force final fights to be LV50 even if TWTNW is not (courtesy of Num/Zeddikus)
* Keyblade Locking Chests configurable by world (with corresponding tracker update from roromaniac8)
* Ability to customize starting with specific magic/movement/visit unlocks and a range of random ones. 
* Custom Objective Pool support
* Armor/Accessories can have randomized abilities (will update description with replaced ability)
* Configurable Bonus Stat Reward Pool (HP/MP/Slots)
* Configurable Shop Prices for added shop items
* Non-second Visit Item Depth (excludes second visits of GoA portal worlds)
* Level Slot randomization option (same number of slots available on levels, just random which levels have the items)

QoL
* Seed string copy formatting for pasting to Discord (opt-in)
* Custom command menu cosmetic support
* Texture preset improvements
* Starting with all visit unlocks should disable the tracker from tracking all the unlocks to GoA
* Donald/Goofy AP can increment by 1 instead of 5 (minimum is still 5/4 respectively due to ModManager)
* Small seed checking lua file to check if the seed was added into the game properly

Bugfixes
* Valor/Final in the second slot of bonuses shouldn't fail to track anymore
* Random preset should be random
* Keyblade slots should no longer show as unreachable in the spoiler log (unless they are actually unreachable)

Detailed Notes for Custom Cosmetics (courtesy of equations19)
* incorporate a lot of the player feedback to rework the cosmetics menu's layout, in hopes of simplifying its use
  * add windows to display the custom keyblades, command menus, itempics, room transitions, ending screens
  * rearrange some of the options to hopefully make it less confusing which ones go together
  * cosmetic settings that have an additional options screen now include an "additional settings" button inline with the associated setting, rather than a separate button below
  * separate music options into sections for KH games music and custom music to make it clearer which are overall settings and which go with the individual music pools
  * music summary is formatted as a grid now
  * if isn't set up yet for a particular cosmetic setting, try to guide the player on what to do in-app rather than just giving a popup message or silently having options be disabled
* add the ability to download custom keyblade packs for KH1 and BBS, with permission from the mod authors
* Generalize keyblade importing to support more mods
* Adds a basic OpenKH mod.yml parser that can use a mod.yml file to determine the locations of keyblade models, textures, etc., rather than having to bake them into code. This (in theory) enables most well-formed keyblade replacement mods to be able to have their keyblade(s) imported into the seed generator without any work from the mod author.
* Add a setting to replace GoA keyblades


## 3.1.2 (2025-04-25)

Fixing starting inventory causing problems with journal text

## 3.1.1 (2025-04-25)

### Settings

* Added 7 Random and 9 Random growth options
* Added new options to limit stat growth on level ups
  * The default remains to allow double stat growth on all levels 1-99

### Changes

* Spoiler hints in reports should now only show hinted items, not all trackable
* Data Roxas will no longer be considered part of the first visit
* Multiple copies of the same visit unlock item will not be added to shops, and other copies are still placed elsewhere
* Fix vanilla magnet location for Luxord in The World that Never Was
* Marluxia and Oogie Boogie can now have their textures recolored

## 3.1.0 (2025-02-02)

### Settings

* Updated visit locking to allow first visits to be locked. Visit availability options are moved to the Locations tab
  instead of the Starting Inventory tab.
* New options for unlocking the Final Door (alternatives to Three Proofs)
  * Objectives - requires completing a set of objectives from a given list
  * Emblems - requires finding a certain number of Emblems placed in the game
* Expanded Starting Inventory options
  * Torn Pages
  * Drive Forms
  * Summons
  * Magics
  * Keyblades
  * Expanded Starting Abilities
* Glass Cannon removed and replaced with new settings for controlling relative rates of strength, magic, defense, and
  AP increases
* New Hints setting for revealing locations of select abilities in the Ansem Report text in Jiminy's Journal
* New setting to configure whether Munny Pouches are included in the randomized item pool or not
* Updated Item Placement to allow for a configurable placement bias for each individual item type. This replaces what
  were previously two related concepts (Item Placement Difficulty and items having a "rarity").
* Updated Random Battle Levels to allow for a configurable minimum and maximum random battle level rather than a set
  range of 1-50.
* New Challenge Modifier that requires Sora to have certain keyblades to open chests in the different worlds.
* Expanded Challenge Modifier options for restricting Final Form
* New Companions tab with settings for configuring Donald and Goofy's attacks/damage
* New Cosmetics setting for recoloring many in-game textures
* New Cosmetics setting for randomizing keyblades
* New Cosmetics settings for customizing item pictures, room transitions, and the ending picture
* New Cosmetics setting for adding some randomizer-themed textures to the game
* Removed options for Remove Cutscenes and Randomize Character Costumes for the time being
  * These are known to be problematic and cause confusion for players
  * See the Discord for an alternative cutscene skipper mod

### Changes

* Continued visual updates to the seed generator
* Spoiler log now displays the logical "sphere" of each location
* Ansem Report text in Jiminy's Journal now includes the hint text from the various hint systems
* Armor and accessories are now placed into their own category for the Chest Visuals Match Contents setting
* Progression Point thresholds can now be exported to and imported from CSV

## 3.0.3 (2023-10-01)

* KHBR updated to 4.0.5
* Spoiler hints with boss rando fixed
* Vanilla MCP health bug fixed

## 3.0.2 (2023-09-03)

* Fixing some duplicate cmd patching, which resulted in some vanilla looking sections of the game
* KHBR updated to 4.0.4, fixing some boss/enemy related issues
* Minor fix to loading presets from before vanilla world options

## 3.0.1 (2023-08-12)

* Better Spoiler Log (includes the settings, synth, shop)
* Softlock fixes (Setzer winner/loser item fix, picture on puzzles, synth logic)
* Boss/Enemy only mod button (useful for Archipelago)
* Additional validation on loading seeds from seed strings
* Chest Visuals Match Contents - change the texture on chests based on the item inside
* Various UI and logic fixes
* KHBR updated to 4.0.3 https://github.com/thundrio-kh/khbr/blob/master/CHANGELOG

## 3.0.0 (2023-01-21)

* Updated visual overhaul
* Vanilla World Options (not fully vanilla items in each world, just the notable unique items, such as abilities, keyblades, and the tracker items)
* Added Start with 3 Random Growths
* Custom Hintable Item Set
* Progression Hint Variation - Instead of relying on reports to give hints, world progress gives you points which can unlock hints for you (requires updated KH2Tracker)
* Custom Set Bonus Rewards for Point Hint Mode
* Antiform Item can be added into the Item Pool
* Randomized Stackable Abilities Option
* Option to add N Random Visit Unlocks to the Shop
* Option to add N Random Reports to the Shop
* Option to add all Keyblades, Elixirs, Drive Recoveries, and Stat Boosts to the Shop
* Beatable Accessibility Option - Some locations may be unreachable, but 3 proofs will always be obtainable
* Nightmare Item Logic renamed to Extended Item Placement Logic, no functional change
* Chain Logic - Force a sequence of unlocks that ends in Proof of Nonexistence
* QoL for Beast's Castle Wardrobe never waking up, Olympus Urns dropping lots of orbs, and Skipping Atlantica music tutorial (don't skip cutscene after the skipped tutorial)
* Cutscene Remover Option (Beta)
* Randomized Party Members (Beta)
* Randomized Revenge Value (Beta)
* Global Jackpot/Lucky Lucky modifiers - Make overworld enemies drop much more
* Make all overworld enemies drop munny or mp orbs
* Disable Final Form option - Makes final form cost 10 drive, so can never enter it. Can still be found for Genie forms and unlocking Form Level 7 checks
* Battle Level Randomization - Change the difficulty of the worlds
* Boss/Enemy Randomization Updates - KHBR updated to 3.0.0 https://github.com/thundrio-kh/khbr/blob/master/CHANGELOG
* Randomize Character Costumes (Beta)
* Updated Music Rando (requires updated OpenKH Mod Manager)
* Updated Daily Seeds (should be more stable, feel free to suggest new modifications)
* Updated Rando Rando (now called Randomized Settings) - choose a subset of settings to pick at random
* Pick a Random Preset - From your presets, let the generator pick a random one.
* Tourney Seed Generator - You can now bulk generate seeds for tourneys, with a full list of seeds/spoiler logs
