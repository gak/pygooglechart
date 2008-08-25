#!/usr/bin/env python

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

