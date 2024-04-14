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

### Replace Keyblade Effects

If enabled, replaces keyblade effects (such as swing trails and sound effects) in addition to textures. If disabled,
only replaces the keyblade textures.

Not all external keyblades include effects, and some effects have visual and/or audio quirks, so this option exists as a
way to avoid any potential problems that may come along with replacing effects.

### Allow Duplicate Replacements

Check this option if you don't have enough keyblades available to replace all the game ones, but you'd like only
keyblades from your keyblade pool to be used (even if it means some keyblades will be re-used).

With this option disabled, once the randomizer runs out of replacement keyblades, it will not replace any further
keyblades from the game, and some keyblades will remain unchanged.

Checking this option could be used, for example, to replace all in-game keyblades with a single replacement.

## In-Game Keyblades

If you haven't yet configured the seed generator to point to your OpenKH folder, choose `Find OpenKH Folder` in the
`Configure` menu.

Then, to prepare in-game keyblades to be randomized, choose the `Extract Vanilla Keyblades` process, found in the seed
generator's `Configure` menu.

## External Keyblades

You can import and use external keyblades as part of the keyblade randomizer.

> Obtaining external keyblades is outside the scope of this page.

### Setup

If you haven't yet configured a folder for custom visuals, choose the `Choose Custom Visuals Folder` from the seed
generator's `Configure` menu and select a folder where your imported keyblade files will be placed.

### Importing Keyblades

Choose `Import External Keyblade(s)` in the seed generator's `Configure` menu to add one or more external keyblades to
the pool for randomization. Files need to be in the [.kh2randokb](kh2randokb.md) file format. When finished, the seed generator
will inform you how many keyblades were imported.

> Imported keyblades are placed into a `keyblades` folder within your chosen custom visuals folder.

### Packaging Keyblades

Designers/modders who have created custom keyblades can package their assets into the [.kh2randokb](kh2randokb.md) file format to
allow KH2 Randomizer players to easily import them into the pool for randomization. To begin, choose `Package External
Keyblade` in the seed generator's `Configure` menu. You'll be shown a window with many fields (with Browse buttons for
most) for selecting the various assets needed to represent a keyblade. Check the tooltip for each input field for more
information.

Not all fields are required. A keyblade can be created with just a base model/texture as well as at least one remastered
texture.
