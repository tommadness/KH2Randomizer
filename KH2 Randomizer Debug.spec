# -*- mode: python ; coding: utf-8 -*-


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
        dest_dirname = dest_dirname.split("site-packages" + os.sep)[1]
      
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
        'static/**/*.*',
        'static/*.*',
        'Module/icon.png',
        'extracted_data.zip'
    ]) + external_data_recursive([khbrpath+"/**/*.*"]),
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
    a.binaries,
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
