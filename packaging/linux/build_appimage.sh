#!/usr/bin/env bash
# Builds KH2.Randomizer-x86_64.AppImage from the repo root.
#
# Requirements:
#   - A Python environment with requirements.txt installed (default: .venv in the
#     repo root; override with PYTHON=/path/to/python)
#   - extracted_data.zip present in the repo root (same as the Windows build)
#   - appimagetool on PATH (downloaded automatically if missing)
#
# For maximum compatibility, run the build on the oldest distro you intend to
# support (the bundled glibc floor comes from the build machine).
set -euo pipefail

cd "$(dirname "$0")/../.."

PYTHON=${PYTHON:-.venv/bin/python}
BUILD_DIR=build/appimage
APPDIR="$BUILD_DIR/AppDir"
OUTPUT_NAME="KH2.Randomizer-x86_64.AppImage"
APPIMAGETOOL_SHA256="a6d71e2b6cd66f8e8d16c37ad164658985e0cf5fcaa950c90a482890cb9d13e0"

if [ ! -f extracted_data.zip ]; then
    echo "error: extracted_data.zip not found in the repo root (required for bundling)" >&2
    exit 1
fi

"$PYTHON" -m PyInstaller --noconfirm "KH2 Randomizer Linux.spec"

rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin" "$APPDIR/usr/share/icons/hicolor/256x256/apps"
cp -r dist/kh2randomizer "$APPDIR/usr/bin/kh2randomizer"
install -m 755 packaging/linux/AppRun "$APPDIR/AppRun"
cp packaging/linux/kh2randomizer.desktop "$APPDIR/"
"$PYTHON" -c "from PIL import Image; Image.open('rando.ico').save('$APPDIR/kh2randomizer.png')"
cp "$APPDIR/kh2randomizer.png" "$APPDIR/usr/share/icons/hicolor/256x256/apps/kh2randomizer.png"

APPIMAGETOOL=${APPIMAGETOOL:-appimagetool}
if ! command -v "$APPIMAGETOOL" >/dev/null 2>&1; then
    APPIMAGETOOL="$BUILD_DIR/appimagetool-x86_64.AppImage"
    if [ ! -x "$APPIMAGETOOL" ]; then
        echo "Downloading appimagetool..."
        curl -fL -o "$APPIMAGETOOL" \
            "https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage"
        chmod +x "$APPIMAGETOOL"
    fi
    echo "$APPIMAGETOOL_SHA256  $APPIMAGETOOL" | sha256sum --check -
fi

ARCH=x86_64 "$APPIMAGETOOL" "$APPDIR" "$OUTPUT_NAME"
echo "Built $OUTPUT_NAME"
