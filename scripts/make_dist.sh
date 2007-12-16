#!/bin/bash

python setup.py sdist --formats=gztar,zip
python setup.py bdist --formats=wininst
python setup.py register

