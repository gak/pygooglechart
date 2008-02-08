#!/usr/bin/env python

import os
import sys
import math

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, '..'))

from pygooglechart import ScatterChart

import settings
import helper

def scatter_random():
    chart = ScatterChart(settings.width, settings.height, 
                         x_range=(0, 100), y_range=(0, 100))
    chart.add_data(helper.random_data())
    chart.add_data(helper.random_data())
    chart.download('scatter-random.png')

def scatter_random_marker_sizes():
    chart = ScatterChart(settings.width, settings.height, 
                         x_range=(0, 100), y_range=(0, 100))
    chart.add_data(helper.random_data())
    chart.add_data(helper.random_data())
    chart.add_data(helper.random_data())
    chart.download('scatter-random-marker-sizes.png')

def scatter_circle():
    chart = ScatterChart(settings.width, settings.height, 
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
    chart.add_data(range(len(ylist)))
    chart.add_marker(0, 1.0, 'o', '00ff00', 10)
    chart.download('scatter-circle.png')

def main():
    scatter_random()
    scatter_random_marker_sizes()
    scatter_circle()

if __name__ == '__main__':
    main()

