# -*- mode: python ; coding: utf-8 -*-


import os, glob, shutil, importlib, kh2fmbr

for root, dirs, files in os.walk(DISTPATH):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))


khbrpath = os.path.dirname(kh2fmbr.__file__)
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

def external_data_recursive(paths):
  datas = []
  
  for path in paths:
    for filename in glob.iglob(path, recursive=True):
      if os.path.isfile(filename):
        dest_dirname = os.path.dirname(filename)
        if dest_dirname == "":
          dest_dirname = "."
        else:
          dest_dirname = dest_dirname.split("site-packages" + os.sep)[1]
        
        data_entry = (filename, dest_dirname)
        datas.append(data_entry)
        print(data_entry)
  
  return datas


updater_analysis = Analysis(
    ['updater.py'],
    pathex=[],
    binaries=[],
    datas=build_datas_recursive([
        'UI/**/*.*',
        'UI/*.*',
        'Module/icon.png',
       ]),
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(updater_analysis.pure)

updater_exe = EXE(
    pyz,
    updater_analysis.scripts,
    updater_analysis.binaries,
    updater_analysis.datas,
    [],
    name='updater',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='rando.ico'
)

a = Analysis(
    ['localUI.py'],
    pathex=[],
    binaries=[('{0}/updater.exe'.format(DISTPATH),".")],
    datas=build_datas_recursive([
        'UI/**/*.*',
        'UI/*.*',
        'static/**/*.*',
        'static/*.*',
        'presets/*.*',
        'Module/icon.png',
        'extracted_data.zip'
       ]) + external_data_recursive([khbrpath+"/**/*"]),
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

rando_pyz = PYZ(a.pure)
exe = EXE(
    rando_pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='KH2 Randomizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='rando.ico'
)

#shutil.make_archive('Kingdom Hearts II Final Mix Randomizer', 'zip', DISTPATH)
