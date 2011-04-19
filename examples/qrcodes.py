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

from pygooglechart import QRChart

import settings
import helper

def hello():

    # Create a 250x250 QR chart
    chart = QRChart(250, 250)

    # Add the text
    chart.add_data('Hello, World!')

    # "Level H" error correction with a 0 pixel margin
    chart.set_ec('H', 0)

    # Download
    chart.download('qr-hello.png')

def main():
    hello()

if __name__ == '__main__':
    main()

