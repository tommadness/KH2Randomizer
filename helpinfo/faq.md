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
The KH2R community has come up with two different hint systems:
- **JSmartee** - Inspired by [JSmartee](https://jsmartee.github.io/kh2fm-hints-demo/)'s implementation of hints. When you find an Ansem Report in-game, you are told how many [Important Checks](https://jsmartee.github.io/kh2fm-hints-demo/info.html#checks) exist in a world.
- **Shananas** - Inspired by Shananas' implementation of hints. While playing, you are informed once you have found all Important Checks in a world.

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

## `(JSmartee Hints)` What do the various JSmartee hint modes mean?
The different modes determine where a report can be found:

  - **JSmartee** - Reports can be found anywhere.
  - **JSmartee-FirstVisit** - All reports can be found in the first visit to a world.
    - First visits are considered:
      * The first visit to any Disney world in the Vanilla game
      * Up to and including Sora Level 30
      * Up to and including level 3 on any Drive Forms
      * Up to and including Piglet's Howse
      * Up to and including Xigbar in The World That Never Was
      * The entirety of Simulated Twilight Town
  - **JSmartee-SecondVisit** - All reports can be found in the first or second visit to the world. (They can not be found on Data/Absent Silhouette fights)
  - **JSmartee-FirstBoss** - All reports are guaranteed on the boss at the end of the first visit of a world (excluding 100 Acre Wood and Atlantica).
  - **JSmartee-SecondBoss** - All reports are guaranteed on the end of the second visit to a world (excluding 100 Acre Wood and Atlantica).

# Seed Modifiers

## What do the Seed Modifiers do?
- **Max Logic Item Placement** - Explained in its own section below
- **Reverse Rando** - Alters item placement logic to work with `Reverse Garden of Assemblage`.
- **Glass Cannon** - All defense stat ups are removed from Sora's Levels
- **Library of Assemblage** - Sora starts with all 13 Ansem Reports (used as hints in the JSmartee Hint System)
- **Schmovement** - Sora starts with level 1 of all movement abilities
- **Better Junk** - All synthesis items in the filler item pool are replaced with consumables
- **Randomize Ability Pool** - Explained in its own section below
- **Start with No AP** - Sora, Donald, and Goofy start with 0 AP
- **Remove Damage Cap** - Bosses and enemies no longer have a maximum damage that can be applied in one hit.

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
**Seed Item Placement Difficulty** weights "favorable" checks earlier or later in a world, depending on the setting.

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
- Horizontal Slash
- Slide Dash
- Flash Step
- Guard Break
- Explosion
- Aerial Dive
- Magnet Burst
- Trinity Limit
