# Migrating from Mods Manager Bridge to OpenKH Mods Manager Patching

This guide helps you migrate from using Mods Manager Bridge (`build_from_mm`) to patching your game using OpenKH Mods
Manager itself. This guide is _not_ meant to be a first-time setup guide - it assumes you already have a working setup
with Mods Manager and Mods Manager Bridge, and that you're comfortable using them to patch your game.

### 1. Make sure your game files are back to a vanilla/unpatched state before migrating

You absolutely want to make sure you start from a fresh set of game files. There are two ways to accomplish this:

* Option 1: Verify your game in Epic Games Store. This is the most foolproof way to ensure your game files are
  unpatched.

![Verify](../images/egs/verify.png)

* Option 2: Use the `restore` option in Mods Manager Bridge to restore the backup packages it created automatically when
  you first patched. This option will be faster than verifying in Epic Games Store since the backup files are already on
  your PC.

![Restore](../images/mods-manager-bridge/restore.png)

* Go to your game installation folder and delete the **DBGHELP.dll, Luabackend.toml, and Lua54.dll files** before continuing as well.

### 2. Install the latest version of the OpenKH tools

* Determine where you have the OpenKH tools installed on your PC. This is the folder that contains the Mods Manager
  program that you have already been using to add/remove mods.
* Download the latest version of the OpenKH tools (linked on the [Downloads](../../downloads/index.md) page).
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

* On the `Install OpenKH Panacea` screen, just choose `Next` without installing as we'll be patching our game files
  rather than using OpenKH Panacea.

![Panacea](../images/mods-manager/wizard/panacea-not-installed.png)

* On the next screen, leave `Bypass the launcher` unchecked and choose `Next` to move on. Bypassing the launcher
  requires OpenKH Panacea to be installed, which we are choosing not to do with this setup.

![Launcher](../images/mods-manager/wizard/bypass-launcher-unchecked.png)

* For the `Set Game Data Location` screen's `Extraction folder location`, you can use one of two approaches:
    * Browse to the folder where you extracted your KH2 game data using Mods Manager Bridge originally. As long as
      you're confident your extracted game data was from vanilla game files, this option should be fine.
    * Alternatively, choose a desired location and choose `Extract game data` to start an extraction. This will take
      several minutes, depending on your PC.
    * Either way, once finished, choose `Next` to move on.

![Game data](../images/mods-manager/wizard/game-data-location.png)

* Choose `Finish` to close the setup wizard and save your settings.

### 4. Configure LuaBackend Hook for Mods Manager integration (optional but recommended)

If you haven't already done so, performing this step allows mods to bundle their own Lua scripts. See
[LuaBackend Hook Setup](../../luabackend-hook-setup/index.md) for more information, as well as instructions.

### 5. Use Mods Manager to configure mods

* Use Mods Manager to add/remove/check/uncheck mods as usual. (You may have fewer or more mods than shown here.)

![Mods list](../images/mods-manager/example-mods-list.png)

* Choose one of the `Game -> Build -> Build and Patch` options to begin patching your game.
    * If you've been using `fast_patch` all along in Mods Manager Bridge, the `Fast` option works mostly the same. If
      you've needed to use the full `patch` option in Mods Manager Bridge, then you probably want to avoid the `Fast`
      option here as well.

![Patch options](../images/mods-manager/build-and-patch.png)

* A console window will come up while patching and will disappear once finished. After the patching has finished, start
  your game normally and your chosen mods should be applied.

### 6. Patching a new Randomizer Seed

* Works essentially the same as it did before. Remove the previous randomizer seed from Mods Manager, add the new seed,
  and then Build and Patch again.

### 7. Restoring original files (if desired)

* The first time you patch within Mods Manager, backups of your original game packages will be made, so the first patch
  will take longer than subsequent patches. Choose `Game -> Restore` if you ever want to restore your game files to
  their original state from these backups.

![Restore](../images/mods-manager/restore.png)

### What happens to my old KH2PCPATCH files?

The new update to the mod manager allows it to load in kh2pcpatch files as if they were regular mods. Just add your kh2pcpatch files the same way you would add a zip seed and the mod manager will handle everything for you.
