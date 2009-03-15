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

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, '..'))

from pygooglechart import MapChart

import settings
import helper

def birth_rate():

    # Create a chart object of 200x100 pixels
    chart = MapChart(440, 220)

    # Load the data from a file, create a dict that looks like:
    # {'AU': 5, 'YE': 10}
    data = {}
    countries = open('mapchart-birth-rate.txt', 'rb').read().split('\n')
    for line in countries[:-1]:
        code, score = line.split(' ', 1)
        data[code] = float(score)

    # Set the data dictionary for country codes to value mapping
    chart.add_data_dict(data)

    # Download the chart
    chart.download('mapchart-birth-rate.png')

    # Now do it in africa ...
    chart.set_geo_area('africa')

    # ... with white as the default colour and gradient from green to red
    chart.set_colours(('EEEEEE', '10A010', 'D03000'))

    chart.download('mapchart-birth-rate-africa.png')

def main():
    birth_rate()

if __name__ == '__main__':
    main()
