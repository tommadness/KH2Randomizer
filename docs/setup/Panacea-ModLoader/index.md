# PC New Setup Guide

* *Heads up! It's recommended to run the game once before installing the randomizer, so that the game can make some systems files for itself. Otherwise the game may not boot up correctly after the randomzier is installed.*

## Resources Needed:
* [OpenKH](https://github.com/OpenKH/OpenKh/releases/download/release-412/openkh-build1892.zip)
* [Seed Generator](https://github.com/tommadness/KH2Randomizer/releases/latest/download/Kingdom.Hearts.II.Final.Mix.Randomizer.zip)

## Extract your files
1. Create a KH2 Rando Folder (Recommended *not* to be in your games installation folder)
2. Extract OpenKH to this folder
3. Extract Seed Generator to this Folder

## How to Setup The Mod Manager:
1. Run the **"OpenKh.Tools.ModsManager"** in the OpenKH folder 
	- The Setup Wizard will open automatically, click **"Next"** to start.
2. Change game edition to **"PC Release Via Epic Games Store"
	- image here
3. Then click the folder icon and navigate to your installation (Default C:\Program Files\Epic Games\KH_1.5_2.5)
	-gif here
4. Click the **"Install OpenKH Panacea"** Button. This will install the mod loader to your game installation folder
5. If you want to bypass the epic games launcher, and kh games launch window, check the **"Bypass the launcher"** check box
	- *You will need to input your epic games user id, which can be found using the link below the text box*
6. Keep the extraction folder location as default, and click on the **"extract game data"** button. You will need to wait a few minutes for the process to complete.
### *You have successfully installed the mod manager*

## Garden of Assemblage Mod:
1. Click **"Mods"** in the top left
	-image here
2. In the **"add a new mod from github"** section, type in the account name and mod name.
	-gif here
	- Type **"KH2FM-Mods-Num/GoA-ROM-Edition"** into the text box and click on **"install"** in the bottom right
*Note: You can find more mods made by the community in the rando discord, checkout the **"Mods and Scripts"** Section*
3. To enable the mod, be sure to click the checkbox next to the newly added mod in the list
	-image here
4. Then click **"Game"** and **"build", then **"build only"
	-gif here
*Note: Every time you add a new mod to the list you will need to **"Build"** again, or it wont show up in game*
### *You have now successfully installed the Garden of Assemblage Mod*

## Lua Backend Installation:
1. Open the seed generator program
2. In the top left click on the **"Configure"** tab, then click on **"Luabackend Hook Setup (PC Only)
	-Image here
3. In this new window click on **"browse"** next to the OpenKh Location, and browse to your openkh folder, then click **"select folder"
	-gif here
4. For **"Mod mode", click the drop down and select **"Panacea/Mod Loader"
5. Click on **"Check configuration"
*The status messages below should say **"Not Found"*
6. Now click on the **"Download/Install/Configure"** button in the bottom left
*This will download and install the luabackend hooks required for the Panacea Mod Loader to work, these files go directly into your game installation folder*
### *The Backend Hook has been installed into your game folder now, you can close this window*

## Installing a new seed to play:
1. Choose your seed settings in the generator window and then click on **"Generate Seed"** in the bottom right.
*If you choose settings that may not act the same between the PCSX2 and PC version, the button will separate between PC and PCSX2, be sure to click the right one if it does so.*
2. This will open up a window to save the seed as a zip file. Save it anywhere that works for you (I like to place it in the same folder as the generator)
3. Once saved, open up the mod manager and click on **"Mods", then **"install a new mod
	-image here
4. This time click on **"select and install mod archive", navigate to your new seed zip file and click **"open"
	-gif here
*This will add the seed to your mods list*
### *Note: It is very important that the seed is always ABOVE the GoA ROM mod in the list. The Randomizer will not work otherwise*
5. Be sure to click on the check box next to the seed, then click on **"build"** and **"build only"** to enable the mod in game
	-gif here

# *You are now ready to play a KH2 Rando Seed! Run the game from the epic games launcher and have fun!*

*Note:* (If you chose the **"Bypass Launcher"** option during the wizard setup you will need to choose the **"Run"** option under the **"Game"** tab in Mod Manager. You can also choose the **"Build and Run Option"** to enable your new mods and start the game at the same time.
