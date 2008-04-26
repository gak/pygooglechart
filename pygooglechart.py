"""
PyGoogleChart - A complete Python wrapper for the Google Chart API

http://pygooglechart.slowchop.com/

Copyright 2007 Gerald Kaszuba

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
import urllib
import urllib2
import math
import random
import re

# Helper variables and functions
# -----------------------------------------------------------------------------

__version__ = '0.2.0'

reo_colour = re.compile('^([A-Fa-f0-9]{2,2}){3,4}$')


def _check_colour(colour):
    if not reo_colour.match(colour):
        raise InvalidParametersException('Colours need to be in ' \
            'RRGGBB or RRGGBBAA format. One of your colours has %s' % \
            colour)

# Exception Classes
# -----------------------------------------------------------------------------


class PyGoogleChartException(Exception):
    pass


class DataOutOfRangeException(PyGoogleChartException):
    pass


class UnknownDataTypeException(PyGoogleChartException):
    pass


class NoDataGivenException(PyGoogleChartException):
    pass


class InvalidParametersException(PyGoogleChartException):
    pass


class BadContentTypeException(PyGoogleChartException):
    pass


# Data Classes
# -----------------------------------------------------------------------------


class Data(object):

    def __init__(self, data):
        assert(type(self) != Data)  # This is an abstract class
        self.data = data

    @classmethod
    def float_scale_value(cls, value, range):
        lower, upper = range
        max_value = cls.max_value()
        scaled = (value-lower) * (float(max_value)/(upper-lower))
        return scaled

    @classmethod
    def clip_value(cls, value):
        clipped = max(0, min(value, cls.max_value()))
        return clipped

    @classmethod
    def int_scale_value(cls, value, range):
        scaled = int(round(cls.float_scale_value(value, range)))
        return scaled

    @classmethod
    def scale_value(cls, value, range):
        scaled = cls.int_scale_value(value, range)
        clipped = cls.clip_value(scaled)
        return clipped

class SimpleData(Data):
    enc_map = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    def __repr__(self):
        max_value = self.max_value()
        encoded_data = []
        for data in self.data:
            sub_data = []
            for value in data:
                if value is None:
                    sub_data.append('_')
                elif value >= 0 and value <= max_value:
                    sub_data.append(SimpleData.enc_map[value])
                else:
                    raise DataOutOfRangeException('cannot encode value: %d'
                                                  % value)
            encoded_data.append(''.join(sub_data))
        return 'chd=s:' + ','.join(encoded_data)

    @staticmethod
    def max_value():
        return 61

class TextData(Data):

    def __repr__(self):
        max_value = self.max_value()
        encoded_data = []
        for data in self.data:
            sub_data = []
            for value in data:
                if value is None:
                    sub_data.append(-1)
                elif value >= 0 and value <= max_value:
                    sub_data.append("%.1f" % float(value))
                else:
                    raise DataOutOfRangeException()
            encoded_data.append(','.join(sub_data))
        return 'chd=t:' + '|'.join(encoded_data)

    @staticmethod
    def max_value():
        return 100

    @classmethod
    def scale_value(cls, value, range):
        lower, upper = range
        if upper > lower:
            max_value = cls.max_value()
            scaled = (float(value) - lower) * max_value / upper
            clipped = max(0, min(scaled, max_value))
            return clipped
        else:
            return lower

    @classmethod
    def scale_value(cls, value, range):
        # use float values instead of integers because we don't need an encode
        # map index
        scaled = cls.float_scale_value(value,range)
        clipped = cls.clip_value(scaled)
        return clipped

class ExtendedData(Data):
    enc_map = \
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-.'

    def __repr__(self):
        max_value = self.max_value()
        encoded_data = []
        enc_size = len(ExtendedData.enc_map)
        for data in self.data:
            sub_data = []
            for value in data:
                if value is None:
                    sub_data.append('__')
                elif value >= 0 and value <= max_value:
                    first, second = divmod(int(value), enc_size)
                    sub_data.append('%s%s' % (
                        ExtendedData.enc_map[first],
                        ExtendedData.enc_map[second]))
                else:
                    raise DataOutOfRangeException( \
                        'Item #%i "%s" is out of range' % (data.index(value), \
                        value))
            encoded_data.append(''.join(sub_data))
        return 'chd=e:' + ','.join(encoded_data)

    @staticmethod
    def max_value():
        return 4095


# Axis Classes
# -----------------------------------------------------------------------------


class Axis(object):
    BOTTOM = 'x'
    TOP = 't'
    LEFT = 'y'
    RIGHT = 'r'
    TYPES = (BOTTOM, TOP, LEFT, RIGHT)

    def __init__(self, axis_index, axis_type, **kw):
        assert(axis_type in Axis.TYPES)
        self.has_style = False
        self.axis_index = axis_index
        self.axis_type = axis_type
        self.positions = None

    def set_index(self, axis_index):
        self.axis_index = axis_index

    def set_positions(self, positions):
        self.positions = positions

    def set_style(self, colour, font_size=None, alignment=None):
        _check_colour(colour)
        self.colour = colour
        self.font_size = font_size
        self.alignment = alignment
        self.has_style = True

    def style_to_url(self):
        bits = []
        bits.append(str(self.axis_index))
        bits.append(self.colour)
        if self.font_size is not None:
            bits.append(str(self.font_size))
            if self.alignment is not None:
                bits.append(str(self.alignment))
        return ','.join(bits)

    def positions_to_url(self):
        bits = []
        bits.append(str(self.axis_index))
        bits += [str(a) for a in self.positions]
        return ','.join(bits)


class LabelAxis(Axis):

    def __init__(self, axis_index, axis_type, values, **kwargs):
        Axis.__init__(self, axis_index, axis_type, **kwargs)
        self.values = [str(a) for a in values]

    def __repr__(self):
        return '%i:|%s' % (self.axis_index, '|'.join(self.values))


class RangeAxis(Axis):

    def __init__(self, axis_index, axis_type, low, high, **kwargs):
        Axis.__init__(self, axis_index, axis_type, **kwargs)
        self.low = low
        self.high = high

    def __repr__(self):
        return '%i,%s,%s' % (self.axis_index, self.low, self.high)

# Chart Classes
# -----------------------------------------------------------------------------


class Chart(object):
    """Abstract class for all chart types.

    width are height specify the dimensions of the image. title sets the title
    of the chart. legend requires a list that corresponds to datasets.
    """

    BASE_URL = 'http://chart.apis.google.com/chart?'
    BACKGROUND = 'bg'
    CHART = 'c'
    ALPHA = 'a'
    VALID_SOLID_FILL_TYPES = (BACKGROUND, CHART, ALPHA)
    SOLID = 's'
    LINEAR_GRADIENT = 'lg'
    LINEAR_STRIPES = 'ls'

    def __init__(self, width, height, title=None, legend=None, colours=None,
                 auto_scale=True, x_range=None, y_range=None):
        assert(type(self) != Chart)  # This is an abstract class
        assert(isinstance(width, int))
        assert(isinstance(height, int))
        self.width = width
        self.height = height
        self.data = []
        self.set_title(title)
        self.set_legend(legend)
        self.set_colours(colours)

        # Data for scaling.
        self.auto_scale = auto_scale    # Whether to automatically scale data
        self.x_range = x_range          # (min, max) x-axis range for scaling
        self.y_range = y_range          # (min, max) y-axis range for scaling
        self.scaled_data_class = None
        self.scaled_x_range = None
        self.scaled_y_range = None

        self.fill_types = {
            Chart.BACKGROUND: None,
            Chart.CHART: None,
            Chart.ALPHA: None,
        }
        self.fill_area = {
            Chart.BACKGROUND: None,
            Chart.CHART: None,
            Chart.ALPHA: None,
        }
        self.axis = []
        self.markers = []
        self.line_styles = {}
        self.grid = None

    # URL generation
    # -------------------------------------------------------------------------

    def get_url(self, data_class=None):
        url_bits = self.get_url_bits(data_class=data_class)
        return self.BASE_URL + '&'.join(url_bits)

    def get_url_bits(self, data_class=None):
        url_bits = []
        # required arguments
        url_bits.append(self.type_to_url())
        url_bits.append('chs=%ix%i' % (self.width, self.height))
        url_bits.append(self.data_to_url(data_class=data_class))
        # optional arguments
        if self.title:
            url_bits.append('chtt=%s' % self.title)
        if self.legend:
            url_bits.append('chdl=%s' % '|'.join(self.legend))
        if self.colours:
            url_bits.append('chco=%s' % ','.join(self.colours))
        ret = self.fill_to_url()
        if ret:
            url_bits.append(ret)
        ret = self.axis_to_url()
        if ret:
            url_bits.append(ret)
        if self.markers:
            url_bits.append(self.markers_to_url())
        if self.line_styles:
            style = []
            for index in xrange(max(self.line_styles) + 1):
                if index in self.line_styles:
                    values = self.line_styles[index]
                else:
                    values = ('1', )
                style.append(','.join(values))
            url_bits.append('chls=%s' % '|'.join(style))
        if self.grid:
            url_bits.append('chg=%s' % self.grid)
        return url_bits

    # Downloading
    # -------------------------------------------------------------------------

    def download(self, file_name):
        opener = urllib2.urlopen(self.get_url())

        if opener.headers['content-type'] != 'image/png':
            raise BadContentTypeException('Server responded with a ' \
                'content-type of %s' % opener.headers['content-type'])

        open(file_name, 'wb').write(urllib.urlopen(self.get_url()).read())

    # Simple settings
    # -------------------------------------------------------------------------

    def set_title(self, title):
        if title:
            self.title = urllib.quote(title)
        else:
            self.title = None

    def set_legend(self, legend):
        """legend needs to be a list, tuple or None"""
        assert(isinstance(legend, list) or isinstance(legend, tuple) or
            legend is None)
        if legend:
            self.legend = [urllib.quote(a) for a in legend]
        else:
            self.legend = None

    # Chart colours
    # -------------------------------------------------------------------------

    def set_colours(self, colours):
        # colours needs to be a list, tuple or None
        assert(isinstance(colours, list) or isinstance(colours, tuple) or
            colours is None)
        # make sure the colours are in the right format
        if colours:
            for col in colours:
                _check_colour(col)
        self.colours = colours

    # Background/Chart colours
    # -------------------------------------------------------------------------

    def fill_solid(self, area, colour):
        assert(area in Chart.VALID_SOLID_FILL_TYPES)
        _check_colour(colour)
        self.fill_area[area] = colour
        self.fill_types[area] = Chart.SOLID

    def _check_fill_linear(self, angle, *args):
        assert(isinstance(args, list) or isinstance(args, tuple))
        assert(angle >= 0 and angle <= 90)
        assert(len(args) % 2 == 0)
        args = list(args)  # args is probably a tuple and we need to mutate
        for a in xrange(len(args) / 2):
            col = args[a * 2]
            offset = args[a * 2 + 1]
            _check_colour(col)
            assert(offset >= 0 and offset <= 1)
            args[a * 2 + 1] = str(args[a * 2 + 1])
        return args

    def fill_linear_gradient(self, area, angle, *args):
        assert(area in Chart.VALID_SOLID_FILL_TYPES)
        args = self._check_fill_linear(angle, *args)
        self.fill_types[area] = Chart.LINEAR_GRADIENT
        self.fill_area[area] = ','.join([str(angle)] + args)

    def fill_linear_stripes(self, area, angle, *args):
        assert(area in Chart.VALID_SOLID_FILL_TYPES)
        args = self._check_fill_linear(angle, *args)
        self.fill_types[area] = Chart.LINEAR_STRIPES
        self.fill_area[area] = ','.join([str(angle)] + args)

    def fill_to_url(self):
        areas = []
        for area in (Chart.BACKGROUND, Chart.CHART, Chart.ALPHA):
            if self.fill_types[area]:
                areas.append('%s,%s,%s' % (area, self.fill_types[area], \
                    self.fill_area[area]))
        if areas:
            return 'chf=' + '|'.join(areas)

    # Data
    # -------------------------------------------------------------------------

    def data_class_detection(self, data):
        """Determines the appropriate data encoding type to give satisfactory
        resolution (http://code.google.com/apis/chart/#chart_data).
        """
        assert(isinstance(data, list) or isinstance(data, tuple))
        if not isinstance(self, (LineChart, BarChart, ScatterChart)):
            # From the link above:
            #   Simple encoding is suitable for all other types of chart
            #   regardless of size.
            return SimpleData
        elif self.height < 100:
            # The link above indicates that line and bar charts less
            # than 300px in size can be suitably represented with the
            # simple encoding. I've found that this isn't sufficient,
            # e.g. examples/line-xy-circle.png. Let's try 100px.
            return SimpleData
        else:
            return ExtendedData

    def data_x_range(self):
        """Return a 2-tuple giving the minimum and maximum x-axis
        data range.
        """
        try:
            lower = min([min(s) for type, s in self.annotated_data()
                         if type == 'x'])
            upper = max([max(s) for type, s in self.annotated_data()
                         if type == 'x'])
            return (lower, upper)
        except ValueError:
            return None     # no x-axis datasets

    def data_y_range(self):
        """Return a 2-tuple giving the minimum and maximum y-axis
        data range.
        """
        try:
            lower = min([min(s) for type, s in self.annotated_data()
                         if type == 'y'])
            upper = max([max(s) for type, s in self.annotated_data()
                         if type == 'y'])
            return (lower, upper)
        except ValueError:
            return None     # no y-axis datasets

    def scaled_data(self, data_class, x_range=None, y_range=None):
        """Scale `self.data` as appropriate for the given data encoding
        (data_class) and return it.

        An optional `y_range` -- a 2-tuple (lower, upper) -- can be
        given to specify the y-axis bounds. If not given, the range is
        inferred from the data: (0, <max-value>) presuming no negative
        values, or (<min-value>, <max-value>) if there are negative
        values.  `self.scaled_y_range` is set to the actual lower and
        upper scaling range.

        Ditto for `x_range`. Note that some chart types don't have x-axis
        data.
        """
        self.scaled_data_class = data_class

        # Determine the x-axis range for scaling.
        if x_range is None:
            x_range = self.data_x_range()
            if x_range and x_range[0] > 0:
                x_range = (0, x_range[1])
        self.scaled_x_range = x_range

        # Determine the y-axis range for scaling.
        if y_range is None:
            y_range = self.data_y_range()
            if y_range and y_range[0] > 0:
                y_range = (0, y_range[1])
        self.scaled_y_range = y_range

        scaled_data = []
        for type, dataset in self.annotated_data():
            if type == 'x':
                scale_range = x_range
            elif type == 'y':
                scale_range = y_range
            elif type == 'marker-size':
                scale_range = (0, max(dataset))
            scaled_data.append([data_class.scale_value(v, scale_range)
                                for v in dataset])
        return scaled_data

    def add_data(self, data):
        self.data.append(data)
        return len(self.data) - 1  # return the "index" of the data set

    def data_to_url(self, data_class=None):
        if not data_class:
            data_class = self.data_class_detection(self.data)
        if not issubclass(data_class, Data):
            raise UnknownDataTypeException()
        if self.auto_scale:
            data = self.scaled_data(data_class, self.x_range, self.y_range)
        else:
            data = self.data
        return repr(data_class(data))

    def annotated_data(self):
        for dataset in self.data:
            yield ('x', dataset)

    # Axis Labels
    # -------------------------------------------------------------------------

    def set_axis_labels(self, axis_type, values):
        assert(axis_type in Axis.TYPES)
        values = [ urllib.quote(a) for a in values ]
        axis_index = len(self.axis)
        axis = LabelAxis(axis_index, axis_type, values)
        self.axis.append(axis)
        return axis_index

    def set_axis_range(self, axis_type, low, high):
        assert(axis_type in Axis.TYPES)
        axis_index = len(self.axis)
        axis = RangeAxis(axis_index, axis_type, low, high)
        self.axis.append(axis)
        return axis_index

    def set_axis_positions(self, axis_index, positions):
        try:
            self.axis[axis_index].set_positions(positions)
        except IndexError:
            raise InvalidParametersException('Axis index %i has not been ' \
                'created' % axis)

    def set_axis_style(self, axis_index, colour, font_size=None, \
            alignment=None):
        try:
            self.axis[axis_index].set_style(colour, font_size, alignment)
        except IndexError:
            raise InvalidParametersException('Axis index %i has not been ' \
                'created' % axis)

    def axis_to_url(self):
        available_axis = []
        label_axis = []
        range_axis = []
        positions = []
        styles = []
        index = -1
        for axis in self.axis:
            available_axis.append(axis.axis_type)
            if isinstance(axis, RangeAxis):
                range_axis.append(repr(axis))
            if isinstance(axis, LabelAxis):
                label_axis.append(repr(axis))
            if axis.positions:
                positions.append(axis.positions_to_url())
            if axis.has_style:
                styles.append(axis.style_to_url())
        if not available_axis:
            return
        url_bits = []
        url_bits.append('chxt=%s' % ','.join(available_axis))
        if label_axis:
            url_bits.append('chxl=%s' % '|'.join(label_axis))
        if range_axis:
            url_bits.append('chxr=%s' % '|'.join(range_axis))
        if positions:
            url_bits.append('chxp=%s' % '|'.join(positions))
        if styles:
            url_bits.append('chxs=%s' % '|'.join(styles))
        return '&'.join(url_bits)

    # Markers, Ranges and Fill area (chm)
    # -------------------------------------------------------------------------

    def markers_to_url(self):
        return 'chm=%s' % '|'.join([','.join(a) for a in self.markers])

    def add_marker(self, index, point, marker_type, colour, size, priority=0):
        self.markers.append((marker_type, colour, str(index), str(point), \
            str(size), str(priority)))

    def add_horizontal_range(self, colour, start, stop):
        self.markers.append(('r', colour, '1', str(start), str(stop)))

    def add_vertical_range(self, colour, start, stop):
        self.markers.append(('R', colour, '1', str(start), str(stop)))

    def add_fill_range(self, colour, index_start, index_end):
        self.markers.append(('b', colour, str(index_start), str(index_end), \
            '1'))

    def add_fill_simple(self, colour):
        self.markers.append(('B', colour, '1', '1', '1'))

    # Line styles
    # -------------------------------------------------------------------------

    def set_line_style(self, index, thickness=1, line_segment=None, \
            blank_segment=None):
        value = []
        value.append(str(thickness))
        if line_segment:
            value.append(str(line_segment))
            value.append(str(blank_segment))
        self.line_styles[index] = value

    # Grid
    # -------------------------------------------------------------------------

    def set_grid(self, x_step, y_step, line_segment=1, \
            blank_segment=0):
        self.grid = '%s,%s,%s,%s' % (x_step, y_step, line_segment, \
            blank_segment)


class ScatterChart(Chart):

    def type_to_url(self):
        return 'cht=s'

    def annotated_data(self):
        yield ('x', self.data[0])
        yield ('y', self.data[1])
        if len(self.data) > 2:
            # The optional third dataset is relative sizing for point
            # markers.
            yield ('marker-size', self.data[2])

class LineChart(Chart):

    def __init__(self, *args, **kwargs):
        assert(type(self) != LineChart)  # This is an abstract class
        Chart.__init__(self, *args, **kwargs)

#    def get_url_bits(self, data_class=None):
#        url_bits = Chart.get_url_bits(self, data_class=data_class)
#        return url_bits


class SimpleLineChart(LineChart):

    def type_to_url(self):
        return 'cht=lc'

    def annotated_data(self):
        # All datasets are y-axis data.
        for dataset in self.data:
            yield ('y', dataset)

class SparkLineChart(SimpleLineChart):

    def type_to_url(self):
        return 'cht=ls'

class XYLineChart(LineChart):

    def type_to_url(self):
        return 'cht=lxy'

    def annotated_data(self):
        # Datasets alternate between x-axis, y-axis.
        for i, dataset in enumerate(self.data):
            if i % 2 == 0:
                yield ('x', dataset)
            else:
                yield ('y', dataset)

class BarChart(Chart):

    def __init__(self, *args, **kwargs):
        assert(type(self) != BarChart)  # This is an abstract class
        Chart.__init__(self, *args, **kwargs)
        self.bar_width = None
        self.zero_lines = {}

    def set_bar_width(self, bar_width):
        self.bar_width = bar_width

    def set_zero_line(self, index, zero_line):
        self.zero_lines[index] = zero_line

    def get_url_bits(self, data_class=None, skip_chbh=False):
        url_bits = Chart.get_url_bits(self, data_class=data_class)
        if not skip_chbh and self.bar_width is not None:
            url_bits.append('chbh=%i' % self.bar_width)
        zero_line = []
        if self.zero_lines:
            for index in xrange(max(self.zero_lines) + 1):
                if index in self.zero_lines:
                    zero_line.append(str(self.zero_lines[index]))
                else:
                    zero_line.append('0')
            url_bits.append('chp=%s' % ','.join(zero_line))
        return url_bits


class StackedHorizontalBarChart(BarChart):

    def type_to_url(self):
        return 'cht=bhs'


class StackedVerticalBarChart(BarChart):

    def type_to_url(self):
        return 'cht=bvs'

    def annotated_data(self):
        for dataset in self.data:
            yield ('y', dataset)


class GroupedBarChart(BarChart):

    def __init__(self, *args, **kwargs):
        assert(type(self) != GroupedBarChart)  # This is an abstract class
        BarChart.__init__(self, *args, **kwargs)
        self.bar_spacing = None
        self.group_spacing = None

    def set_bar_spacing(self, spacing):
        """Set spacing between bars in a group."""
        self.bar_spacing = spacing

    def set_group_spacing(self, spacing):
        """Set spacing between groups of bars."""
        self.group_spacing = spacing

    def get_url_bits(self, data_class=None):
        # Skip 'BarChart.get_url_bits' and call Chart directly so the parent
        # doesn't add "chbh" before we do.
        url_bits = BarChart.get_url_bits(self, data_class=data_class,
            skip_chbh=True)
        if self.group_spacing is not None:
            if self.bar_spacing is None:
                raise InvalidParametersException('Bar spacing is required to ' \
                    'be set when setting group spacing')
            if self.bar_width is None:
                raise InvalidParametersException('Bar width is required to ' \
                    'be set when setting bar spacing')
            url_bits.append('chbh=%i,%i,%i'
                % (self.bar_width, self.bar_spacing, self.group_spacing))
        elif self.bar_spacing is not None:
            if self.bar_width is None:
                raise InvalidParametersException('Bar width is required to ' \
                    'be set when setting bar spacing')
            url_bits.append('chbh=%i,%i' % (self.bar_width, self.bar_spacing))
        elif self.bar_width:
            url_bits.append('chbh=%i' % self.bar_width)
        return url_bits


class GroupedHorizontalBarChart(GroupedBarChart):

    def type_to_url(self):
        return 'cht=bhg'


class GroupedVerticalBarChart(GroupedBarChart):

    def type_to_url(self):
        return 'cht=bvg'

    def annotated_data(self):
        for dataset in self.data:
            yield ('y', dataset)


class PieChart(Chart):

    def __init__(self, *args, **kwargs):
        assert(type(self) != PieChart)  # This is an abstract class
        Chart.__init__(self, *args, **kwargs)
        self.pie_labels = []

    def set_pie_labels(self, labels):
        self.pie_labels = [urllib.quote(a) for a in labels]

    def get_url_bits(self, data_class=None):
        url_bits = Chart.get_url_bits(self, data_class=data_class)
        if self.pie_labels:
            url_bits.append('chl=%s' % '|'.join(self.pie_labels))
        return url_bits

    def annotated_data(self):
        # Datasets are all y-axis data. However, there should only be
        # one dataset for pie charts.
        for dataset in self.data:
            yield ('y', dataset)


class PieChart2D(PieChart):

    def type_to_url(self):
        return 'cht=p'


class PieChart3D(PieChart):

    def type_to_url(self):
        return 'cht=p3'


class VennChart(Chart):

    def type_to_url(self):
        return 'cht=v'

    def annotated_data(self):
        for dataset in self.data:
            yield ('y', dataset)


class RadarChart(Chart):

    def type_to_url(self):
        return 'cht=r'

class SplineRadarChart(RadarChart):

    def type_to_url(self):
        return 'cht=rs'


class MapChart(Chart):

    def __init__(self, *args, **kwargs):
        Chart.__init__(self, *args, **kwargs)
        self.geo_area = 'world'
        self.codes = []

    def type_to_url(self):
        return 'cht=t'

    def set_codes(self, codes):
        self.codes = codes

    def get_url_bits(self, data_class=None):
        url_bits = Chart.get_url_bits(self, data_class=data_class)
        url_bits.append('chtm=%s' % self.geo_area)
        if self.codes:
            url_bits.append('chld=%s' % ''.join(self.codes))
        return url_bits


class GoogleOMeterChart(PieChart):
    """Inheriting from PieChart because of similar labeling"""

    def type_to_url(self):
        return 'cht=gom'


def test():
    chart = PieChart2D(320, 200)
    chart = ScatterChart(320, 200)
    chart = SimpleLineChart(320, 200)
    chart = GroupedVerticalBarChart(320, 200)
#    chart = SplineRadarChart(500, 500)
#    chart = MapChart(440, 220)
#    chart = GoogleOMeterChart(440, 220, x_range=(0, 100))
    sine_data = [math.sin(float(a) / math.pi) * 100 for a in xrange(100)]
    random_data = [random.random() * 100 for a in xrange(100)]
    random_data2 = [random.random() * 50 for a in xrange(100)]
#    chart.set_bar_width(50)
#    chart.set_bar_spacing(0)
    chart.add_data(sine_data)
    chart.add_data(random_data)
    chart.set_zero_line(1, .5)
#    chart.add_data(random_data2)
#    chart.set_line_style(0, thickness=5)
#    chart.set_line_style(1, thickness=2, line_segment=10, blank_segment=5)
#    chart.set_title('heloooo weeee')
#    chart.set_legend(('sine wave', 'random * x'))
    chart.set_colours(('ee2000', 'DDDDAA', 'fF03f2'))
#    chart.fill_solid(Chart.ALPHA, '123456')
#    chart.fill_linear_gradient(Chart.ALPHA, 20, '004070', 1, '300040', 0,
#        'aabbcc55', 0.5)
#    chart.fill_linear_stripes(Chart.CHART, 20, '204070', .2, '300040', .2,
#        'aabbcc00', 0.2)
#    axis_left_index = chart.set_axis_range(Axis.LEFT, 0, 10)
#    axis_right_index = chart.set_axis_range(Axis.RIGHT, 5, 30)
#    axis_bottom_index = chart.set_axis_labels(Axis.BOTTOM, [1, 25, 95])
#    chart.set_axis_positions(axis_bottom_index, [1, 25, 95])
#    chart.set_axis_style(axis_bottom_index, '003050', 15)

#    chart.set_pie_labels(('apples', 'oranges', 'bananas'))

#    chart.set_grid(10, 10)
#    for a in xrange(0, 100, 10):
#        chart.add_marker(1, a, 'a', 'AACA20', 10)

#    chart.add_horizontal_range('00A020', .2, .5)
#    chart.add_vertical_range('00c030', .2, .4)

#    chart.add_fill_simple('303030A0')

#    chart.set_codes(['AU', 'AT', 'US'])
#    chart.add_data([1,2,3])
#    chart.set_colours(('EEEEEE', '000000', '00FF00'))

#    chart.add_data([50,75])
#    chart.set_pie_labels(('apples', 'oranges'))

    url = chart.get_url()
    print url

    chart.download('test.png')

    if 1:
        data = urllib.urlopen(chart.get_url()).read()
        open('meh.png', 'wb').write(data)
        os.system('eog meh.png')


if __name__ == '__main__':
    test()

