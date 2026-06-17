# Randomized Keyblades

The KH2 Randomizer supports randomizing keyblades from your extracted copy of KH2, as well as other external keyblades.

* [General Options](#general-options)
* [In-Game Keyblades](#in-game-keyblades)
* [External Keyblades](#external-keyblades)

## General Options

### Keyblades

Controls the appearance of keyblades.

* Vanilla - Keyblades will have their normal appearance.
* Randomize (in-game only) - Randomizes keyblades among in-game options. See [In-Game Keyblades](#in-game-keyblades) below for more
  instructions.
* Randomize (custom only) - Randomizes keyblades using only custom options. See [External Keyblades](#external-keyblades) below for more
  instructions.
* Randomize (in-game + custom) - Randomizes keyblades using in-game and custom options.

> The settings icon next to the Keyblades drop down opens the Manage Keyblades window, which can be used to preview the
> available keyblades and import additional custom keyblades. See below for more information.

### Allow Duplicate Replacements

Check this option if you don't have enough keyblades available to replace all the game ones, but you'd like only
keyblades from your keyblade pool to be used (even if it means some keyblades will be re-used).

With this option disabled, once the randomizer runs out of replacement keyblades, it will not replace any further
keyblades from the game, and some keyblades will remain unchanged.

Checking this option could be used, for example, to replace all in-game keyblades with a single replacement.

### Replace Keyblade Effects

If enabled, replaces keyblade effects (such as swing trails and sound effects) in addition to textures. If disabled,
only replaces the keyblade textures.

Not all external keyblades include effects, and some effects have visual and/or audio quirks, so this option exists as a
way to avoid any potential problems that may come along with replacing effects.

### Replace GoA Keyblades

If enabled, attempts to also replace keyblades from the Garden of Assemblage mod (Kingdom Key D, Alpha Weapon,
Omega Weapon, Pureblood, and the Struggle Weapons).

This has been tested with a sampling of in-game and custom keyblades, but is marked beta at this time for further
testing. It is recommended to test multiple seeds with this option enabled before attempting to do so in a race.

## In-Game Keyblades

If you haven't yet configured the seed generator to point to your OpenKH folder, choose `Find OpenKH Folder` in the
`Configure` menu.

Then, to prepare in-game keyblades to be randomized, choose the `Extract Vanilla Keyblades` process, found on the Manage
Keyblades window (which is accessed via the settings icon next to the Keyblades drop down).

## External Keyblades

You can import and use external keyblades as part of the keyblade randomizer.

### Setup

If you haven't yet configured a folder for custom visuals, choose the `Choose Custom Visuals Folder` from the seed
generator's `Configure` menu and select a folder where your imported keyblade files will be placed.

### Importing Keyblades

These options exist in the menus of the Manage Keyblades window (which is accessed via the settings icon next to the
main Keyblades drop down).

* Add Keyblade(s) from .kh2randokb Files - Can add one or more keyblades in the [.kh2randokb](kh2randokb.md) file format to the
  custom keyblade pool. When finished, the seed generator will inform you how many keyblades were imported.
* Add Keyblade(s) from OpenKH Mod - Attempts to find any keyblades within a well-structured OpenKH mod and import them
  into the custom keyblade pool without any work from the mod author. Some mods have keyblades that lack certain assets
  needed for this to function correctly, so be sure to test multiple seeds with any keyblades added this way before
  using them in a race.
* Download KH1 Keyblade Pack - Downloads Zurphing's [KH1 keyblade pack](https://github.com/Zurphing/KH1_Keyblades) and
  makes its keyblades available in the custom keyblade pool.
* Download BBS Keyblade Pack - Downloads Kite2810's
  [BBS keyblade pack](https://github.com/Kite2810/Birth-by-Sleep-Keybladepack) and makes its keyblades available in the
  custom keyblade pool.

> Imported keyblades are placed into a `keyblades` folder within your chosen custom visuals folder.

> Obtaining other external keyblades is outside the scope of this page.

### Packaging Keyblades

Designers/modders who have created custom keyblades can package their assets into the [.kh2randokb](kh2randokb.md) file format to
allow KH2 Randomizer players to more easily import them into the pool for randomization. To begin, choose `Create
.kh2randokb File` in the `Create` menu on the Manage Keyblades window. You'll be shown a window with many fields (with
Browse buttons for most) for selecting the various assets needed to represent a keyblade. Check the tooltip for each
input field for more information.

Not all fields are required. A keyblade can be created with just a base model/texture as well as at least one remastered
texture.
