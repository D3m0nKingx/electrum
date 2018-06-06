# -*- mode: python -*-

from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs

import sys
import os

PACKAGE='Electrum-Ganja'
PYPKG='electrum-ganja'
MAIN_SCRIPT='electrum-ganja'
ICONS_FILE='electrum-ganja.icns'

for i, x in enumerate(sys.argv):
    if x == '--name':
        VERSION = sys.argv[i+1]
        break
else:
    raise Exception('no version')

electrum-ganja = os.path.abspath(".") + "/"
block_cipher = None

# see https://github.com/pyinstaller/pyinstaller/issues/2005
hiddenimports = []
hiddenimports += collect_submodules('trezorlib')
hiddenimports += collect_submodules('btchip')
hiddenimports += collect_submodules('keepkeylib')
hiddenimports += collect_submodules('websocket')

datas = [
    (electrum-ganja+'lib/currencies.json', PYPKG),
    (electrum-ganja+'lib/servers.json', PYPKG),
    (electrum-ganja+'lib/checkpoints.json', PYPKG),
    (electrum-ganja+'lib/servers_testnet.json', PYPKG),
    (electrum-ganja+'lib/checkpoints_testnet.json', PYPKG),
    (electrum-ganja+'lib/wordlist/english.txt', PYPKG + '/wordlist'),
    (electrum-ganja+'lib/locale', PYPKG + '/locale'),
    (electrum-ganja+'plugins', PYPKG + '_plugins'),
]
datas += collect_data_files('trezorlib')
datas += collect_data_files('btchip')
datas += collect_data_files('keepkeylib')

# Add libusb so Trezor will work
binaries = [(electrum-ganja + "contrib/build-osx/libusb-1.0.dylib", ".")]
binaries += [(electrum-ganja + "contrib/build-osx/libsecp256k1.0.dylib", ".")]

# Workaround for "Retro Look":
binaries += [b for b in collect_dynamic_libs('PyQt5') if 'macstyle' in b[0]]

# We don't put these files in to actually include them in the script but to make the Analysis method scan them for imports
a = Analysis([electrum-ganja+MAIN_SCRIPT,
              electrum-ganja+'gui/qt/main_window.py',
              electrum-ganja+'gui/text.py',
              electrum-ganja+'lib/util.py',
              electrum-ganja+'lib/wallet.py',
              electrum-ganja+'lib/simple_config.py',
              electrum-ganja+'lib/ganja.py',
	      electrum-ganja+'lib/blockchain.py',
              electrum-ganja+'lib/dnssec.py',
              electrum-ganja+'lib/commands.py',
              electrum-ganja+'plugins/cosigner_pool/qt.py',
              electrum-ganja+'plugins/email_requests/qt.py',
              electrum-ganja+'plugins/trezor/client.py',
              electrum-ganja+'plugins/trezor/qt.py',
              electrum-ganja+'plugins/keepkey/qt.py',
              electrum-ganja+'plugins/ledger/qt.py',
              ],
             binaries=binaries,
             datas=datas,
             hiddenimports=hiddenimports,
             hookspath=[])

# http://stackoverflow.com/questions/19055089/pyinstaller-onefile-warning-pyconfig-h-when-importing-scipy-or-scipy-signal
for d in a.datas:
    if 'pyconfig' in d[0]:
        a.datas.remove(d)
        break

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.datas,
          name=PACKAGE,
          debug=False,
          strip=False,
          upx=True,
          icon=electrum-ganja+ICONS_FILE,
          console=False)

app = BUNDLE(exe,
             version = VERSION,
             name=PACKAGE + '.app',
             icon=electrum-ganja+ICONS_FILE,
             bundle_identifier=None,
             info_plist={
                'NSHighResolutionCapable': 'True',
                'NSSupportsAutomaticGraphicsSwitching': 'True'
             }
)
