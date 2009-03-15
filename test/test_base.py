#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
import os
import warnings
import urllib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT)

import pygooglechart as gc


class TestBase(unittest.TestCase):

    def setUp(self):

        # All tests require warnings to be raised
        self.raise_warnings(True)

        self.temp_image = 'temp.png'

    def tearDown(self):
        if os.path.exists(self.temp_image):
            os.unlink(self.temp_image)

    def raise_warnings(self, rw):
        gc._reset_warnings()

        if rw:
            warnings.simplefilter('error')
        else:
            # Don't print out warnings if we're expecting them--so we can have
            # nicer looking tests! :)
            warnings.simplefilter('ignore')

    def assertChartURL(self, url, query):
        self.assertTrue(url.endswith(query))



