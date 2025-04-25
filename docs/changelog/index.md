# Changelog

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
