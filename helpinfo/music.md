## Daily Seeds

The KH2 Randomizer supports randomizing music from any of the games in KH 1.5/2.5/2.8, as well as your own custom music. Below are some basic guidelines for how to set this up

### KH Music

For Kingdom Hearts 2, this is setup automatically once you have the rest of the randomizer working. For the other games in the series, the games need to be extracted into the same folder as the extracted copy of KH2 (instructions for this are outside the scope of this page). In the list of music choices, the randomizer will only show the games that you have properly extracted. 

### Custom Music

All your custom music should go in a folder called `custom` which is in the same folder as the rest of your extracted games. Each folder within this `custom` folder becomes a option in the list of music choices in the randomizer.

Organize your custom scd files as you like within different folders for different options of music (making custom .scd files is outside the scope of this page).

By default each song is given a music category of `unknown`, but this can be overridden by creating a `config.txt` file within a folder (see below).

A category folder can have subfolders as well and they will all be added into the same category. The use for this is each subfolder can have a different config file, allowing easier control of the categories of different music

Any folder that starts with an _ will be ignored by the randomizer, which can be used to quickly disable groups of songs from being included


### Config

A config.txt can have two types of lines (others are ignored)

`category=(unknown|battle|field|cutscene)`

This is the type of music that will be applied to all the .scd files in this folder (not subfolders).

`<songname.scd>=(unknown|battle|field|cutscene)

In addition you can add lines to override specific songs to a specific type of music


### Example

Here is an example folder of extracted games and custom music, and then I will explain how the randomizer treats the music

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

When I open the cosmetic section of the randomizer, 4 options will show up for music
kh2
bbs
ffx
oot

If ffx is chosen, the `Victory Fanfare.scd` will be added into the randomization pool with a category of `unknown`

If oot is chosen then the overworld and dungeon folders will be added into the randomization pool, but the _songs folder will be ignored. Everything in the overworld folder will be given the category of `field`. The two boss battle themes in the dungeon folder are given a category of `battle`, but the `Dodongo's Cavern.scd` file is given a category of `field`.