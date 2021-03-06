#!/usr/bin/env python3

# python setup.py sdist --format=zip,gztar

from setuptools import setup
import os
import sys
import platform
import imp
import argparse

with open('contrib/requirements/requirements.txt') as f:
    requirements = f.read().splitlines()

with open('contrib/requirements/requirements-hw.txt') as f:
    requirements_hw = f.read().splitlines()

version = imp.load_source('version', 'lib/version.py')

if sys.version_info[:3] < (3, 4, 0):
    sys.exit("Error: Electrum-Ganja requires Python version >= 3.4.0...")

data_files = []

if platform.system() in ['Linux', 'FreeBSD', 'DragonFly']:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root=', dest='root_path', metavar='dir', default='/')
    opts, _ = parser.parse_known_args(sys.argv[1:])
    usr_share = os.path.join(sys.prefix, "share")
    icons_dirname = 'pixmaps'
    if not os.access(opts.root_path + usr_share, os.W_OK) and \
       not os.access(opts.root_path, os.W_OK):
        icons_dirname = 'icons'
        if 'XDG_DATA_HOME' in os.environ.keys():
            usr_share = os.environ['XDG_DATA_HOME']
        else:
            usr_share = os.path.expanduser('~/.local/share')
    data_files += [
        (os.path.join(usr_share, 'applications/'), ['electrum-ganja.desktop']),
        (os.path.join(usr_share, icons_dirname), ['icons/electrum_ganja.png'])
    ]

extras_require = {
    'hardware': requirements_hw,
    'fast': ['pycryptodomex'],
}
extras_require['full'] = extras_require['hardware'] + extras_require['fast']


setup(
    name="Electrum-Ganja",
    version=version.ELECTRUM_GANJA_VERSION,
    install_requires=requirements,
    extras_require=extras_require,
    packages=[
        'electrum_ganja',
        'electrum_ganja_gui',
        'electrum_ganja_gui.qt',
        'electrum_ganja_plugins',
        'electrum_ganja_plugins.audio_modem',
        'electrum_ganja_plugins.cosigner_pool',
        'electrum_ganja_plugins.email_requests',
        'electrum_ganja_plugins.greenaddress_instant',
        'electrum_ganja_plugins.hw_wallet',
        'electrum_ganja_plugins.keepkey',
        'electrum_ganja_plugins.labels',
        'electrum_ganja_plugins.ledger',
        'electrum_ganja_plugins.trezor',
        'electrum_ganja_plugins.digitalbitbox',
        'electrum_ganja_plugins.trustedcoin',
        'electrum_ganja_plugins.virtualkeyboard',
    ],
    package_dir={
        'electrum_ganja': 'lib',
        'electrum_ganja_gui': 'gui',
        'electrum_ganja_plugins': 'plugins',
    },
    package_data={
        'electrum_ganja': [
            'servers.json',
            'servers_testnet.json',
            'servers_regtest.json',
            'currencies.json',
            'checkpoints.json',
            'checkpoints_testnet.json',
            'www/index.html',
            'wordlist/*.txt',
            'locale/*/LC_MESSAGES/electrum_ganja.mo',
        ]
    },
    scripts=['electrum-ganja'],
    data_files=data_files,
    description="Lightweight Ganjacoin Wallet",
    #author="Thomas Voegtlin",
    author="GanjaProject"
    #author_email="thomasv@electrum.org",
    license="MIT Licence",
    #url="https://electrum.org",
    url="https://ganjacoinpro.com"
    long_description="""Lightweight Ganjacoin Wallet"""
)
