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

from pygooglechart import VennChart

import settings
import helper

def ultimate_power():
    """
    Data from http://indexed.blogspot.com/2007/08/real-ultimate-power.html
    """
    chart = VennChart(settings.width, settings.height)
    chart.add_data([100, 100, 100, 20, 20, 20, 10])
    chart.set_title('Ninjas or God')
    chart.set_legend(['unseen agents', 'super powerful', 'secret plans'])
    chart.download('venn-ultimate-power.png')

def main():
    ultimate_power()

if __name__ == '__main__':
    main()


