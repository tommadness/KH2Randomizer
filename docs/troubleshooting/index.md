# Troubleshooting

* [Setup Issues](#setup-issues)
* [In-Game Issues](#in-game-issues)
* [Troubleshooting GoA (PC)](#troubleshooting-goa-pc)
* [Troubleshooting GoA (PCSX2)](#troubleshooting-goa-pcsx2)

## Setup Issues

### Why won't OpenKH Mods Manager start up?

* You may be missing the .NET Desktop Runtime. See [Downloads](../downloads/index.md).
* Depending on your system setup, you may need to run the Mods Manager program with Administrator privileges

## In-Game Issues

### (PC) Why does the game crash immediately upon startup?

* You may be using an incorrect version of LuaBackend Hook. See [Troubleshooting GoA (PC)](#troubleshooting-goa-pc).
* You may be running an incorrect version of the game. Randomizer only supports an up-to-date, legitimately purchased
  copy of the game from Epic Games Store.

### (PC) Why does the game crash when interacting with the Moogle in the Garden of Assemblage?

This usually means the Garden of Assemblage Lua script did not load properly.
See [Troubleshooting GoA (PC)](#troubleshooting-goa-pc).

### (PC) Why does the game crash when interacting with the map in Port Royal?

This is a common crash known as ["map crash"](../glossary/index.md#map-crash).

### (PC) Why does the game crash after defeating The Experiment in Halloween Town?

This is a crash caused by using the finisher of the Dance Call limit to end the fight. Avoid using the finisher at the
end of the fight to avoid this crash.

### Why does my game start in Twilight Town as Roxas, rather than at the Station of Awakening as Sora?

This usually means the Garden of Assemblage mod did not load properly.
See [Troubleshooting GoA (PC)](#troubleshooting-goa-pc) or [Troubleshooting GoA (PCSX2)](#troubleshooting-goa-pcsx2).

### (PCSX2) Why is my game in Japanese?

* Make sure you're opening PCSX2 via the "Build and Run" command in OpenKH Mods Manager and not opening PCSX2 directly
* Make sure the order of your mods in OpenKH Mods Manager is correct. The correct order (top to bottom) is
    * Randomizer seed
    * All-in-One
    * Language Pack

### Why are my keyblades not randomized? Why are certain Bonus Levels always the same?

The randomizer seed may not be properly applied to the game.

#### PC

Verify that you have done all of the following steps.

* Added the randomizer seed as a mod to OpenKH Mods Manager in the highest priority slot (at the top)
* Checked the checkbox next to the randomizer seed
* Run "Build only" in OpenKH Mods Manager
* Run "patch" or "fast_patch" in the Mod Manager Bridge

#### PCSX2

Make sure the order of your mods in OpenKH Mods Manager is correct. The correct order (top to bottom) is

* Randomizer seed
* All-in-One
* Language Pack

## Troubleshooting GoA (PC)

Press the F2 key while the game is open. A window should appear giving information about loaded Lua scripts. It should
look similar (but not identical) to this screenshot:

![Lua console](lua-console.png)

If that window does not appear, it's likely one of two causes.

* The LuaBackend Hook is missing, is in the wrong location, or is an incorrect version
    * See [LuaBackend Hook Setup](../luabackend-hook-setup/index.md) for additional instructions

* Lua scripts are missing or are in the wrong location. Verify that your Lua scripts are placed in the correct folder
  for KH2 scripts (usually something like `C:\Users\johndoe\Documents\KINGDOM HEARTS HD 1.5+2.5 ReMIX\scripts\kh2`).

If the Lua scripts window _does_ appear and you're still having trouble, verify that you have only one Garden of
Assemblage Lua script. There should only be _one_ of the following scripts in your folder: `GoA Practice.lua`,
`GoA RAM.lua`, `F266B00B GoA ROM.lua`, `F266B00B GoA Reverse.lua`. It's fine to have other Lua scripts such as soft
reset, auto-save, quality of life, etc., but only one GoA script should be there at any given time.

You can also try to use the Rando Setup Checker to help verify that you have the correct setup. See
[Downloads](../downloads/index.md) for a link.

## Troubleshooting GoA (PCSX2)

* Verify that you have "Enable Cheats" checked in the PCSX2 System menu

* Verify that you have the Garden of Assemblage `.pnach` file in the correct cheats folder
    * The correct folder can be found on the "Plugin/BIOS Selector" screen from the PCSX2 Config menu

![Cheats folder](pcsx2-cheats-location.png)

* Verify that the Garden of Assemblage `.pnach` file name starts with `F266B00B` - this is how PCSX2 knows to link that
  file up with the version of KH2 used for randomizer

* Verify that you have only one Garden of Assemblage `.pnach` file. There should only be _one_ of the following files in
  your folder: `F266B00B (Garden of Assemblage Randomizer Build).pnach`,
  `F266B00B (Garden of Assemblage Practice Build).pnach`

You can also try to use the Rando Setup Checker to help verify that you have the correct setup. See
[Downloads](../downloads/index.md) for a link.
