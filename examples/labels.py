#!/usr/bin/env python
"""
Copyright Gerald Kaszuba 2008

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
import math
import random

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, '..'))

from pygooglechart import SimpleLineChart
from pygooglechart import Axis

import settings
import helper

def cat_proximity():
    """Cat proximity graph from http://xkcd.com/231/"""
    chart = SimpleLineChart(int(settings.width * 1.5), settings.height)
    chart.set_legend(['INTELLIGENCE', 'INSANITY OF STATEMENTS'])

    # intelligence
    data_index = chart.add_data([100. / y for y in xrange(1, 15)])

    # insanity of statements
    chart.add_data([100. - 100 / y for y in xrange(1, 15)])

    # line colours
    chart.set_colours(['208020', '202080'])

    # "Near" and "Far" labels, they are placed automatically at either ends.
    near_far_axis_index = chart.set_axis_labels(Axis.BOTTOM, ['FAR', 'NEAR'])

    # "Human Proximity to cat" label. Aligned to the center.
    index = chart.set_axis_labels(Axis.BOTTOM, ['HUMAN PROXIMITY TO CAT'])
    chart.set_axis_style(index, '202020', font_size=10, alignment=0)
    chart.set_axis_positions(index, [50])

    chart.download('label-cat-proximity.png')

def many_labels():
    chart = SimpleLineChart(settings.width, settings.height)

    for a in xrange(3):
        for axis_type in (Axis.LEFT, Axis.RIGHT, Axis.BOTTOM):
            index = chart.set_axis_range(axis_type, 0, random.random() * 100)
            chart.set_axis_style(index, colour=helper.random_colour(), \
                font_size=random.random() * 10 + 5)

    chart.add_data(helper.random_data())
    chart.download('label-many.png')

def main():
    cat_proximity()
    many_labels()

if __name__ == '__main__':
    main()

