# Migrating from Mods Manager Bridge to OpenKH Panacea

This guide helps you migrate from using Mods Manager Bridge (`build_from_mm`) to the OpenKH Panacea mod loader. This
guide is _not_ meant to be a first-time setup guide - it assumes you already have a working setup with Mods Manager and
Mods Manager Bridge, and that you're comfortable using them to patch your game.

### 1. Make sure your game files are back to a vanilla/unpatched state before migrating

You absolutely want to make sure you start from a fresh set of game files. There are two ways to accomplish this:

* Option 1: Verify your game in Epic Games Store. This is the most foolproof way to ensure your game files are
  unpatched.

![Verify](../images/egs/verify.png)

* Option 2: Use the `restore` option in Mods Manager Bridge to restore the backup packages it created automatically when
  you first patched. This option will be faster than verifying in Epic Games Store since the backup files are already on
  your PC.

![Restore](../images/mods-manager-bridge/restore.png)

### 2. Install the latest version of the OpenKH tools

* Determine where you have the OpenKH tools installed on your PC. This is the folder that contains the Mods Manager
  program that you have already been using to add/remove mods.
* Download the latest version of the OpenKH tools (linked on the [Downloads](../../downloads/index.md) page).
  * Or click [HERE](https://cdn.discordapp.com/attachments/803658031749267517/1006967855633399838/openkh-modmanager.zip) for direct download
* Copy all files from the OpenKH tools zip file to your OpenKH tools location. When prompted to replace existing files,
  do so.
    * Alternatively, you could choose to copy all the files from the OpenKH tools zip file somewhere else to start fresh
      without affecting your existing OpenKH tools version.

### 3. Run the Mods Manager setup wizard

* Open Mods Manager. If you are starting fresh, the setup wizard will display. If not, choose `Settings -> Run wizard`.

![Run wizard](../images/mods-manager/run-wizard.png)

* On the `Game edition` screen, choose `PC Release via Epic Game Store` and browse to the folder containing the game
  executable files (for many setups `C:\Program Files\Epic Games\KH_1.5_2.5` but could be different for your PC).
  Choose `Next` to move on.

![Game edition](../images/mods-manager/wizard/game-edition-pc.png)

* On the `Install OpenKH Panacea` screen, choose to `Install OpenKH Panacea`. The wizard should inform you that Panacea
  is now installed (this should not take long). Choose `Next` to move on.

![Panacea](../images/mods-manager/wizard/panacea-not-installed.png) ![Panacea installed](../images/mods-manager/wizard/panacea-installed.png)

* On the next screen, leave `Bypass the launcher` unchecked and choose `Next` to move on. Bypassing the launcher is not
  recommended.

![Launcher](../images/mods-manager/wizard/bypass-launcher-unchecked.png)

* For the `Set Game Data Location` screen's `Extraction folder location`, you can use one of two approaches:
    * Browse to the folder where you extracted your KH2 game data using Mods Manager Bridge originally. As long as
      you're confident your extracted game data was from vanilla game files, this option should be fine.
    * Alternatively, choose a desired location and choose `Extract game data` to start an extraction. This will take
      several minutes, depending on your PC.
    * Either way, once finished, choose `Next` to move on.

![Game data](../images/mods-manager/wizard/game-data-location.png)

* Choose `Finish` to close the setup wizard and save your settings.

### 4. Configure LuaBackend Hook for Mods Manager integration

Version 2.1.5 of the seed generator adds a screen to help you configure LuaBackend Hook automatically.

* Open the seed generator and choose `Configure -> LuaBackend Hook Setup (PC Only)`.

![LuaBackend Hook Setup](../images/seed-generator/configure-luabackend-hook-setup.png)

* On the LuaBackend Hook Setup screen, browse to the location where your OpenKH tools (such as Mods Manager) are
  located, and choose your intended Mod mode. This choice affects the name of the LuaBackend Hook DLL file.
  * Choose `Panacea (Mod Loader)` if you intend to use OpenKH Panacea to load mods without patching game files. Panacea
    uses `DBGHELP.dll` to hook into the game, and it knows to look for LuaBackend Hook's file with the name
    `LuaBackend.dll`.
  * Choose `Patch / Fast Patch` if you intend to patch your game files. In this configuration, LuaBackend Hook is named
    `DBGHELP.dll` itself.
* Choose `Check Configuration`.

![Check Configuration](../images/seed-generator/luabackendhook-setup-panacea.png)

* If you already have LuaBackend Hook installed, the files will all be found, but `Configuration File Status` may report
  that LuaBackend Hook is not yet configured for Mods Manager integration. If this is the case, you can just choose
  `Apply Configuration` to apply the necessary configuration.
* If any of the files are missing, or if you just want a fresh copy, choose `Download/Install/Configure` which will
  download, install, and configure a compatible version of LuaBackend Hook.

After you've configured LuaBackend Hook for Mods Manager integration, you can now take advantage of several common mods
with bundled scripts.

* Remove GoA ROM, auto save, and soft reset Lua scripts (if they exist) from your
  `Documents\KINGDOM HEARTS HD 1.5+2.5 ReMIX\scripts\kh2` folder. We'll manage these scripts via Mods Manager now. If
  you have other Lua scripts in this folder, you can still manage those manually. We just don't want duplicates.
* Make sure GoA ROM Edition is up-to-date in Mods Manager. GoA ROM bundles its Lua script in recent versions.
* Install `KH2FM-Mods-equations19/auto-save` and `KH2FM-Mods-equations19/soft-reset` in Mods Manager. The order for
  these two mods doesn't matter.

![Mods with scripts](../images/mods-manager/example-mods-lua-scripts.png)

### 5. Use Mods Manager to configure mods

* Use Mods Manager to add/remove/check/uncheck mods as usual. (You may have fewer or more mods than shown here.)

![Mods list](../images/mods-manager/example-mods-list.png)

* Choose `Game -> Build -> Build Only` to prepare your mods.

![Build only](../images/mods-manager/build-only.png)

* A console window will come up while preparing mods and will disappear once finished. After this has finished, start
  your game normally and your chosen mods should be applied.

### 6. Preparing a new Randomizer Seed

* Works essentially the same as it did before, but without the additional patching step. Remove the previous randomizer
  seed from Mods Manager, add the new seed, and then Build Only again. The next time you start the game, the new seed
  will get loaded.

### 7. Removing Panacea (if desired)

* Once Panacea is installed, it will run every time you start the game and will attempt to load any mods that are built.
  To remove Panacea, you can run the setup wizard again and there is an option to `Remove OpenKH Panacea`.

![Remove Panacea](../images/mods-manager/wizard/panacea-installed.png)

* If you still want to use LuaBackend Hook, rename `LuaBackend.dll` back to `DBGHELP.dll` after Panacea is gone.

### What happens to my old KH2PCPATCH files?

The new update to the mod manager allows it to load in kh2pcpatch files as if they were regular mods. Just add your kh2pcpatch files the same way you would add a zip seed and the mod manager will handle everything for you.
