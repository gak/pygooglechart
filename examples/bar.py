#!/usr/bin/env python

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

