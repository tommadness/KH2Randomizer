# -*- mode: python ; coding: utf-8 -*-

# Linux build: a single onedir app (see packaging/linux/build_appimage.sh, which wraps
# the output in an AppImage). Unlike the Windows build there is no separate updater
# executable; linux_main.py dispatches --updater to the updater UI.

import glob
import os

from PyInstaller.utils.hooks import collect_data_files


def build_datas_recursive(paths):
  datas = []

  for path in paths:
    for filename in glob.iglob(path, recursive=True):
      if os.path.isfile(filename):
        dest_dirname = os.path.dirname(filename)
        if dest_dirname == "":
          dest_dirname = "."

        data_entry = (filename, dest_dirname)
        datas.append(data_entry)
        print(data_entry)

  return datas


a = Analysis(
    ['linux_main.py'],
    pathex=[],
    binaries=[],
    datas=build_datas_recursive([
        'UI/**/*.*',
        'UI/*.*',
        'static/**/*.*',
        'static/*.*',
        'presets/*.*',
        'Module/icon.png',
        'extracted_data.zip',
       ]) + collect_data_files('kh2fmbr', include_py_files=False),
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='kh2randomizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='kh2randomizer',
)
