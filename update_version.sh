#!/bin/bash

echo $1 > .version
echo -ne "from .instrumentmanager import RemoteInstrument\n__version__ = '$1'\n" > pyvisaserver/__init__.py

rm -r build
rm -r dist
rm -r shgpy.egg.info

python setup.py sdist bdist_wheel

cd docsrc
./make_docsrc.sh
./make_ghpages.sh
