#!/bin/bash

NAME_ROOT=electrum-ganja
PYTHON_VERSION=3.5.4

# These settings probably don't need any change
export WINEPREFIX=/opt/wine64
export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=22

PYHOME=c:/python$PYTHON_VERSION
PYTHON="wine $PYHOME/python.exe -OO -B"


# Let's begin!
cd `dirname $0`
set -e

mkdir -p tmp
cd tmp

if [ -d ./electrum-ganja ]; then
  rm ./electrum-ganja -rf
fi

git clone https://github.com/D3m0nKingx/electrum-ganja -b master

pushd electrum-ganja
if [ ! -z "$1" ]; then
    # a commit/tag/branch was specified
    if ! git cat-file -e "$1" 2> /dev/null
    then  # can't find target
        # try pull requests
        git config --local --add remote.origin.fetch '+refs/pull/*/merge:refs/remotes/origin/pr/*'
        git fetch --all
    fi
    git checkout $1
fi

# Load electrum-ganja-icons and electrum-ganja-locale for this release
git submodule init
git submodule update

pushd ./contrib/deterministic-build/electrum-ganja-locale
for i in ./locale/*; do
    dir=$i/LC_MESSAGES
    mkdir -p $dir
    msgfmt --output-file=$dir/electrum-ganja.mo $i/electrum-ganja.po || true
done
popd

VERSION=`git describe --tags --dirty`
echo "Last commit: $VERSION"
find -exec touch -d '2000-11-11T11:11:11+00:00' {} +
popd

rm -rf $WINEPREFIX/drive_c/electrum-ganja
cp -r electrum-ganja $WINEPREFIX/drive_c/electrum-ganja
cp electrum-ganja/LICENCE .
cp -r ./electrum-ganja/contrib/deterministic-build/electrum-ganja-locale/locale $WINEPREFIX/drive_c/electrum-ganja/lib/
cp ./electrum-ganja/contrib/deterministic-build/electrum-ganja-icons/icons_rc.py $WINEPREFIX/drive_c/electrum-ganja/gui/qt/

# Install frozen dependencies
$PYTHON -m pip install -r ../../deterministic-build/requirements.txt

$PYTHON -m pip install -r ../../deterministic-build/requirements-hw.txt

pushd $WINEPREFIX/drive_c/electrum-ganja
$PYTHON setup.py install
popd

cd ..

rm -rf dist/

# build standalone and portable versions
wine "C:/python$PYTHON_VERSION/scripts/pyinstaller.exe" --noconfirm --ascii --name $NAME_ROOT-$VERSION -w deterministic.spec

# set timestamps in dist, in order to make the installer reproducible
pushd dist
find -exec touch -d '2000-11-11T11:11:11+00:00' {} +
popd

# build NSIS installer
# $VERSION could be passed to the electrum-ganja.nsi script, but this would require some rewriting in the script itself.
wine "$WINEPREFIX/drive_c/Program Files (x86)/NSIS/makensis.exe" /DPRODUCT_VERSION=$VERSION electrum-ganja.nsi

cd dist
mv electrum-ganja-setup.exe $NAME_ROOT-$VERSION-setup.exe
cd ..

echo "Done."
md5sum dist/electrum-ganja*exe
