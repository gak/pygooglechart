#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
import os
import warnings
import urllib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT)

from test.test_base import TestBase
import pygooglechart as gc


if __name__ == "__main__":
    unittest.main()

