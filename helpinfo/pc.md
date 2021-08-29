# Setting up PC Seeds using Build-From-MM

The OpenKH mods manager does not currently support PC directly, however using a bridge program it is possible to use mods built by mods manager on PC.

## First Time Setup (Should Only have to follow these once)

Presetup note: Make sure the versions of the .PKG/.HED files in your KH1.5/2.5 install folder are unmodified (If you have previously modified them either restore backups, or right click the game in EGS and "verify game files")

- Download the zip of the latest release of the [khpc-modsmanager-bridge](https://github.com/thundrio-kh/khpc-modsmanager-bridge/releases/), and extract it to a folder of your choice.
- Run the build_from_mm.exe, and in the window that appears a few directories need to be set under "setup".
* openkh_path: This should be the directory containing your openkh installation (so the mods manager exe/everything else).
    Example: `C:\Users\randouser1001\Desktop\openkh`
* extracted_games_path: This is the folder where build_from_mm.exe will extract your kh2 pkg files to (as well as BBS/Recom/KH1 if you choose to extract those as well). Inside this folder a subfolder called "kh2" will be created containing the extracted files (this will be important when configuring the mods manager later).
    Example: `C:\Users\randouser1001\Desktop\KH_Games`
* khgame_path: This is the folder containing your KH1.5/2.5 installation by Epic Games
    Example: `C:\Program Files\Epic Games\KH_1.5_2.5`
* patches_path: This is a folder containing any .kh2pcpatch files you want applied when installing a seed. The .kh2pcpatch files will be applied in alphabetical order, with the mods build by mods manager being applied last.
    Example: `C:\Users\randouser1001\Desktop\kh2patches`
Note: If you are using GOA ROM edition, the .kh2pcpatch version of GoA ROM will not work. You will need to install it using the mods manager (see below).
- After the paths are set, change the mode option to "extract". You most likely want to leave every other option the same.
- Then click Start, and wait for the extract to finish. This will take several minutes, and may throw an error early on if you do not have the unmodified .pkg/.hed files in your KH1.5/2.5 folder.
(hint: the other patch manager for PC will create a backup folder automatically in the KH1.5/2.5 folder, and you can just copy those files into the `image/en` location instead of redownloading the original files from EGS)
- NOTE: If you plan on using the randomized music option with music from BBS or RECOM, you must rerun the extraction with "bbs" and "recom" selected as well.

- Once that is completed successfully, open up your copy of the OpenKH mods manager, and rerun the setup wizard (this is assuming you have already set it up once). Click next to go through each option except for when you get to where it asks you for the location of the extracted KH2 Folder. For this setting click "browse" and find the "kh2" folder that was created above inside your "extracted_games_path". Then for language select (us/us) or whatever your region is.
Note: You will have issues if you try to run pscx2 using the mods manager setup for PC. If you regularly run seeds on both PC and PCSX2, I would recommend having a completely separate copy of the OpenKH folder for each.

- If you are using GoA ROM edition then install the openkh mod version of that `KH2FM-Mods-Num/GoA-ROM-Edition`

## Installing a Seed

- Generate a seed and download it using the "Download for PC" option (Depending on the configured options it may be possible for PS2 seeds to work for PC, but this is not recommended)
- Install the mod into the Mods Manager, and make sure it is highest in your priority list. If using GoA ROM edition then that mod should be selected as well (the All In One and text patches typically used for PS2 are not supported on PC)
- Instead of using "Build and Run" like you would for PS2, just select "Build Only". And when the grey box that pops up disappears you can close the Mods Manager.
- Open up the build_from_mm.exe, make sure kh2 and patch are selected, then click Start (these are the default options, and your selected paths will be saved from previous runs)
- This will take a while to run, depending on the speed of your computer. If it completes successfully, you can launch the game and the seed will be running (you can close build_from_mm after it completes)