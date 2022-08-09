# Migrating from Mods Manager Bridge

With a recent release of the OpenKH tools, Mods Manager Bridge (also known as `build_from_mm` or `bfmm` in many places)
should no longer be needed for most KH2 Randomizer players. There are two newer options that should largely eliminate
the need for Mods Manager Bridge.

### Using OpenKH Panacea to load mods

This option installs a "mod loader" next to the game files that instructs the game to load mods that you have
configured, without ever touching the actual game files themselves. See
[Migrating to OpenKH Panacea](migrate-panacea.md) to learn how to migrate to this option.

### Patching within OpenKH Mods Manager

This option uses a similar build and patch approach to Mods Manager Bridge, but the patching step can now be done within
OpenKH Mods Manager itself. See [Migrating to OpenKH Mods Manager patching](migrate-patching.md) to learn how to migrate
to this option.
