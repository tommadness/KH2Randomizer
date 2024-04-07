# Keyblade Folder/File Structure

This folder/file structure is designed so that the randomizer is able to patch the keyblade visuals and
effects _without_ altering the keyblade's hitbox / collision box.

### Notes:

* See [Packaging Keyblades](../keyblades/index.md#packaging-keyblades) for instructions on how to package an external
  keyblade into this folder/file structure from the seed generator.
* Once a keyblade is packaged, see [Importing Keyblade(s)](../keyblades/index.md#importing-keyblades) for instructions
  for importing packaged keyblades into the keyblade randomization pool.

#### Specifications

The keyblade folder structure expects files to be in well-known sub-folders and have certain file names/extensions so
that the randomizer can quickly and unambiguously find the files it needs.

Other files may be included for future consideration, but only files used by the randomizer at this time are listed for
simplicity.

```
My Keyblade/                      the root folder is the name of the keyblade
  keyblade.json                   metadata such as versioning, an optional author for attribution, etc. (Required)

  itempic/
    [any name].dds                remastered item picture for the keyblade (Required)

  base/
    [any name].texture            texture data for the keyblade. This file is usually unpacked from the keyblade's
                                  `.mdlx` file as part of packaging the external keyblade. Allows for the `.tim` file
                                  extension as well. (Required)

    [any name].model              model data for the keyblade. This file is usually unpacked from the keyblade's `.mdlx`
                                  file as part of packaging the external keyblade. Allows for the alternate `.tim` file
                                  extension as well. (Required)

    [any name].pax                effect(s) for the keyblade. This file is usually unpacked from the keyblade's `.a.us`
                                  file as part of packaging the external keyblade.

    [any name].scd                sound effects file for the keyblade. The `.scd` extension is added to the file when
                                  packaging the external keyblade to allow for previewing the sound effects more easily.

    remastered-effects/           remastered effects for the keyblade. The file names will be used as-is, so be sure
      -0.dds                      that these files are named correctly.
      -1.dds
      etc.

    remastered-textures/          remastered textures for the keyblade. The file names will be used as-is, so be sure
      -0.dds                      that these files are named correctly.
      etc.

  nm/                             Halloween Town specific keyblade assets. Same structure as the `base` folder.
                                  Everything in here is optional - falls back to the base assets as needed.

  tr/                             Space Paranoids specific keyblade assets. Same structure as the `base` folder.
                                  Everything in here is optional - falls back to the base assets as needed.

  wi/                             Timeless River specific keyblade assets. Same structure as the `base` folder.
                                  Everything in here is optional - falls back to the base assets as needed.
```

A `.kh2randokb` file is simply a standard zip file where the files inside are arranged in the folder structure described
above. The intended usage of this file type is for sharing of randomizer-capable keyblades. The randomizer seed
generator provides a [Package Custom Keyblade](../keyblades/index.md#packaging-keyblades) option to properly package all
the keyblade assets.
