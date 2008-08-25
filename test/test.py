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
from pygooglechart import NoDataGivenException


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


class TestDataTypes(TestBase):

    def test_simple_data(self):
        s = gc.SimpleData([range(0, 62), [0, 1, 60, 61]])
        self.assertEquals(repr(s),
            'chd=s:ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            'abcdefghijklmnopqrstuvwxyz0123456789,AB89')

    def test_text_data(self):
        s = gc.TextData([[0, 1, 99.9]])
        self.assertEquals(repr(s), 'chd=t:0.0,1.0,99.9')

    def test_ext_data(self):
        s = gc.ExtendedData([[0, 1, 4095]])
        self.assertEquals(repr(s), 'chd=e:AAAB..')


class TestScaling(TestBase):

    def test_simple_scale(self):
        sv = gc.SimpleData.scale_value

        self.raise_warnings(False)  # We know some of these give warnings
        self.assertEquals(sv(-10, [0, 1]), 0)
        self.assertEquals(sv(0, [0, 1]), 0)
        self.assertEquals(sv(.5, [0, 1]), 31)
        self.assertEquals(sv(30, [0, 1]), 61)
        self.assertEquals(sv(2222, [0, 10000]), 14)

        # Test for warnings
        self.raise_warnings(True)
        self.assertRaises(UserWarning, sv, -10, [0, 1])
        self.assertRaises(UserWarning, sv, 30, [0, 1])

    def test_text_scale(self):
        sv = gc.TextData.scale_value

        self.raise_warnings(False)
        self.assertEquals(sv(-10, [0, 1]), 0)
        self.assertEquals(sv(0, [0, 1]), 0)
        self.assertEquals(sv(.5, [0, 1]), 50)
        self.assertEquals(sv(30, [0, 1]), 100)
        self.assertEquals(sv(2222, [0, 10000]), 22.22)

        self.raise_warnings(True)
        self.assertRaises(UserWarning, sv, -10, [0, 1])
        self.assertRaises(UserWarning, sv, 30, [0, 1])

    def test_ext_scale(self):
        sv = gc.ExtendedData.scale_value

        self.raise_warnings(False)
        self.assertEquals(sv(-10, [0, 1]), 0)
        self.assertEquals(sv(0, [0, 1]), 0)
        self.assertEquals(sv(.5, [0, 1]), 2048)
        self.assertEquals(sv(30, [0, 1]), 4095)
        self.assertEquals(sv(2222, [0, 10000]), 910)

        self.raise_warnings(True)
        self.assertRaises(UserWarning, sv, -10, [0, 1])
        self.assertRaises(UserWarning, sv, 30, [0, 1])


class TestLineChart(TestBase):

    def test_none_data(self):
        chart = gc.SimpleLineChart(300, 100)
        chart.add_data([1, 2, 3, None, 5])
        self.assertChartURL(chart.get_url(), \
            '?cht=lc&chs=300x100&chd=e:AAMzZm__zM')


class TestQRChart(TestBase):

    def assertQRImage(self, chart, text):
        try:
            import PyQrcodec
        except ImportError:
            print 'PyQrCodec not installed. Can not test QR code image'
            return

        chart.download(self.temp_image)
        status, string = PyQrcodec.decode(self.temp_image)
        self.assertTrue(status)
        self.assertEquals(text, string)

    def test_simple(self):
        text = 'Hello World'
        chart = gc.QRChart(100, 150)
        chart.add_data(text)
        self.assertChartURL(chart.get_url(), \
            '?cht=qr&chs=100x150&chl=Hello%20World')

    def test_encoding(self):
        chart = gc.QRChart(100, 100)
        chart.add_data('Hello World')
        self.assertChartURL(chart.get_url(), \
            '?cht=qr&chs=100x100&chl=Hello%20World')

    def test_no_data(self):
        chart = gc.QRChart(100, 100)
        self.assertRaises(NoDataGivenException, chart.get_url)

    def test_validate_image(self):
        text = 'Hello World'
        chart = gc.QRChart(100, 100)
        chart.add_data(text)
        chart.set_ec('H', 0)  # PyQrcodec seems to only work on higher EC
        self.assertQRImage(chart, text)

    def test_validate_utf8(self):
        text = 'こんにちは世界'  # Hello world in Japanese UTF-8
        chart = gc.QRChart(100, 100)
        chart.add_data(text)
        chart.set_ec('H', 0)
        self.assertQRImage(chart, text)

    def test_validate_shift_jis(self):
        # XXX: It looks like PyQrcodec doesn't do shift_jis?
        text = unicode('こんにちは世界', 'utf-8').encode('shift_jis')
        chart = gc.QRChart(100, 100)
        chart.add_data(text)
        chart.set_ec('H', 0)
        chart.set_encoding('Shift_JIS')
        self.assertChartURL(chart.get_url(), \
            '?cht=qr&chs=100x100&chl=%82%B1%82%F1%82%C9' \
            '%82%BF%82%CD%90%A2%8AE&choe=Shift_JIS&chld=H|0')
        chart.download(self.temp_image)


class TestGrammar(TestBase):

    types = ('Venn', 'GroupedHorizontalBar', 'GoogleOMeter', 'Scatter',
        'StackedVerticalBar', 'Map', 'StackedHorizontalBar', 'SimpleLine',
        'SparkLine', 'GroupedVerticalBar', 'SplineRadar', 'XYLine', 'Radar',
        'QR')

    def test_chart_types(self):
        ret = gc.ChartGrammar.get_possible_chart_types()
        diff = set(ret).symmetric_difference(set(TestGrammar.types))
        self.assert_(not diff)

    def test_google_chart(self):
        g = {
            'type': 'GoogleOMeter',
            'w': 100,
            'h': 100,
            'auto_scale': True,
            'x_range': [ 0, 10 ],
            'data': [
                [ 1, 5, 10 ]
            ],
        }
        grammar = gc.ChartGrammar()
        chart = grammar.parse(g)
#        print chart.get_url()
#        chart.download('meh.png')


if __name__ == "__main__":
    unittest.main()

