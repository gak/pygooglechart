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

import random

def random_data(points=50, maximum=100):
    return [random.random() * maximum for a in xrange(points)]

def random_colour(min=20, max=200):
    func = lambda: int(random.random() * (max-min) + min)
    r, g, b = func(), func(), func()
    return '%02X%02X%02X' % (r, g, b)

