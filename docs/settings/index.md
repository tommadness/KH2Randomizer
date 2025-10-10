# Settings

* [Menus](#menus)
* [Locations](#locations)
* [Rules/Placement](#rulesplacement)
* [Hints](#hints)
* [Item Pool](#item-pool)
* [Starting Inventory](#starting-inventory)
* [Seed Modifiers](#seed-modifiers)
* [EXP/Stats](#expstats)
* [Keyblades](#keyblades)
* [Companions](#companions)
* [Boss/Enemy](#bossenemy)
* [Cosmetics](#cosmetics)

## Menus

### Share Seed

**Save Seed to Clipboard** - Copies information about the currently configured seed to the clipboard so that you can
send the same seed to other players. This is the recommended way to share seeds (sharing the seed `.zip` file itself is
not guaranteed to work, especially if custom cosmetics are used).

**Load Seed from Clipboard** - Loads a seed from the clipboard into the generator.

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

**Find OpenKH Folder** - Displays a folder chooser allowing you to configure the location of your OpenKH Mods Manager.
This is currently only used for cosmetic replacement on the PC version of the game, but its use may expand over time.

**Choose Custom Music Folder** - Displays a folder chooser allowing you to configure the location of custom music that
you would like to include in music randomization. See [Randomized Music](../music/index.md) for more information.

**Choose Custom Visuals Folder** - Displays a folder chooser allowing you to configure the location of custom visuals
that you would like to include in some cosmetic replacement settings.

**(Keyblade Options)** - See [Randomized Keyblades](../keyblades/index.md) for descriptions of each keyblade option.

**Remember Window Size/Position** - If checked, the seed generator application attempts to open at the same size and
position it was the last time it was closed.

**LuaBackend Hook Setup** - *(This setup has been moved to OpenKH Mods Manager.)*

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

> Note that the `Level 1` option means you must choose either `Vanilla` or `Junk` rewards for Levels.

**Dream Weapon Matters** - At the beginning of a seed, the dream weapon you choose will determine when you get items
from levels. When disabled, all weapons will give the same items on the same levels.

**Critical Bonuses** - If enabled, the 7 starting items on Critical Mode can contain randomized rewards.

> Only enable this option if you plan to play on Critical Mode, or you may prevent yourself from obtaining those
> randomized rewards.

**Garden of Assemblage** - If enabled, the 3 chests in the Garden of Assemblage can contain randomized rewards.

### Starting Visit Availability

**Availability** - How "visits" for worlds that have them (the 13 portal worlds) should be initially available.
        
* All Visits - All visits of all worlds are available from the beginning of the seed.
* First Visits - All first visits are immediately available, but you must find visit unlock items to
  access subsequent visits in each visit-capable world.
* No Visits - No world visits are immediately available, outside the ones that are always present. You
  must find a visit unlock item in the immediately available areas to proceed. 
* Random Visits - Unlock a random set of visits by starting with random visit unlock items. Use `Minimum Visits
  Available` and `Maximum Visits Available` to configure a range of how many.
* Specific Visits - Unlock a specific set of visits by starting with specific visit unlock items. Use the individual 
  location options to configure how many visits to make available at the start for each location.

**Minimum Visits Available** - When using Random Visits, the minimum number of random visits to unlock at the start.
This can be the same as `Maximum Visits Available` to configure an exact number of random visits.

**Maximum Visits Available** - When using Random Visits, the maximum number of random visits to unlock at the start.
This can be the same as `Minimum Visits Available` to configure an exact number of random visits.

**(individual location options)** - When using Specific Visits, the number of visits to make available at the start for
each location.

### Worlds

Allows you to select whether each world has one of the following:

* Randomized - This location can contain randomized rewards.
* Vanilla - This location will have its notable unique items in their vanilla locations from the game. All other
  locations will get junk items.
* Junk - This location will only contain junk items.

### Superbosses / Misc Locations

Allows you to select whether each superboss/location can contain randomized rewards.

Any of the `Misc Locations` can be enabled independently of the associated world (e.g. Olympus Cups can be enabled
without enabling Olympus Coliseum).

**Remove Non-Superboss Popups** - If enabled, removes story popup and bonus rewards from the eligible location pool for
non-junk items. This setting is primary used for door rando.

## Rules/Placement

### Final Door Requirement

**Requirement** - Conditions required to unlock the final door at the Altar of Naught (the door leading to Final
Xemnas).

* Three Proofs - Obtain the three Proofs (Connection, Nonexistence, and Peace).
* Objectives - Complete a set of objectives from a given list.
* Emblems - Collect a certain number of Emblems that have been randomly placed.

**Objectives Required** - When using Objectives, the number of objectives that must be completed.

**Objectives Available** - When using Objectives, the number of objectives that will be placed in the game.

**Objective Pool** - When using Objectives, configures the type of objectives that are available.

* All Objectives - All available world progress checkpoints, Drive Form levels, and bosses.
* Bosses Only - Only allows bosses to be in the pool (both story and superbosses).
* Last Story Check - Only allows the checkpoints for the end of the story for each world.
* Everything but Bosses - All world progress checkpoints and Drive Form levels.
* Spike Hit List - Popularized by Spikevegeta, this pool of objectives contains all superbosses, a level 7 Drive Form,
  and Starry Hill. For the superbosses, those that have Absent Silhouettes places the objective there.

**Emblems Required** - When using Emblems, the number of Emblems that must be collected.

**Emblems Available** - When using Emblems, the number of Emblems that will be placed in the game.

### Where Items Can Go

**Accessibility** - How accessible locations need to be for the seed to be "completable".

* 100% Locations - All locations must be reachable, and nothing will be permanently locked.
* Beatable - The Final Door Requirement must be reachable, but nothing else is guaranteed. For Three Proofs, this means
  all three Proof items must be obtainable. For Objectives, this means at least the required number of objectives must
  be completable (some objectives may not be). For Emblems, this means at least the required number of Emblems must be
  obtainable (some Emblems may not be).

**Softlock Prevention** - An option to change the softlock prevention method in use. Default option is `Regular Rando`
which is correct for most cases, but if you play reverse rando or are doing a co-op with someone playing reverse rando,
you can select other softlock preventions options for those cases.

**Extended Item Placement Logic** - If enabled, auto forms (Auto Valor, Auto Wisdom, etc.) may be required to make
progress in your seed.

### Guaranteed Restrictions

> For the Depth settings, the choices are:
> - **Anywhere** - No restriction
> - **Non-Superboss** - Cannot be on a superboss; all other locations are possible
> - **First Visit** - Force into a first visit (only for the 13 main hub worlds with portals)
> - **First Visit Boss** - Force onto the first visit boss of a world (only for the 13 main hub worlds with portals)
> - **Second Visit** - Force into a second visit (only for the 13 main hub worlds with portals)
> - **Last Story Boss** - Force onto the last boss or story content of a world (only for the 13 main hub worlds with
>   portals)
> - **Superbosses** - Force onto superbosses only (Data Organization/Absent Silhouette/Sephiroth/Terra)
> - **Non First Visits** - Opposite of the first visit depth. Anywhere but the first visit of the 13 portal worlds (can
>   include Drive Forms/Levels/100 Acre Wood)

**Visit Unlock Depth** - Configures locations where the visit unlocks can be placed.

**Ansem Report Depth** - Configures locations where the Ansem Reports can be placed.

**Proof Depth** - Configures locations where the three Proof items can be placed.

**Promise Charm Depth** - Configures locations where the Promise Charm can be placed.

**Yeet The Bear Required** - If enabled, forces the Proof of Nonexistence onto the popup reward from 100 Acre Wood -
Starry Hill, thus requiring The Hunny Pot minigame to be completed in order to obtain the Proof.

### Item Placement Biases

Enables a bias for the placement of various item types based on how overall difficult/easy you'd like accessing those
items to be.

> **Very Early (Scaled)** - Equivalent to Earlier (Scaled) with more bias to the early locations.
> 
> **Earlier (Scaled)** - Items in the category are more likely to be placed in the earliest locations, with the
> likelihood decreasing as locations get later.
> 
> **Early (Twice as Likely)** - Items in the category are twice as likely to be placed in the first half of locations.
> 
> **None (Normal)** - Items in the category are equally likely to be placed anywhere.
> 
> **Late (Twice as Likely)** - Items in the category are twice as likely to be placed in the second half of locations.
> 
> **Later (Scaled)** - Items in the category are less likely to be placed in the earliest locations, with the
> likelihood increasing as locations get later.
> 
> **Very Late (Scaled)** - Equivalent to Later (Scaled) with more bias to the late locations.
> 
> **Extremely Late (Scaled)** - Equivalent to Very Late (Scaled) with even more bias to the late locations.
> 
> **Latest (Scaled)** - Items are _drastically_ biased towards the latest locations.

### Chain Logic

**Chain Logic Enabled** - If enabled, places items that can block progress in a chain with one another, making the seed
very linear.

**Maximum Logic Length** - How many steps in the logic chain you'd like to do at minimum.

**Maximum Logic Length** - How many steps in the logic chain you'd like to do at most.

## Hints

**Hint System** - Controls which hint system to use, as well as options for hints.

> See the main [Hints](../hints/index.md) page for explanations of the different hint systems and their options.

## Item Pool

### Include in Item Pool

**Bonus Rewards as Items** - If enabled, takes HP, MP, Drive, Accessory Slot, Armor Slot, and Item Slot upgrades from
the normal bonus popup locations and lets them appear in chests or other randomized locations. Those bonus popup
locations will instead contain other randomized rewards.

**50 AP Boosts** - Adds 50 guaranteed AP Boosts into the item pool.

**Promise Charm** - If enabled, the Promise Charm item will be added to the randomized item pool, which can allow
skipping The World That Never Was by interacting with the computer in the Garden of Assemblage once you have obtained
the Promise Charm and satisfied the Final Door Requirement.

**Antiform** - If enabled, adds Antiform as an obtainable form.

**Maps** - If enabled, adds maps to the item pool.

**Synthesis Recipes** - If enabled, adds synthesis recipes to the item pool.

* Note that recipes are not required, even when synthesis rewards are randomized, so enabling this setting only affects
  how much of the item pool is available for other items.

**Accessories** - If enabled, all accessories are included in the item pool.

**Armor** - If enabled, all armor items are included in the item pool.

**Munny Pouches** - If enabled, all Munny Pouches are included in the item pool.

**Ability Pool** - Controls the inclusion and quantity of abilities in the randomized pool.

* Default Abilities - Includes the default set of action and support abilities, with their default quantities.
* Randomize Ability Pool - Picks Sora's obtainable action and support abilities at random (guaranteed to have 1
  Second Chance and 1 Once More). Some other abilities may not be included at all, and some support abilities may have
  several copies.
* Randomize Support Ability Pool - Includes the default set of action abilities, but will pick support abilities
  at random (still guaranteed to have 1 Second Chance and 1 Once More). Some other support abilities may not be
  included at all, and others may have several copies.
* Randomize Stackable Abilities - Guarantees 1 copy of each ability that works on its own, but randomizes how many
  copies of the stackable support abilities you can get (guaranteeing at least 1 copy of each).

### Randomized Shop

**Add Visit Unlocks To Shop** - Adds a number of visit unlocks into the Moogle shop.

**Add Ansem Reports To Shop** - Adds a number of Ansem Reports into the Moogle shop.

### Guaranteed Shop Items

**Keyblades** - Adds duplicates of each keyblade into the Moogle shop.

**Elixirs** - Adds Elixir and Megalixir into the Moogle shop.

**Drive Recoveries** - Adds Drive Recovery and High Drive Recovery into the Moogle shop.

**Stat Boosts** - Adds Power Boost, Magic Boost, Defense Boost, and AP Boost into the Moogle shop.

### Junk Items

Once all the required items are placed, items from this list are used to fill any remaining locations. This list is also
used as the items to place in worlds/locations that are configured to contain only junk.

## Starting Inventory

### Starting Inventory

**Growth Abilities** - Select how many growth (movement) abilities you want to start with.

* None
* 3 Random - Pick 3 individual growth abilities to add at the start (e.g. you could start with High Jump LV1 and Dodge
  Roll LV2).
* 5 Random - Pick 5 individual growth abilities to add at the start.
* 7 Random - Pick 7 individual growth abilities to add at the start.
* 9 Random - Pick 9 individual growth abilities to add at the start.
* Level 1 - All growths start at level 1.
* Level 2 - All growths start at level 2.
* Level 3 - All growths start at level 3.
* Max - All growths start at the maximum level.

(Magics) - Begin the game with this many of each Magic already acquired.

**Torn Pages** - Begin the game with this many Torn Pages already acquired.

**Ansem Reports** - Begin the game with this many Ansem Reports already acquired (will randomly choose among
the reports).

### (Other Groups)

Begin the game with each selected item already acquired.

**Starting Abilities Equipped** - If enabled, all starting abilities will be automatically equipped (except those coming
from critical bonuses).

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

### Other Modifiers

**Split AS/Data Rewards** - Controls how rewards are given for Absent Silhouette fights.

* If enabled, Absent Silhouette rewards will _NOT_ give the reward from their Data versions. You must beat the Data
  version to get the Data-specific reward.
* If disabled, beating the Absent Silhouette gives rewards from the Data version as well as the Absent Silhouette
  version.

**Cups Give Experience** - If enabled, experience for party members and Drive Forms can be earned while in an Olympus
Coliseum cup.

**Retry Data Final Xemnas** - If enabled, if you die to Data Final Xemnas, Continue will spawn you right back into the
fight, instead of having to fight Data Xemnas I again.

> **Warning** - if you are unable to beat Data Final Xemnas, there is no way to exit, essentially causing a softlock,
> and you'll have to load a save.

**Retry Dark Thorn** - If enabled, if you die to Dark Thorn (Beast's Castle first visit boss), Continue will spawn you
right back into the fight, instead of having to fight Shadow Stalker again. Especially useful when bosses are
randomized.

> **Warning** - if you are unable to beat Dark Thorn, there is no way to exit, essentially causing a softlock, and
> you'll have to load a save.

**Remove Damage Cap** - Removes the damage cap for every enemy/boss in the game.

**Chest Visuals Match Contents** - If enabled, treasure chests will visually indicate the type of item they contain.
See [Chest Visuals](../seed-generator/chests/index.md) for more details.

**Randomize World Party Members (Beta)** - Randomizes the world-specific party member in each world (e.g. Tron may
appear in Olympus Coliseum rather than Auron).

**Revenge Limit Maximum (Beta)** - Randomizes the revenge value limit of each enemy/boss in the game. Vanilla
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

**Keyblades Unlock Chests** - When enabled, Sora must have certain keyblades to open chests in the different worlds.
It's not required to equip the keyblade - being in the inventory is enough. If the keyblade is not acquired, the
reaction command to open chests in the associated world will be disabled.

> **Note** - this setting requires the `KH2FM-Mods-equations19/KH2-Lua-Library` mod, and will not work properly
> without it installed and enabled.

    Simulated Twilight Town | Bond of Flame
    Twilight Town           | Oathkeeper
    Hollow Bastion          | Sleeping Lion
    Cavern of Remembrance   | Winner's Proof
    Land of Dragons         | Hidden Dragon
    Beast's Castle          | Rumbling Rose
    Olympus Coliseum        | Hero's Crest
    Disney Castle           | Monochrome
    Port Royal              | Follow The Wind
    Agrabah                 | Wishing Lamp
    Halloween Town          | Decisive Pumpkin
    Pride Lands             | Circle of Life
    Space Paranoids         | Photon Debugger
    World that Never Was    | Two Become One
    Hundred Acre Wood       | Sweet Memories

**Restrict Final Form** - Restrictions on how Final Form works.

* None - No changes are done to how Final Form works in the randomizer.
* No Random Chance - Turns off random anti-form, which means it's not possible to force Final Form without the Light &
  Darkness ability
* No Final Form - Disables going into Final Form in any way. Final Form can still be obtained to raise the maximum level
  for all other Drive Forms, but no checks will be found on Final Form's levels.

### Battle Levels

**Battle Level Choice** - Configures how the world battle levels are chosen.

* Normal - Battle levels are unchanged.
* Shuffle - Shuffles the normal battle levels among all visits of all worlds.
* Offset - Increases or decreases all battle levels by a chosen amount.
* Within Range of Normal - Chooses a random battle level for each world visit within a chosen range above or below the
  visit's normal battle level.
* Random - Chooses a random battle level for each world visit within a configurable range.
* Scale to 50 - All last visits are set to battle level 50, with previous visits to the same world scaled
  proportionally.

## EXP/Stats

**Sora Starting AP** - Sora begins the game with this much AP.

**Double Stats Start Level** - The level at which two stat increases start to be given (when no item is given)

**Double Stats End Level** - The level at which two stat increases stop being given (when no item is given)

**Sora Strength/Magic/Defense/AP Rate** - Configures how likely each of these upgrades are given on level ups, relative
to the others.

* Example: Setting the magic rate to 20 and the other rates to 10 means a magic upgrade is twice as likely as any of the
others.

### Experience Multipliers

Adjusts the amount of experience needed to reach each level. Sora's level, Drive Form levels, and Summon levels are all
configurable.

* Example: If the game normally requires 1000 experience to reach level 2, setting the multiplier to 2.0 changes the
game to require only 500 experience to reach level 2.

### Experience Curves

Allows for further customization of experience rates, inspired by a similar concept in Kingdom Hearts I.

* Dawn (Normal) - The default EXP rate.
* Midday - Early levels (up to 50 for Sora, levels 2-4 for Drive Forms and Summons) require more experience, but later
  levels require less.
* Dusk - Early levels (up to 50 for Sora, levels 2-4 for Drive Forms and Summons) require even more experience, but
  later levels require even less.

## Keyblades

### Keyblade Statistics

**Keyblade Min/Max Stat** - Controls the minimum and maximum strength and magic stat that each keyblade can have.

### Support/Action Keyblade-Eligible Abilities

Controls the abilities that are eligible to be randomized onto keyblades. Any abilities not selected are guaranteed to
not be attached to a keyblade.

> Note that there must be enough keyblade-eligible abilities chosen such that each keyblade gets an ability, or the seed
> will fail to generate.

## Companions

### AP

**Donald Starting AP** - Donald begins the game with this much AP.

**Goofy Starting AP** - Goofy begins the game with this much AP.

**Companions Deal Damage to All Enemies and Bosses** - If enabled, companions will deal damage to all enemies and bosses
instead of just one damage.

**Companions Can Kill Bosses** - If enabled, companion attacks will be able to kill bosses.

(Companion Attack Damage Mode Options) - Defines the type of knockback each attack will have. Keep in mind, changes will
also affect enemies that Companions could already affect normally.
        
* Just Damage: Enemies won't be phased (except for certain things like Goofy Tornado which have a second attack effect
  for pulling enemies in).

* Damage + Stun: Enemies will be stunned, but won't move very much or at all from their position.

* Damage + Stun + Knockback: Like above, but will also be moved.

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

**Allow more annoying replacements** - If enabled, allows bosses to be placed in more locations that may be exceedingly
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

**Command Menu** - controls the appearance of the command menu on-screen.

* Vanilla - Command menus will have their normal appearance.
* Randomize (one) - Chooses a single random command menu to use for the entire game. Favors custom command menus over
  in-game ones.
* Randomize (in-game only) - Chooses a random command menu for each world from existing in-game command menus.
* Randomize (custom only) - Chooses a random command menu for each world from the `command-menus` folder contained
  within your configured Custom Visuals Folder.
* Randomize (in-game + custom) - Chooses a random command menu for each world from both existing in-game command menus
  and the `command-menus` folder contained within your configured Custom Visuals Folder.
* (individual command menus) - Forces all command menus to have the chosen appearance.

> Using custom command menus requires a Custom Visuals Folder to have been configured using the Configure menu -> Choose
> Custom Visuals Folder. Place any custom command menus into individual folders within the `command-menus` folder within
> your chosen custom visuals folder.
> 
> Each custom command menu folder must include a .2dd file for the base asset, and a .png or .dds file for the
> remastered asset (if using the PC game version).

### Visuals (PC Panacea Only)

_These options will only work properly when using [Panacea](../glossary/index.md#panacea) for loading mods. Things will
likely look incorrect if using any of these options when patching the game._

**Add Randomizer-Themed Textures** - If enabled, adds a few KH2 Randomizer-themed textures to the game.

**Item Pictures** - controls the appearance of item pictures.

* Vanilla - Item pictures will have their normal appearance.
* Randomize (in-game only) - Chooses a random picture for each item from existing in-game pictures.
* Randomize (custom only) - Chooses a random picture for each item from the `item-pictures` folder contained within your
  configured Custom Visuals Folder.
* Randomize (in-game + custom) - Chooses a random picture for each item from both existing in-game pictures and the
  `item-pictures` folder contained within your configured Custom Visuals Folder.

If you'd like control over categories for item pictures, you can create your own additional category folders, and
you can edit the `item-pictures.json` file (located in the folder where you installed the seed generator) to configure
the category/categories of each item. Items can be given multiple categories, and a replacement picture will be chosen
from one of those categories. A category can be repeated in the configuration to give a certain category more "weight".

Using this technique, you can get as precise as having limited a set of custom item pictures for each category, or a
specific custom picture for each supported item in the game.

> Using custom item pictures requires a Custom Visuals Folder to have been configured using the Configure menu -> Choose
> Custom Visuals Folder. Place any custom images into appropriate category folders within the `item-pictures` folder
> within your chosen custom visuals folder. Custom images can be in .dds or .png format.

**Room Transitions** - controls the appearance of the room transition images.

* Vanilla - Room transitions will have their normal appearance.
* Randomize (in-game only) - Chooses a random transition for each world from existing in-game room transition images.
* Randomize (custom only) - Chooses a random transition for each world from the `room-transition-images` folder
  contained within your configured Custom Visuals Folder.
* Randomize (in-game + custom) - Chooses a random transition for each world from both existing in-game transition images
  and the `room-transition-images` folder contained within your configured Custom Visuals Folder.

> Using custom room transition images requires a Custom Visuals Folder to have been configured using the Configure menu
> -> Choose Custom Visuals Folder. Place any custom images into a `room-transition-images` folder within your chosen
> custom visuals folder. Custom images must be in .png format.

**Ending Screen** - controls the appearance of the ending ("The End") screen picture.

* Vanilla - Ending screen will have its normal appearance.
* Randomize (in-game only) - Chooses a random ending screen from existing in-game options.
* Randomize (custom only) - Chooses a random ending screen from the `ending-pictures` folder contained within your
  configured Custom Visuals Folder.
* Randomize (in-game + custom) - Chooses a random ending screen from both existing in-game options and the
  `ending-pictures` folder contained within your configured Custom Visuals Folder.

> Using custom ending screen images requires a Custom Visuals Folder to have been configured using the Configure menu
> -> Choose Custom Visuals Folder. Place any custom images into an `ending-pictures` folder within your chosen
> custom visuals folder. Custom images must be in .png format.

**Recolor Some Textures** - If enabled, allows for basic recoloring of some of the in-game textures. See
[Texture Colors](../seed-generator/textures/index.md) for more details.

> Recoloring textures requires the OpenKH folder to be set up in the Configure menu, and for KH2 to have been extracted
> using the OpenKH Mods Manager setup wizard.

### Keyblades

See the main [Randomized Keyblades](../keyblades/index.md) page for instructions.

### Music

See the main [Randomized Music](../music/index.md) page for instructions.

### External Randomization Executables

Allows external randomization files to be executed every time a seed is generated. This can be used to integrate with
external mods that have their own `Randomize.exe` file (or similar) that must be run in order to randomize their
contents.

### Cosmetics-Only Mod

Generates a mod for OpenKH Mods Manager that _only_ randomizes cosmetics. Can be useful if using a randomizer
seed generated outside the standard seed generator (using [Archipelago](https://archipelago.gg/) or otherwise).
