# Texture Recolor Template Format

A _recolor template_ is a configuration of how a game entity may be colored.

**id** - A unique, filename-safe identifier for the entity being colored.

**name** - The user-facing name for the entity being colored.

**tags** - A list of strings representing metadata about the type of entity. Some of these are used by the generator to
categorize entities.

**recolors** - A list of [Recolor Definitions](#recolor-definition) for the entity.

### Recolor Definition

A grouping of texture images that will be colored using the same rules.

**colorable_areas** - A list of [Colorable Areas](#colorable-area) that apply to all images in this recolor definition.

**image_groups** - A list of groups of images to color using the same replacement color(s). Each image group contains
only texture images that are _visually identical_ in the base game assets. Note that some texture images are very
similar, but not visually identical. Such images that are visually similar should be placed in their own group.

An image group has a list of **images** and a **required** property that configures whether that group is necessary or
optional. This is used for filtering out "extra" textures such as high-resolution cutscene textures.

### Colorable Area

Configures a specific area of an entity that can be colored.

**id** - A unique (within the same entity), filename-safe identifier for the area being colored.

**name** - The user-facing name for the area being colored.

**new_saturation (optional)** - A new color saturation (on a scale of 0-100) to apply to this area when recoloring.
Most often only applicable when coloring areas that are mainly black/white/gray.

**value_offset (optional)** - A value (between -100 and 100) by which to offset the color value of each pixel within
this area when recoloring. Most often only applicable when coloring areas that are mainly black/white/gray.

#### Option 1 - Dynamic color matching

**hue_start/hue_end (optional)** - The range of color hues (0-360) to match when computing which pixels should be
colored as part of this area. The range can "wrap around" if needed (i.e. hue range could be 150-210 to match hues in
the middle of the color spectrum, or it could be 300-60 to match hues both at the start and end of the color spectrum).

**saturation_start/saturation_end (optional)** - The range of color saturation values (on a scale of 0-100) to match
when computing which pixels should be colored as part of this area.

**value_start/value_end (optional)** - The range of color values (on a scale of 0-100) to match when computing which
pixels should be colored as part of this area.

#### Option 2 - Area masking

**mask_files** - A listing of files containing masks of areas that should be colored. The mask files are a format
derived from an image file where areas containing red pixels are considered part of the colorable area. There needs to
be one item in this list per image group. Use `N/A` to indicate that there is no mask file for a specific group.

The current way to create an encoded mask file from a mask image file is to use the `Configure -> Create Texture
Recolor` menu option (only available in a special debug build of the seed generator).

## Full Examples with Comments

### Dynamic color matching example

```yaml
- id: sora
  name: Sora
  tags:
    - character
    - party
  recolors:
    # Sora's main clothing, belt, and shoes are all in the same texture images, so that's one "recolor definition"
    - colorable_areas:

        # The first colorable area is for Sora's main clothing. The clothing color is black/dark gray, so matching on
        # hue isn't particularly helpful. We do our best to just match on pixels that have low saturation and low value,
        # and we apply a new saturation and value offset to those pixels so that when we apply a new hue, it actually
        # ends up doing something visible.
        - id: main
          name: Main
          saturation_start: 0
          saturation_end: 25
          value_start: 0
          value_end: 30
          new_saturation: 50
          value_offset: 15

        # The second colorable area is for Sora's belts and shoes. These are normally yellow-ish, so we can match on a
        # specific range of color hues to just isolate those yellow-ish pixels.
        - id: belt_shoes
          name: Belt/Shoes
          hue_start: 27
          hue_end: 57

      image_groups:

        # At first glance, all these images appear the same, but they are not, so we split them into 3 distinct groups.
        # All the images across these groups will have the same colors applied to them, but because the source images
        # are not the same, the generator will create 3 individual recolored images and will apply them appropriately in
        # the mod using Mod Manager's `multi` capabilities (as opposed to needing to create an individual recolored
        # image for every one of these).
        - required: true
          images:
            - remastered/obj/ACTOR_SORA.mdlx/-0.dds
            - remastered/obj/ACTOR_SORA_H.mdlx/-3.dds
            - remastered/obj/AL14_PLAYER.mdlx/-0.dds
            - remastered/obj/DEAD_BOSS.mdlx/-0.dds
            - remastered/obj/LAST_ATTACKER.mdlx/-0.dds
            - remastered/obj/LAST_GIMMICK.mdlx/-0.dds
            - remastered/obj/LAST_HITMARK.mdlx/-0.dds
            - remastered/obj/PO06_PLAYER.mdlx/-0.dds
            - remastered/obj/PO07_PLAYER.mdlx/-0.dds
            - remastered/obj/PO08_PLAYER.mdlx/-0.dds
            - remastered/obj/WM_EX100.mdlx/-0.dds

        - required: false  # This is a high-resolution cutscene texture so it's optional
          images:
            - remastered/obj/H_EX500.mdlx/-3.dds

        - required: true
          images:
            - remastered/obj/P_EX100.mdlx/-0.dds
            - remastered/obj/P_EX100_AL_CARPET.mdlx/-0.dds
            - remastered/obj/P_EX100_LAST.mdlx/-0.dds
            - remastered/obj/P_EX100_MEMO.mdlx/-0.dds
            - remastered/obj/P_EX100_NPC.mdlx/-0.dds
            - remastered/obj/P_EX100_WM.mdlx/-0.dds

    # The accent color on Sora's side is in a separate set of texture images, so that's a separate "recolor definition".
    # The only colorable area we have defined for this is a shade of red that's easy to isolate by a hue range.
    - colorable_areas:
        - id: side_accent
          name: Side Accent
          hue_start: 0
          hue_end: 8
      image_groups:

        # The image groups here are similar to above, but there's actually a fourth visually distinct image, so we need
        # 4 image groups for this one.
        - required: true
          images:
            - remastered/obj/ACTOR_SORA.mdlx/-1.dds
            - remastered/obj/AL14_PLAYER.mdlx/-1.dds
            - remastered/obj/DEAD_BOSS.mdlx/-1.dds
            - remastered/obj/LAST_ATTACKER.mdlx/-1.dds
            - remastered/obj/LAST_GIMMICK.mdlx/-1.dds
            - remastered/obj/LAST_HITMARK.mdlx/-1.dds
            - remastered/obj/PO06_PLAYER.mdlx/-1.dds
            - remastered/obj/PO07_PLAYER.mdlx/-1.dds
            - remastered/obj/PO08_PLAYER.mdlx/-1.dds
            - remastered/obj/WM_EX100.mdlx/-1.dds

        - required: true
          images:
            - remastered/obj/ACTOR_SORA_H.mdlx/-0.dds

        - required: false  # This is a high-resolution cutscene texture so it's optional
          images:
            - remastered/obj/H_EX500.mdlx/-0.dds

        - required: true
          images:
            - remastered/obj/P_EX100.mdlx/-1.dds
            - remastered/obj/P_EX100_AL_CARPET.mdlx/-1.dds
            - remastered/obj/P_EX100_LAST.mdlx/-1.dds
            - remastered/obj/P_EX100_MEMO.mdlx/-1.dds
            - remastered/obj/P_EX100_NPC.mdlx/-1.dds
            - remastered/obj/P_EX100_WM.mdlx/-1.dds
```

### Mask files example

```yaml
- id: xemnas_final
  name: Xemnas (Final)
  tags:
    - character
  recolors:
    # We define four colorable areas for Final Xemnas. All the areas are contained within three unique
    # texture images.
    - colorable_areas:
        - id: white
          name: White
          mask_files:
            # There are mask files for the second and third image group for the white area, but none is needed for the
            # first group, so that group just gets an N/A designation.
            - N/A
            - static/recolors/masks/xemnas-final/1_White.mask
            - static/recolors/masks/xemnas-final/2_White.mask
          new_saturation: 50
        - id: black
          name: Black
          mask_files:
            # The black area is in both the second and third textures
            - N/A
            - static/recolors/masks/xemnas-final/1_Black.mask
            - static/recolors/masks/xemnas-final/2_Black.mask
          new_saturation: 50
        - id: silver
          name: Silver
          mask_files:
            # The silver area is in both the first and second textures
            - static/recolors/masks/xemnas-final/0_Silver.mask
            - static/recolors/masks/xemnas-final/1_Silver.mask
            - N/A
          new_saturation: 50
        - id: trim
          name: Trim
          mask_files:
            # The trim is only in the third texture
            - N/A
            - N/A
            - static/recolors/masks/xemnas-final/2_Trim.mask
          new_saturation: 50
      image_groups:
        - required: true
          images:
            - remastered/obj/B_EX170_LAST.mdlx/-0.dds
            - remastered/obj/B_EX170_LAST_LV99.mdlx/-0.dds

        - required: true
          images:
            - remastered/obj/B_EX170_LAST.mdlx/-1.dds
            - remastered/obj/B_EX170_LAST_LV99.mdlx/-1.dds

        - required: true
          images:
            - remastered/obj/B_EX170_LAST.mdlx/-2.dds
            - remastered/obj/B_EX170_LAST_LV99.mdlx/-2.dds
```
