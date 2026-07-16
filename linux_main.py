"""
Entry point for the Linux bundle. The same executable serves as both the main app and
the updater (via --updater), since the AppImage can't ship a second executable the way
the Windows build bundles updater.exe.
"""
import sys

if __name__ == "__main__":
    if "--updater" in sys.argv:
        import updater
        updater.main()
    else:
        import localUI
        localUI.main()
