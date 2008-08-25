#!/usr/bin/env python

import os
import sys
import math

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, '..'))

from pygooglechart import SimpleLineChart
from pygooglechart import XYLineChart
from pygooglechart import SparkLineChart
from pygooglechart import Axis

import settings
import helper

def simple_random():
    chart = SimpleLineChart(settings.width, settings.height, y_range=(0, 100))
    chart.add_data(helper.random_data())
    chart.download('line-simple-random.png')

def xy_random():
    chart = XYLineChart(settings.width, settings.height,
                        x_range=(0, 100), y_range=(0, 100))
    chart.add_data(helper.random_data())
    chart.add_data(helper.random_data())
    chart.download('line-xy-random.png')

def xy_rect():
    chart = XYLineChart(settings.width, settings.height,
                        x_range=(0, 100), y_range=(0, 100))
    chart.add_data([10, 90, 90, 10, 10])
    chart.add_data([10, 10, 90, 90, 10])
    chart.download('line-xy-rect.png')

def xy_circle():
    chart = XYLineChart(settings.width, settings.height,
                        x_range=(0, 100), y_range=(0, 100))
    steps = 40
    xradius = 25
    yradius = 45
    xmid = 50
    ymid = 50
    xlist = []
    ylist = []
    for angle in xrange(0, steps + 1):
        angle = float(angle) / steps * math.pi * 2
        xlist.append(math.cos(angle) * xradius + xmid)
        ylist.append(math.sin(angle) * yradius + ymid)
    chart.add_data(xlist)
    chart.add_data(ylist)
    chart.download('line-xy-circle.png')

def sparklines():
    chart = SparkLineChart(settings.width, settings.height)
    chart.add_data(helper.random_data())
    chart.download('line-sparkline.png')

def fill():

    # Set the vertical range to 0 to 50
    max_y = 50
    chart = SimpleLineChart(200, 125, y_range=[0, max_y])

    # First value is the highest Y value. Two of them are needed to be
    # plottable.
    chart.add_data([max_y] * 2)

    # 3 sets of real data
    chart.add_data([28, 30, 31, 33, 35, 36, 42, 48, 43, 37, 32, 24, 28])
    chart.add_data([16, 18, 18, 21, 23, 23, 29, 36, 31, 25, 20, 12, 17])
    chart.add_data([7, 9, 9, 12, 14, 14, 20, 27, 21, 15, 10, 3, 7])

    # Last value is the lowest in the Y axis.
    chart.add_data([0] * 2)

    # Black lines
    chart.set_colours(['000000'] * 5)

    # Filled colours
    # from the top to the first real data
    chart.add_fill_range('76A4FB', 0, 1)

    # Between the 3 data values
    chart.add_fill_range('224499', 1, 2)
    chart.add_fill_range('FF0000', 2, 3)
    
    # from the last real data to the
    chart.add_fill_range('80C65A', 3, 4)

    # Some axis data
    chart.set_axis_labels(Axis.LEFT, ['', max_y / 2, max_y])
    chart.set_axis_labels(Axis.BOTTOM, ['Sep', 'Oct', 'Nov', 'Dec'])

    chart.download('line-fill.png')

def main():
    simple_random()
    xy_random()
    xy_rect()
    xy_circle()
    sparklines()
    fill()

if __name__ == '__main__':
    main()

