# Texture Colors

When the _Recolor Some Textures_ setting is enabled, some of the in-game textures can be recolored. The seed generator
has the ability to recolor most playable characters, many non-playable characters, most Heartless, and most Nobodies
(including bosses).

> Due to the way textures are applied, this option will only work properly when using Panacea for loading mods into the
> PC versions of the game.

## Texture Recolor Settings

From the _Cosmetics_ tab use the _Texture Recolor Settings_ button to open the window for configuring texture colors.
The window contains several settings, as well as a sample of the original texture and a preview of the recolored
texture.

![Settings Window](texture-recolor-settings.png)

### Menus

**Presets** - Contains options for setting all colors to vanilla, all colors to random, as well as the ability to save
and load presets similar to presets for seed settings.

**Category** - Contains options to set all colors for all models in the selected category to vanilla or random.

**Model** - Contains options to set colors for all colorable areas of the selected model to vanilla or random.

### Area To Color

**Category** - Can be used to filter the models available for selection.

**Model** - Chooses the model for which to edit colors.

**Area** - Chooses the area within the selected model for coloring.

### Color to Use

**Setting** - Chooses how to color the selected area of the selected model.

* Vanilla - Do not recolor this area.
* Randomized - Choose a random color for this area each time a seed (or cosmetics-only mod) is generated.
* Custom - Use a specific color for this area.

**Color Hue** - Chooses the color hue (0-360) to use to color the selected color area of the selected model. Only
applicable when the color _Setting_ is Custom.

General estimates of hue values:
* 0 - Red
* 60 - Yellow
* 120 - Green
* 180 - Cyan
* 240 - Blue
* 270 - Purple
* 330 - Pink

### Other

**Include Extra Textures** - If enabled, additional textures (such as high-resolution cutscene textures) will also be
recolored. This uses additional disk space and causes generation to take longer.

If you play rando with a cutscene skipper or always skip cutscenes, it's recommended to leave this setting disabled.

**Keep Previously Generated Textures** - If enabled, previously generated textures will be kept around to speed up
future recolors. This will potentially use large amounts of disk space, but improves performance. Disable this option to
minimize disk space usage, but recoloring will take longer for each seed.

**Compress Textures** - If enabled, recolored textures will use image compression. This saves a **large** amount of disk
space, but could have performance impacts on the game (none have been found, but it's possible), and causes recolored
textures to take slightly longer to generate.

**Refresh Preview(s)** - Displays or refreshes the preview image(s) that help show what the texture recoloring will look
like when applied. Depending on the texture and your machine's performance, this can take a few seconds or more.

## Other Notes

- Coloring the textures is done by applying color hues to the base game textures found in your extracted game files.
  Because of this, texture coloring is only available if you have extracted your KH2 game files using OpenKH Mods
  Manager.
- Texture coloring will cause seeds (or cosmetics-only mods) to take longer to generate, relative to the number of
  recolored textures. However, the generator stores off copies of each recolored texture it creates to speed up future
  generations. So over time, the generation speed will improve (at the expense of disk space).
- Previously generated texture recolors are kept in a `cache/texture-recolors` folder next to where the seed generator
  is located. This folder can be safely deleted for disk space concerns, but as described above, doing so will cause
  seeds/mods with texture recoloring enabled to take longer to generate.
