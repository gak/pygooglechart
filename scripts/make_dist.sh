#!/bin/bash

rm -fr dist
python setup.py sdist --formats=gztar,zip
python setup.py bdist --formats=wininst
python setup.py register
scp dist/* slowchop.com:/var/www/slowchop.com/pygooglechart/download/

