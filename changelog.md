## 2.0 Zip Seed Generator Changelog
 
- "Max Item Placement Logic" is the only logic in this generator. The arbitrary restrictions in place before didn't prevent all softlocks and caused an undue maintenance burden in the code.  
- Revamped Item Placement Difficulty System: more even distribution of useful checks across worlds, incremental increase in weight based on how far you get into worlds, items have a rarity which influences the weights as well. Works for reverse rando now as well
- Statsanity Mode: Randomizes the HP, MP, Drive, Accessory, Armor, and Item Ups from bonuses into the item pool, which frees up those bonus slots for other items. (HP, MP, and Drive Ups can't be in STT or popups)
- You can choose what abilities are allowed to be on keyblades. Too few abilities eligible for keyblades will result in no seed being generated.
- Proof Depth Option: You can choose where the proofs will be found (similar to report depth), where you can force proofs to be in first visits, on first visit bosses, in first or second visit (no datas), second bosses (bosses before datas), on data fights, or anywhere (default).
- Struggle Weapons from STT will now have the Draw ability guaranteed, and will have the average keyblade stats for the settings (e.g. if min stat is 5 and max stat is 13, the stats of all struggle weapons will be 9/9)
- Spoiler log contains more information about the seed (settings, exp values, party weapons, boss/enemy swaps, etc.)
- New Midday and Dusk Exp gain options, which make earlier levels harder to obtain, but makes later ones easier to obtain.
- Yeet the Bear Option: Forces the Proof of Nonexistence onto the Starry Hill popup of 100 Acre Wood
- Customizable Point Hint values
- Randomized Settings Option (Rando Rando) - Experimental option to pick random settings for a seed. Will randomize exp values, keyblade stats, hint system, point values for point hints (if picked as the hint system), item placement level (up to very hard), and worlds/bosses/misc locations (only if you left them on before generating a random settings seed, if you left an option off, it will stay off).
- Randomized Music (Improved): Now supports custom music, please see [here](https://github.com/tommadness/KH2Randomizer/blob/2.0/helpinfo/music.md) for an explanation.
- More Daily Seed settings: Full list can be found [here](https://github.com/tommadness/KH2Randomizer/blob/2.0/helpinfo/dailyseeds.md). The default settings now only have enemies randomized, as boss randomization has too many edge cases to always be on in Daily Seeds.
- Boss/Enemy related features/improvements: See the full list [here](https://github.com/thundrio-kh/khbr/blob/master/CHANGELOG)

## 2021-24-Sep update
- Added option to randomize puzzle rewards
- Added Nightmare Item Placement Difficulty
  - Auto forms will be in logic on Nightmare
  - Forcing final will be in logic on Nightmare
  - Keyblades with good abilities are weighted checks on Nightmare
  - Puzzles rewards are guaranteed enabled on Nightmare
- Adjusting some locations as early or late for item difficulty purposes
  - Added some Twilight Town Mansion location as late instead of neutral
  - Made Atlantica tutorial an early location

## 2021-08-Sep update
- Added settings for JSmartee Report depth.
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
- JSmartee Reports can no longer hint the world they were found in.
- Fixed a bug relating to an extra bonus reward, resulting in a blank Donald reward.


## 2021-29-Aug update
- PC Support is here through the build_from_mm bridge program. See [here](https://github.com/tommadness/KH2Randomizer/blob/master/helpinfo/pc.md) for instructions.
- Random Music (PC Only)! Can include music from KH2, BBS, and Recom (if including BBS/Recom music those games need to be extracted, as noted [here](https://github.com/tommadness/KH2Randomizer/blob/master/helpinfo/pc.md))
- Daily seeds! Once a day seeds with different settings each day. see [here](https://github.com/tommadness/KH2Randomizer/blob/master/helpinfo/dailyseeds.md) for details.
- Logic validator to guarantee every location can be reached. There is also now a new seed modifier (on by default) which allows any item to be in any location, see [here](https://pastebin.com/mNhYP9DV) for details.
- Seed difficulty setting, to change how likely an important item is to be found early or late. From "super easy" to "insane". See [here](https://pastebin.com/mNhYP9DV) for details.
- Seed modifier to start Sora/Donald/Goofy with 0 AP.
- Fixed a bug causing the non-critical difficulty modes to start without starting inventory or the proper amount of AP.
- Fixed a bug preventing the "Remove Damage Cap" seed modifier from being used without also enabling random bosses/enemies.
