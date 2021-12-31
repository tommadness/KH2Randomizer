# General FAQ
## What version of Kingdom Hearts II can this be used with?
This seed generator can be used with either the PC (Epic Games Store) or PCSX2 (emulated) version of Kingdom Hearts II: Final Mix. This will not work with Kingdom Hearts II (US PS2), and is not supported on the console versions of the game.

## What are the differences between this and [Valaxor's Seed Generator](https://randomizer.valaxor.com/#/seed)?
This seed generator is designed to be used with the [OpenKH](https://openkh.dev/) Mods Manager [(Download the latest release here)](https://github.com/Xeeynamo/OpenKh/releases). This enables some extra features:
- Cosmetic randomization
  - Currently this takes the form of Command Menu aesthetic randomization on PCSX2, and music randomization on PC
- Boss/Enemy Randomizer improvements
  - Field enemies are now randomized
  - Certain bosses that were not reasonable to randomize can now be randomized
  - Boss/Enemy randomization on PC
- Starting inventory
- Puzzle Reward Randomization Option

Other differences include:
- No "Vanilla" option for any randomization setting
- More item placement logic options
- Additional seed modifiers
- All armor and accessories exist in the item pool
- Once all items are placed, all remaining slots are filled with random Synthesis Materials or Consumable items

## Why are Consumables considered "junk"?
"Junk" is a bit of a misnomer. After all "one-off" items (equipment, abilities, Important Checks, maps) are placed, all remaining locations are filled randomly with Synthesis Materials or Consumables, as the quantity of those per seed don't necessarily matter.

# OpenKH Mods Manager
## What priority should the seed be placed at in OpenKH Mods Manager?
The seed should always be placed at the highest priority. The seed needs to overwrite some defaults set by the All In One mod.

# Hint Systems
## What are the hint systems?
The KH2R community has come up with three different hint systems:
- **JSmartee** - Inspired by [JSmartee](https://jsmartee.github.io/kh2fm-hints-demo/)'s implementation of hints. When you find an Ansem Report in-game, you are told how many [Important Checks](https://jsmartee.github.io/kh2fm-hints-demo/info.html#checks) exist in a world.
- **Shananas** - Inspired by Shananas' implementation of hints. While playing, you are informed once you have found all Important Checks in a world.
- **Points** - An inspired mix of Shananas', and JSmartee's implementation of hints. Each [Important Check](https://jsmartee.github.io/kh2fm-hints-demo/info.html#checks) is worth a set amount of points. You are able to see each world's Score right from the start and when you find an Ansem Report in-game, you are told about a single Important Check in a world.

## How do I use hints?
Your seed zip file can be loaded into the following trackers:
- RedBuddha's [KH2Tracker](https://github.com/TrevorLuckey/KH2Tracker). [(Download `KhTracker.exe` here)](https://github.com/TrevorLuckey/KH2Tracker/releases)
- DA's visual customization-focused fork of [KH2Tracker](https://github.com/o0DemonBoy0o/KH2Tracker). [(Download `KhTracker.exe` here)](https://github.com/o0DemonBoy0o/KH2Tracker/releases)

## `(JSmartee Hints)` What are Hinted Hints? Why do they matter?
Taken from https://jsmartee.github.io/kh2fm-hints-demo/info.html#logic:

Reports pointing to proofs will be hinted.
- Ex: There's a proof in Port Royal. Report 4 points to Port Royal. Report 4 is in Halloween Town. Halloween Town must be hinted by another report.
If the priority items above (proofs, forms, pages, and magic) are already taking up all 13 hints, they will be prioritized over these reports.
Note: If the reports are on drive forms or in 100 Acre Wood, there is no logic to hint forms or pages as of now.

This is represented in RedBuddha's KH2Tracker by the world's check count turning blue.

## `(Points Hints)` What are Points? What is a world Score?
Each Important Check is in category and each category is given a value for each item in it.
The default values for each category are as follows:
- Proofs and Promise Charm = 12 points
- Drive Forms = 10 points
- Each Magic Elemet = 8 points
- Summon Charms = 6 points
- Second Chance and Once More = 4 points
- Torn Pages and Ansem Reports = 2 points

Each world is given a Score based on how many of each of these it contains. You are able to see the Score for each world right from the start.
- Ex. If Twilight Town has a Score of 12 that may mean is has a Proof, A Drive Form and a Torm Page, or any other combonation of items that add up to 12.

Reports when gotten will hint a single Important Check a world contains.
- If Proof-hinting reports is turned on then reports also have a chance of directly telling you which world a proof is in. 
Note: Even with this setting on, Reports are not guaranteed to hint all or any Proofs.

When all the Important Checks for a world are correctly placed, then that world's score will turn into a blue 0.

## `(JSmartee / Points Hints)` What do the various hint modes mean?
The different modes determine where a report can be found:

  - **JSmartee / Points** - Reports can be found anywhere.
  - **FirstVisit** - All reports can be found in the first visit to a world.
    - First visits are considered:
      * The first visit to any Disney world in the Vanilla game
      * Up to and including Sora Level 30
      * Up to and including level 3 on any Drive Forms
      * Up to and including Piglet's Howse
      * Up to and including Xigbar in The World That Never Was
      * The entirety of Simulated Twilight Town
  - **SecondVisit** - All reports can be found in the first or second visit to the world. (They can not be found on Data/Absent Silhouette fights)
  - **FirstBoss** - All reports are guaranteed on the boss at the end of the first visit of a world (excluding 100 Acre Wood and Atlantica).
  - **SecondBoss** - All reports are guaranteed on the end of the second visit to a world (excluding 100 Acre Wood and Atlantica).

# Seed Modifiers

## What do the Seed Modifiers do?
- **Max Logic Item Placement** - Explained in its own section below
- **Reverse Rando** - Alters item placement logic to work with `Reverse Garden of Assemblage`.
- **Glass Cannon** - All defense stat ups are removed from Sora's Levels
- **Library of Assemblage** - Sora starts with all 13 Ansem Reports (used as hints in the JSmartee and Points Hint System)
- **Schmovement** - Sora starts with level 1 of all movement abilities
- **Better Junk** - All synthesis items in the filler item pool are replaced with consumables
- **Randomize Ability Pool** - Explained in its own section below
- **Start with No AP** - Sora, Donald, and Goofy start with 0 AP
- **Remove Damage Cap** - Bosses and enemies no longer have a maximum damage that can be applied in one hit.
- **Cups Give XP** - Enemies fought while in a OC Cup will give out XP and Form XP.

## What does Max Logic Item Placement do?
**Max Logic Item Placement** is a seed modifier that makes all items obtainable, removing most "hard" restrictions on locations.

Guarantees:
- At least 1 `Fire Element`, 1 `Blizzard Element`, and 1 `Thunder Element` before Agrabah 2
- At least 3 `High Jump`s, `Quick Run`s, `Aerial Dodge`s, and `Glide`s before Cavern of Remembrance

Common "Unusual" Occurances from standard item placement logic:
- `Torn Pages` on Form Levels
- Form on Forms
- `Torn Pages` in 100 Acre Wood after Pooh's Howse
- `Blizzard Element` in Agrabah 2
- `Torn Pages` or a form on Mushroom 13

## What does Randomize Ability Pool do?
By default, the ability pool is set. There are always 3 `Finishing Plus` abilities, 2 `Scan`s, 1 `Light & Darkness`, et cetera.

**Randomize Ability Pool** makes it so the only guarantee is exactly 1 `Second Chance` and 1 `Once More` in the ability pool. This can result in, for example, 2 `Finishing Plus`es, 0 `Scan`s, 3 `Light & Darkness`es, et cetera.

The exact possibilities are:
- 0 or 1 of each `Action Ability`
- Exactly 4 of each `Growth Ability`
- Exactly 1 `Second Chance`
- Exactly 1 `Once More`
- 0 or more of each `Support Ability`

# Item Placement Difficulty

## What does Seed Item Placement Difficulty mean?
**Seed Item Placement Difficulty** weights "favorable" checks earlier or later in a world, depending on the setting. Details on location weights can be found [here](https://github.com/tommadness/KH2Randomizer/blob/master/helpinfo/itemweights.md) 

Items that are weighted include:
 
- Proofs
- Magic
- Forms
- Summons
- Torn Pages
- Second Chance/Once More
- Promise Charm
- Munny Pouches
 
Abilities that are weighted (when off keyblades) include:
 
- Combo Master
- Finishing Plus
- Negative Combo
- Experience Boost
- Light & Darkness
- Aerial Spiral
- Horizontal Slash
- Slide Dash
- Flash Step
- Guard Break
- Explosion
- Aerial Dive
- Magnet Burst
- Trinity Limit

## What is the "Nightmare" Item Placement Difficulty?

Nightmare difficulty is an extra difficult item placement setting that expands the pool of items that are pushed late in a seed, as well as changing the weighting for locked areas that you can get checks from (e.g. forms and 100 acre). The expanded pool of items is:

- Combo Boost
- Air Combo Boost
- Berserk Charge
- Form Boost
- Draw
- Drive Converter
- Auto Forms

If there are "good" abilities on keyblades, those keyblades are pushed late as well. Auto forms are also "in-logic" so you may need to use an auto form to unlock the form fully (e.g. Valor form can be on Valor 3, so you need to use auto-valor to get it).

Additionally, **puzzle rewards are guaranteed randomized in this setting, and likely to have important checks**, and those checks, while they are unhinted, may still be required to unlock other checks you need to finish the seed.
