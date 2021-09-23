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
