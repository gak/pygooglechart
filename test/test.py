import unittest
import sys
import os
import warnings

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT)

import pygooglechart as gc


class TestBase(unittest.TestCase):

    def setUp(self):

        # All tests require warnings to be raised
        self.raise_warnings(True)

    def raise_warnings(self, rw):
        gc._reset_warnings()

        if rw:
            warnings.simplefilter('error')
        else:
            # Don't print out warnings if we're expecting them--so we can have
            # nicer looking tests! :)
            warnings.simplefilter('ignore')

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
        sv(-10, [0, 1])
#        self.assertRaises(UserWarning, sv, -10, [0, 1])
#        self.assertEquals(UserWarning, sv, 30, [0, 1])

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

class TestGrammar(TestBase):

    types = ('Venn', 'GroupedHorizontalBar', 'GoogleOMeter', 'Scatter',
        'StackedVerticalBar', 'Map', 'StackedHorizontalBar', 'SimpleLine',
        'SparkLine', 'GroupedVerticalBar', 'SplineRadar', 'XYLine', 'Radar')

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
        print chart.get_url()
#        chart.download('meh.png')


if __name__ == "__main__":
    unittest.main()

    suite = unittest.TestSuite()
    suite.addTest(TestScaling('test_ext_scale'))
    unittest.TextTestRunner().run(suite)

