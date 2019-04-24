# -*- mode: python -*-
import PyInstaller.config
import sys, os, shutil

relative_path = os.getcwd()
try:
    shutil.rmtree(os.path.join(relative_path, 'out'))
    while os.path.exists('out'): # check if it exists
        pass
except:
    pass
os.mkdir(os.path.join(relative_path, 'out'))
os.mkdir(os.path.join(relative_path, 'out/build'))
os.mkdir(os.path.join(relative_path, 'out/build/build'))

PyInstaller.config.CONF['distpath'] = os.path.join(relative_path, 'out')
PyInstaller.config.CONF['workpath'] = os.path.join(relative_path, 'out\\build\\build')


src_path = os.path.join(relative_path, 'app')
assets_path = os.path.join(src_path, 'assets')

files = []
assets = []
for file in os.listdir(src_path):
        if ".py" in file:
            files.append(os.path.join(src_path, file))

for file in os.listdir(assets_path):
    assets.append((os.path.join(assets_path, file), '.'))

a = Analysis(files,
            pathex=[],
            binaries=[],
            datas=assets,
            hiddenimports=[],
            hookspath=[],
            runtime_hooks=[],
            excludes=[],
            win_no_prefer_redirects=False,
            win_private_assemblies=False,
            cipher=None,
            noarchive=False)

def get_numpy_path():
    import numpy
    numpy_path = numpy.__path__[0]
    return numpy_path

dict_tree = Tree(get_numpy_path(), prefix='numpy', excludes=["*.pyc"])
a.datas += dict_tree
a.binaries = filter(lambda x: 'numpy' not in x[0], a.binaries)

def get_sentry_path():
    import sentry_sdk
    sentry_path = sentry_sdk.__path__[0]
    return sentry_path

dict_tree = Tree(get_sentry_path(), prefix='sentry_sdk', excludes=["*.pyc"])
a.datas += dict_tree
a.binaries = filter(lambda x: 'sentry_sdk' not in x[0], a.binaries)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=None)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Bluegrass Polling Utility',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon = os.path.join(assets_path, 'icon.ico'))
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Bluegrass Polling Utility')


shutil.rmtree(os.path.join(relative_path, 'dist'))
shutil.rmtree(os.path.join(relative_path, 'build'))