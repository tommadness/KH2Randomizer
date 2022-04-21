# Randomized Music

The KH2 Randomizer supports randomizing music from any of the games in KH 1.5/2.5/2.8, as well as your own custom music.
Below are some basic guidelines for how to set this up.

### Kingdom Hearts Music

For Kingdom Hearts 2, this is setup automatically once you have the rest of the randomizer working. For the other games
in the series, the games need to be extracted into the same folder as the extracted copy of KH2 (instructions for this
are outside the scope of this page). In the list of music choices, the randomizer will only show the games that you have
properly extracted.

A mapping of the built in songs used, and what category they are assigned, can be found at the
top [here](https://github.com/tommadness/KH2Randomizer/blob/master/Module/randomBGM.py).

### Custom Music

All your custom music should go in a folder called `custom` which is in the same folder as the rest of your extracted
games. Each folder within this `custom` folder becomes an option in the list of music choices in the randomizer.

Organize your custom `.scd` files as you like within different folders for different options of music (making
custom `.scd` files is outside the scope of this page).

By default, each song is given a music category of `unknown`, but this can be overridden by creating a `config.txt` file
within a folder (see below).

A category folder can have subfolders as well, and they will all be added into the same category. The use for this is
each subfolder can have a different config file, allowing easier control of the categories of different music.

Any folder that starts with an _ will be ignored by the randomizer, which can be used to quickly disable groups of songs
from being included.

### Config

A config.txt can have two types of lines (others are ignored).

`category=(unknown|battle|field|boss|title|cutscene)`

This is the type of music that will be applied to all the .scd files in this folder (not subfolders).

`<songname.scd>=(unknown|battle|field|boss|title|cutscene)`

In addition, you can add lines to override specific songs to a specific type of music.

### Categories

Custom Music doesn't require using categories, but by adding them you can use the separation options 
(such as `Randomize Field & Battle Music Separately`) to make sure tracks only get randomized to specific areas in the game.

A breif description of each category are as follows:

- `field`
Music to be used for world field themes.
- `battle`
Music to be used for world battle themes.
- `boss`
Music to be used for boss fight and non world specific battle music (Ex. Tension Rising, Vim & Vigor, ect.).
This category is teated as `battle` when not using `Randomize Special Battle Music Separately`.
- `title`
Music to be used for the Title and Battle Report Dearly Beloved themes.
This category is teated as `field` when not using `Randomize Dearly Beloved Separately`.
- `cutscene`
Music to be used for cutscens.
This category is teated as `field` when not using `Randomize Cutscene Music Separately`.
- `unknown`
Music that can be chosen for any of the above.

### Example

Here is an example folder of extracted games and custom music, and then I will explain how the randomizer treats the
music.

```
kh_games
  * kh2
  * bbs
  * custom
    * ffx
      > Victory Fanfare.scd
    * oot
      * overworld
        > config.txt
        > Kokiri Forest.scd
        > Market.scd
      * dungeon   
        > config.txt
        > Middle Boss Battle.scd
        > Dinosaur Boss Battle.scd
        > Dodongo's Cavern.scd
      * _songs 
        > Song of Time.scd
        > Song of Storms.scd
```

config.txt of overworld folder

```
category=field
```

config.txt of dungeon folder

```
category=battle
Dodongo's Cavern.scd=field
```

Explanation:

When I open the Cosmetics tab of the randomizer, 4 options will show up for music (`kh2`, `bbs`, `ffx`, `oot`).

If `ffx` is chosen, the `Victory Fanfare.scd` will be added into the randomization pool with a category of `unknown`.

If `oot` is chosen, then the `overworld` and `dungeon` folders will be added into the randomization pool, but
the `_songs` folder will be ignored. Everything in the `overworld` folder will be given the category of `field`. The two
boss battle themes in the `dungeon` folder are given a category of `battle`, but the `Dodongo's Cavern.scd` file is
given a category of `field`.
