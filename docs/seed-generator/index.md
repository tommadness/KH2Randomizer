# Seed Generator

* [General / FAQ](#general--faq)
* [Options](#options)
    * [Menus](#menus)
    * [Locations](#locations)
    * [EXP/Stats](#expstats)
    * [Starting Inventory](#starting-inventory)
    * [Hints](#hints)
    * [Keyblades](#keyblades)
    * [Item Pool](#item-pool)
    * [Item Placement](#item-placement)
    * [Seed Modifiers](#seed-modifiers)
    * [Boss/Enemy](#bossenemy)
    * [Cosmetics](#cosmetics)

# General / FAQ

### What version of Kingdom Hearts II can this be used with?

This seed generator can be used with either the PC (Epic Games Store) or PCSX2 (emulated) version of Kingdom Hearts II:
Final Mix. This will not work with Kingdom Hearts II (US PS2), and is not supported on the console versions of the game.

### What are the differences between this and [Valaxor's Seed Generator](https://randomizer.valaxor.com/#/seed)?

This seed generator is designed to be used with the [OpenKH](https://openkh.dev/) Mods Manager, which enables many extra
features. See [Options](#options) below for a list of all the configuration options available using this seed generator.

### What is a Seed Hash?

See [Seed Hash](../glossary/index.md#seed-hash) for details.

### What is a Visit Unlock?

See [Visit Unlock](../glossary/index.md#visit-unlock) for details.

### Why are Consumables considered "junk"?

"Junk" is a bit of a misnomer. After all "one-off" items (equipment, abilities, Important Checks, maps) are placed, all
remaining locations are filled randomly with Synthesis Materials or Consumables, as the quantity of those per seed don't
necessarily matter. So the term "junk" in this context includes things like Potions, AP Boosts, Drive Recoveries, etc.

# Options

## Menus

### Share Seed

**Save Seed to Clipboard** - Copies information about the currently configured seed to the clipboard so that you can
send the same seed to other players. This is the recommended way to share seeds (sharing the seed `.zip` file itself is
not guaranteed to work, especially if custom cosmetics are used).

**Load Seed from Clipboard** - Loads a seed configuration from the clipboard into the generator.

### Preset

**Open Preset Folder** - Opens the folder containing preset configurations. Can be useful for sharing presets with
others, or renaming or deleting a preset.

**Save Settings as New Preset** - Saves the current settings as a preset configuration that can be quickly chosen later.

**Load a Preset** - Lists the presets available for choosing.

**Pick a Random Preset** - Allows for the generator to choose one of your presets at random.

### Daily Seeds

Allows you to load one of the current day's [daily seeds](../daily-seeds/index.md) into the generator.

### Randomize Settings

Allows for the generator to choose among a set of random settings for you to play.

### Tourney Seeds

Allows a tournament organizer to quickly generate a set of tournament seeds that can be easily shared with other
tournament organizers/assistants.

### Configure

**LuaBackend Hook Setup** - Allows you to easily install and/or configure
[LuaBackend Hook](../luabackend-hook-setup/index.md) (only applies to the PC version of the game).

**Find OpenKH Folder** - Displays a folder chooser allowing you to configure the location of your OpenKH Mods Manager.
This is currently only used for music randomization on the PC version of the game, but its use may expand over time.

**Choose Custom Music Folder** - Displays a folder chooser allowing you to configure the location of custom music that
you would like to include in music randomization. See [Randomized Music](../music/index.md) for more information.

**Choose Custom Visuals Folder** - Displays a folder chooser allowing you to configure the location of custom visuals
that you would like to include in some cosmetic randomization settings.

**Remember Window Size/Position** - If checked, the seed generator application attempts to open at the same size and
position it was the last time it was closed.

### About

Displays a window with information about the seed generator.

### Seed

The name of the seed to generate. The seed settings, along with this name, determine the placement for all things
randomized by the generator.

### Make Spoiler Log

If enabled, adds a file to the generated seed `.zip` file detailing the locations of all the randomized items, as well
as other information about the seed.

* Note that enabling/disabling the spoiler log results in 2 completely different seeds, to prevent someone who knows a
  seed name from generating a spoiler log for a seed that was not intended to have a spoiler log (i.e. a seed for a race
  or tournament).

## Locations

**Max Level Reward** - Controls the maximum level that can contain a randomized reward.

* Note that the `Level 1` option means you must choose either `Vanilla` or `Junk` rewards for Levels.

**Dream Weapon Matters** - At the beginning of a seed, the dream weapon you choose will determine when you get items
from levels. When disabled, all weapons will give the same items on the same levels.

**Critical Bonuses** - If enabled, the 7 starting items on Critical Mode can contain randomized rewards.

> Only enable this option if you plan to play on Critical Mode, or you may prevent yourself from obtaining those
> randomized rewards.

**Garden of Assemblage** - If enabled, the 3 chests in the Garden of Assemblage can contain randomized rewards.

**Remove Non-Superboss Popups** - If enabled, removes story popup and bonus rewards from the eligible location pool for
non-junk items. This setting is primary used for door rando.

### Worlds

Allows you to select whether each world has one of the following:

* Rando - This location can contain randomized rewards.
* Vanilla - This location will have its notable unique items in their vanilla locations from the game. All other
  locations will get junk items.
* Junk - This location will only contain junk items.

### Superbosses / Misc Locations

Allows you to select whether each superboss/location can contain randomized rewards.

Any of the `Misc Locations` can be enabled independent of what world it normally is in (e.g. Olympus Cups can be
enabled without enabling Olympus Coliseum).

## EXP/Stats

**Glass Cannon** - Prevents Defense increases from appearing in the level-up randomized rewards pool.

**Sora Starting AP** - Sora begins the game with this much AP.

**Donald Starting AP** - Donald begins the game with this much AP.

**Goofy Starting AP** - Goofy begins the game with this much AP.

### Experience Multipliers

Adjusts the amount of experience needed to reach each level. Sora's level, Drive Form levels, and Summon levels are all
configurable.

* Example: If the game normally requires 1000 EXP to reach level 2, setting the multiplier to 2.0 changes the game to
  require only 500 EXP to reach level 2.

### Experience Curves

Allows for further customization of experience rates, inspired by a similar concept in Kingdom Hearts I.

* Dawn (Normal) - The default EXP rate.
* Midday - Early levels (up to 50 for Sora, levels 2-4 for Drive Forms and Summons) require more experience, but later
  levels require less.
* Dusk - Early levels (up to 50 for Sora, levels 2-4 for Drive Forms and Summons) require even more experience, but
  later levels require even less.

## Starting Inventory

### Starting Inventory Options

**Starting Abilities Equipped** - If enabled, all starting abilities will be automatically equipped (except those coming
from critical bonuses).

**Starting Ansem Reports** - Begin the game with this many Ansem Reports already acquired (will randomly choose among
the reports).

**Growth Ability Starting Level** - Select how many growth abilities you want to start with.

* None
* 3 Random - Pick 3 individual growth abilities to add at the start (e.g. you could start with High Jump LV1 and Dodge
  Roll LV2).
* 5 Random - Pick 5 individual growth abilities to add at the start (e.g. you could start with High Jump LV1, Dodge Roll
  LV1, and Glide LV3).
* Level 1 - All growths start at level 1.
* Level 2 - All growths start at level 2.
* Level 3 - All growths start at level 3.
* Max - All growths start at the maximum level.

### Starting Inventory

Begin the game with each selected item/ability already acquired.

### Starting Visit Unlocks

Begin the game with each selected [visit unlock](../glossary/index.md#visit-unlock) already acquired.

* Starting with no visit unlocks means you'll need to find the visit unlocks to progress into second/third visits of
  worlds.
* Starting with all visit unlocks means all second/third visits will be available.

## Hints

**Hint System** - Controls which hint system to use.

* See the main [Hints](../hints/index.md) page for explanations of the different hint systems and their options.

## Keyblades

### Keyblade Statistics

**Keyblade Min/Max Stat** - Controls the minimum and maximum strength and magic stat that each keyblade can have.

### Support/Action Keyblade-Eligible Abilities

Controls the abilities that are eligible to be randomized onto keyblades. Any abilities not selected are guaranteed to
not be attached to a keyblade.

> Note that there must be enough keyblade-eligible abilities chosen such that each keyblade gets an ability, or the seed
> will fail to generate.

## Item Pool

### Include in Item Pool

**Bonus Rewards as Items (Statsanity)** - If enabled, takes HP, MP, Drive, Accessory Slot, Armor Slot, and Item Slot
upgrades from the normal bonus popup locations and lets them appear in chests or other randomized locations. Those bonus
popup locations can now have other randomized rewards.

**50 AP Boosts** - Adds 50 guaranteed AP Boosts into the item pool.

**Promise Charm** - If enabled, the Promise Charm item will be added to the randomized item pool, which can allow
skipping The World That Never Was by interacting with the computer in the Garden of Assemblage once you have all 3 Proof
items as well as the Promise Charm.

**Antiform** - If enabled, adds Antiform as an obtainable form.

**Maps** - If enabled, adds maps to the item pool.

**Synthesis Recipes** - If enabled, adds synthesis recipes to the item pool. Recipes are NOT required when synthesis
rewards are randomized.

**Accessories** - If enabled, all accessories are included in the item pool.

**Armor** - If enabled, all armor items are included in the item pool.

**Ability Pool** - Controls the presence and amount of abilities in the randomized pool.

* Default Abilities - Uses the default set of action and support abilities.
* Randomize Ability Pool - Chooses Sora's action/support abilities at random (guaranteed to have one Second Chance and
  one Once More ability).
* Randomize Support Ability Pool - Leaves Sora's action abilities alone, but will randomize the support abilities (still
  guaranteed to have one Second Chance and one Once More).
* Randomize Stackable Abilities - Always includes 1 of each ability that works on its own, but will randomize how many
  of the stackable abilities you can get (guaranteeing at least 1 of each).

### Randomized Shop

**Add Visit Unlocks To Shop** - Adds a number of visit unlocks into the Moogle shop.

**Add Ansem Reports To Shop** - Adds a number of Ansem Reports into the Moogle shop.

### Guaranteed Shop Items

**Keyblades** - Adds duplicates of each keyblade into the Moogle shop.

**Elixirs** - Adds Elixir and Megalixir into the Moogle shop.

**Drive Recoveries** - Adds Drive Recovery and High Drive Recovery into the Moogle shop.

**Stat Boosts** - Adds Power Boost, Magic Boost, Defense Boost, and AP Boost into the Moogle shop.

### Junk Items

Once all of the required items are placed, items from this list are used to fill the remaining locations. This item pool
is also used for worlds/locations that are configured to contain only junk.

## Item Placement

### Where Items Can Go

**Accessibility** - How accessible locations need to be for the seed to be "completable".

* 100% Locations - All locations must be reachable, and nothing will be permanently locked.
* Beatable - The 3 proofs must be reachable, but nothing else is guaranteed.

**Softlock Prevention** - An option to change the softlock prevention method in use. Default option is `Regular Rando`
which is correct for most cases, but if you play reverse rando or are doing a co-op with someone playing reverse rando,
you can select other softlock preventions options for those cases.

**Item Placement Difficulty** - Configures the placement of items to be biased based on how easy/difficult you would
like the seed to be. Items have four categories (`Common`, `Uncommon`, `Rare`, `Mythic`) that influence what bias each
item gets when placing those items. `Super Easy` and `Easy` will bias `Rare` and `Mythic` items early, while placements
harder than `Normal` will bias those items later.

**Extended Item Placement Logic** - If enabled, auto forms (Auto Valor, Auto Wisdom, etc.) may be required to make
progress in your seed. Additionally, if item placement difficulty is one of the options besides `Normal`, keyblades with
good abilities will be weighted as well.

**Visit Unlock Category** - Used in tandem with `Item Placement Difficulty`, the visit unlocks can be changed between
the four item categories (`Common`, `Uncommon`, `Rare`, `Mythic`).

**Visit Unlock Depth** - Configures locations where the visit unlocks can be placed.

### Proof Restrictions

**Yeet The Bear Required** - If enabled, forces the Proof of Nonexistence onto the popup reward from 100 Acre Wood -
Starry Hill, thus requiring The Hunny Pot minigame to be completed in order to obtain the Proof.

**Proof Depth** - Configures locations where the three Proof items can be placed.

### Chain Logic

**Turn On Chain Logic** - If enabled, places items that can block progress in a chain with one another, making the seed
very linear.

**Maximum Logic Length** - How many steps in the logic chain you'd like to do at most.

**Include Lingering Will in Chain** - If enabled, puts the Proof of Connection into the logic chain, effectively
requiring beating Lingering Will.

**Force Late Depth for Proof of Connection** - If enabled, forces the Proof of Connection to be in the last 5 steps of
the chain, to give more chances for finding combat tools.

## Seed Modifiers

### Quality of Life

**Roxas Magic/Movement/Trinity** - If enabled, Roxas will be given all the animations of Sora, allowing for the use of
all actions in Simulated Twilight Town.

**Skip Magic Carpet Escape** - If enabled, the entire autoscrolling segment of Agrabah's second visit after exiting the
Ruined Chamber will be skipped.

**Remove Port Royal Map Select** - If enabled, the map for the boat travel in Port Royal will be replaced with text
options. Useful to avoid crashes that are more likely on PC.

**Remove Wardrobe Wakeup Animation** - If enabled, the wardrobe in Beast's Castle will not wake up when pushing it.

**Fast Olympus Coliseum Urns** - If enabled, the urns in the minigame in Olympus Coliseum drop more orbs, making the
minigame much faster.

**Skip Atlantica Minigame Tutorial** - If enabled, skips the Atlantica music tutorial (not the swimming tutorial).

**Remove Cutscenes** - Removes all cutscenes from the game. As a consequence there are occassionally strange
flashes/backgrounds when in a spot a cutscene would normally occur.

### Other Modifiers

**Split AS/Data Rewards** - Controls how rewards are given for Absent Silhouette fights.

* If enabled, Absent Silhouette rewards will _NOT_ give the reward from their Data versions. You must beat the Data
  version to get the Data-specific reward.
* If disabled, beating the Absent Silhouette gives rewards from the Data version as well as the Absent Silhouette
  version

**Cups Give Experience** - If enabled, experience for party members and Drive Forms can be earned while in an Olympus
Coliseum cup

**Retry Data Final Xemnas** - If enabled, if you die to Data Final Xemnas, Continue will spawn you right back into the
fight, instead of having to fight Data Xemnas I again.

> **Warning** - if you are unable to beat Data Final Xemnas, there is no way to exit, essentially causing a softlock,
> and you'll have to load a save.

**Retry Dark Thorn** - If enabled, if you die to Dark Thorn (Beast Castle first visit boss), Continue will spawn you
right back into the fight, instead of having to fight Shadow Stalker again. Especially useful in Boss rando.

> **Warning** - if you are unable to beat Dark Thorn, there is no way to exit, essentially causing a softlock, and
> you'll have to load a save.

**Remove Damage Cap** - Removes the damage cap for every enemy/boss in the game.

**Chest Visuals Match Contents** - If enabled, treasure chests will visually indicate the type of item they contain.
See [Chest Visuals](chests/index.md) for more details.

**Randomize World Party Members (Beta)** - Randomizes the world-specific party member in each world (e.g. Tron may
appear in Olympus Coliseum rather than Auron).

**Randomize Revenge Limit Maximum (Beta)** - Randomizes the revenge value limit of each enemy/boss in the game. Vanilla
uses the default values. Can also be set to 0, set to basically infinity, randomly swapped, or set to a random value
between 0 and 200.

### Drops

**Global Jackpots** - Increases orb/munny drops as if you had this many Jackpot abilities equipped. Each additional
Jackpot adds 50% of the original amount.

**Global Lucky Lucky** - Increases item drops as if you had this many Lucky Lucky abilities equipped. Each additional
Lucky Lucky adds 50 percent of the chance to drop the item.

**All Enemies Drop Munny** - Enemies will all drop munny.

**All Enemies Drop MP Orbs** - Enemies will all drop MP orbs.

### Challenge Modifiers

**Block Skipping CoR** - Disables skipping into the Cavern of Remembrance, instead requiring completion of the fight(s)
to progress.

**Block Skipping Shan-Yu** - Disables skipping into the Throne Room of Land of Dragons, instead requiring beating
Shan-Yu to progress.

**Disable Final Form** - Disables going into Final Form in any way. Final Form can still be found to let other forms
level up and for Final Genie. All rewards from Final Form are replaced with junk.

### Battle Levels

**Battle Level Choice** - Configures how the world battle levels are chosen.

* Normal - Battle levels are unchanged.
* Shuffle - Shuffles the normal battle levels among all visits of all worlds.
* Offset - Increases or decreases all battle levels by a chosen amount.
* Within Range of Normal - Chooses a random battle level for each world visit within a chosen range above or below the
  visit's normal battle level.
* Random (Max 50) - Chooses a random battle level for each world visit within a range of 1-50.
* Scale to 50 - All last visits are set to battle level 50, with previous visits to the same world scaled
  proportionally.

## Boss/Enemy

### Bosses

**Boss Randomization Mode** - Controls if and how the bosses should be randomized.

* One-to-One - Shuffles around where the bosses are located, but each boss is still present (some bosses may be
  excluded from the randomization).
* Wild - Randomly picks an available boss for every location, meaning some bosses can be seen more than once, and some
  may never be seen. If a selected boss is filled in, this setting is ignored and every boss (almost) will become that
  boss.

**Selected Boss** - Replaces every boss possible with the selected boss. Depending on the boss, this may not result in a
completable seed. This value is ignored if Boss Randomization Mode is not "Selected Boss".

**Nightmare Bosses** - If enabled, replaces bosses using only the most difficult bosses in the game, and forces Boss
Randomization Mode to be "Wild".

**Bosses Can Replace Enemies** - If enabled, replaces 0.5 percent of enemies in the game with a random boss. This option
is intended for PC use only.

**Randomize Cups Bosses** - If enabled, includes the Olympus Coliseum cups bosses in the randomization pool.

**Randomize Data Bosses** - If enabled, includes the Data versions of Organization XII members in the pool.

**Include more locations** - If enabled, allows bosses to be placed in more locations that may be exceedingly
difficult/tedious, or that can softlock in certain cases. Example: Allows Sephiroth to replace Blizzard or Volcano Lord.
This option is intended for PC use only.

**Randomize Sephiroth** - If enabled, includes Sephiroth in the pool.

**Randomize Lingering Will** - If enabled, includes Lingering Will (Terra) in the pool.

**Mickey Appearance Settings** - Choose when Mickey appears.

* follow - Mickey appears for the same bosses as in the vanilla game, regardless of their location.
* stay - Mickey appears in the same locations as in the vanilla game, regardless of the bosses placed there.
* all - Mickey will appear for every boss in the game, regardless of whether Mickey normally appears there.
* none - Mickey will never appear. Might make PCSX2 boss fights less stable.

**Scale HP to Original Boss** - If enabled, attempts to force boss levels and HP to the scale of the boss being
replaced. If disabled, uses the game's scaling, which is partially based on the battle level of the world (except for
Data Organization and Lingering Will/Terra which are always level 99).

### Enemies

**Enemy Randomization Mode** - Controls if and how the enemies should be randomized.

* One-to-One - Simple 1:1 replacement (i.e. all Shadows become Dusks).
* One-to-One per room - Similar to One-to-One but every room is re-randomized (so Shadows in Parlor might be Ice Cubes,
  but in Land of Dragons Cave they might be Fire Cubes).
* Wild - Every enemy entity in the game is completely randomized (but due to memory constraints no room can have more
  than 13 unique enemy types). If a selected enemy is filled in, this setting is ignored, and every enemy (almost) will
  become that enemy.

**Selected Enemy** - Replaces every enemy with the selected enemy. Depending on the enemy, this may not result in a
completable seed. This value is ignored if enemy randomization mode is not "Selected Enemy".

**Nightmare Enemies** - If enabled, replaces enemies using only the most difficult enemies in the game.

**Randomize Nobodies Separately** - If enabled, treats Nobodies as a separate type of enemy, so they are only randomized
among themselves.

**Randomize misc enemies as Heartless** - If enabled, randomizes the following enemies as if they were heartless:
Pirates, Bulky Vendors, Bees.

**Combine Enemy Sizes** - Normally, small enemies are randomized separately from big enemies to prevent crashing. On PC
(where this is less likely to crash), small and large enemies are no longer randomized separately if this option is
enabled.

> **Warning** - this setting is experimental and may cause bad crashes

**Combine Melee and Ranged enemies** - Normally, ranged and melee enemies are randomized separate from each other, both
for difficulty and to reduce crashing. On PC (where this is less likely to crash), ranged and melee enemies are no
longer randomized separately if this option is enabled.

> **Warning** - this setting is experimental and may cause bad crashes

### Boss/Enemy-Only Mod

Generates a mod for OpenKH Mods Manager that _only_ randomizes bosses and enemies. Can be useful if using a randomizer
seed generated outside the standard seed generator (using [Archipelago](https://archipelago.gg/) or otherwise).

## Cosmetics

### Visuals

**Command Menu** - controls the appearance of the command menu on-screen

* Vanilla - Command menus will have their normal appearance.
* Randomize (one) - Chooses a single random command menu to use for the entire game.
* Randomize (all) - Chooses random command menus for each world/location that has a unique command menu.
* (individual command menus) - Forces all command menus to have the chosen appearance.

**Randomize Character Costumes (Beta)** - If enabled, randomizes the different costumes that Sora/Donald/Goofy switch
between in the different worlds (i.e. Space Paranoids could now be default Sora, while anywhere default Sora is used
could be Christmas Town Sora).

### Visuals (PC Panacea Only)

_These options will only work properly when using [Panacea](../glossary/index.md#panacea) for loading mods. Things will
likely look incorrect if using any of these options when patching the game._

**Room Transition Images** - controls the appearance of the room transition images

* Vanilla - Room transitions will have their normal appearance.
* Randomize (in-game only) - Chooses a random transition for each world from existing in-game room transition images.
* Randomize (custom only) - Chooses a random transition for each world from the `room-transition-images` folder
  contained within your configured Custom Visuals Folder.
* Randomize (in-game + custom) - Chooses a random transition for each world from both existing in-game transition images
  and the `room-transition-images` folder contained within your configured Custom Visuals Folder.

> Using custom room transition images requires a Custom Visuals Folder to have been configured using the Configure menu
> -> Choose Custom Visuals Folder. Place any custom images into a `room-transition-images` folder within your chosen
> custom visuals folder. Custom images must be in .png format.

### Music

See the main [Randomized Music](../music/index.md) page for instructions.

### External Randomization Executables

Allows external randomization files to be executed every time a seed is generated. This can be used to integrate with
external mods that have their own `Randomize.exe` file (or similar) that must be run in order to randomize their
contents.

### Cosmetics-Only Mod

Generates a mod for OpenKH Mods Manager that _only_ randomizes cosmetics. Can be useful if using a randomizer
seed generated outside the standard seed generator (using [Archipelago](https://archipelago.gg/) or otherwise).
