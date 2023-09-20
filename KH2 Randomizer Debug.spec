# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


import os, glob, khbr
khbrpath = os.path.dirname(khbr.__file__)
def build_datas_recursive(paths):
  datas = []
  
  for path in paths:
    for filename in glob.iglob(path, recursive=True):
      dest_dirname = os.path.dirname(filename)
      if dest_dirname == "":
        dest_dirname = "."
      
      data_entry = (filename, dest_dirname)
      datas.append(data_entry)
      print(data_entry)
  
  return datas


def external_data_recursive(paths):
  datas = []
  
  for path in paths:
    for filename in glob.iglob(path, recursive=True):
      dest_dirname = os.path.dirname(filename)
      if dest_dirname == "":
        dest_dirname = "."
      else:
        dest_dirname = dest_dirname.split("site-packages\\")[1]
      
      data_entry = (filename, dest_dirname)
      datas.append(data_entry)
      print(data_entry)
  
  return datas

a = Analysis(
    ['localUI.py'],
    pathex=[],
    binaries=[],
    datas=build_datas_recursive([
        'UI/**/*.*',
        'UI/*.*',
        'static/spoilerlog.html',
        'static/icons/**/*.*',
        'static/puzzle.bin',
        'static/KHMenu.otf',
        'static/as_data_split/*.*',
        'static/better_stt/*.*',
        'static/map_skip/*.*',
        'static/wardrobe/*.*',
        'static/khbr_override/*.*',
        'static/*.bar',
        'static/*.script',
        'static/*.bin',
        'static/*.json',
        'Module/icon.png',
        'extracted_data/**/*.*',
    ]) + external_data_recursive([khbrpath+"/**/*.*"]),
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)



exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='KH2 Randomizer DEBUG VERSION',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='rando.ico'
)

import shutil
presetPath = '{0}/presets'.format(DISTPATH)
if os.path.exists(presetPath):
  shutil.rmtree(presetPath)

dataPath = '{0}/extracted_data'.format(DISTPATH)
if os.path.exists(dataPath):
  shutil.rmtree(dataPath)

shutil.copytree('extracted_data', dataPath)
shutil.copytree('presets', presetPath)
