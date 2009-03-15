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

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, '..'))

from pygooglechart import StackedHorizontalBarChart, StackedVerticalBarChart, \
    GroupedHorizontalBarChart, GroupedVerticalBarChart

import settings

def stacked_horizontal():
    chart = StackedHorizontalBarChart(settings.width, settings.height,
                                      x_range=(0, 35))
    chart.set_bar_width(10)
    chart.set_colours(['00ff00', 'ff0000'])
    chart.add_data([1,2,3,4,5])
    chart.add_data([1,4,9,16,25])
    chart.download('bar-horizontal-stacked.png')

def stacked_vertical():
    chart = StackedVerticalBarChart(settings.width, settings.height,
                                    y_range=(0, 35))
    chart.set_bar_width(10)
    chart.set_colours(['00ff00', 'ff0000'])
    chart.add_data([1,2,3,4,5])
    chart.add_data([1,4,9,16,25])
    chart.download('bar-vertical-stacked.png')

def grouped_horizontal():
    chart = GroupedHorizontalBarChart(settings.width, settings.height,
                                      x_range=(0, 35))
    chart.set_bar_width(5)
    chart.set_bar_spacing(2)
    chart.set_group_spacing(4)
    chart.set_colours(['00ff00', 'ff0000'])
    chart.add_data([1,2,3,4,5])
    chart.add_data([1,4,9,16,25])
    chart.download('bar-horizontal-grouped.png')

def grouped_vertical():
    chart = GroupedVerticalBarChart(settings.width, settings.height,
                                    y_range=(0, 35))
    chart.set_bar_width(5)
    chart.set_colours(['00ff00', 'ff0000'])
    chart.add_data([1,2,3,4,5])
    chart.add_data([1,4,9,16,25])
    chart.download('bar-vertical-grouped.png')


def main():
    stacked_horizontal()
    stacked_vertical()
    grouped_horizontal()
    grouped_vertical()

if __name__ == '__main__':
    main()

