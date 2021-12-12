2.0 Zip Seed Generator Changelog
 
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