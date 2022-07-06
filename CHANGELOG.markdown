# ChangeLog

## 0.4.1 2018-02-23
 * fix base Google API url (Graham Ullrich)
 * Use correct color delimiter (Dorian Kind)

## 0.4.0 2013-06-02
 * Python 3 compatibility (Geremy Condra)
 * Fix chco separator (Iacopo Spalletti)
 * Download to memory (Eduard Carreras)
 * Documentation work (WoLpH, Eduard Carreras)

## 0.3.0 2010-03-15
 * Allow either arguments in `set_title_style()` (#16) (Alex Robinson)
 * Added MapChart helpers `set_codes()`, `set_geo_area()` and `add_data_dict()` (#23) (Andreas Schawo)
 * Added examples for MapChart
 * Reorganised and contributed to the test suite
 * Fixed examples - line endings to UNIX, correct hash bangs, inserted GPL.
 * Fixed a deprecation warning

## 0.2.1 2008-08-25
 * Added support for QR Code chart (#8) 
 * Added legend positioning (chdlp) (Steve Brandt)
 * Added line styles (chm=D) (Steve Brandt)
 * Added "colours within series" option to chart (chco=xxx|xxx) (Steve Brandt)
 * Added QR codes and more line examples
 * Axis labels are now casted to strings automatically
 * Bug fixed where pie charts stopped working due to automatic scaling
 * Bug fixed where the module would download twice (#7) (Evan Lezar)
 * Bug fixed when automatic scaling is on and None values are in a data set (#5) (Alec Thomas) 
 * Bug fixed with auto-scaling, where the minimum y range was always 0. (#6) (Rohit Jenveja) 
 * Bug fixed, replaced "1" with "0" in add_horizontal_range and add_vertical_range (incorrect syntax for Google) (Steve Brandt)
 * Better clipping checks

## 0.2.0 2008-04-26
 * Automatic scaling, thanks to Trent Mick and Graham Ullrich
 * Added Sparklines, Radar, Google-o-Meter, Map chart types
 * Added priority to shape markers
 * Added zero line to bar charts
 * Grids and Line styles are not restricted to line charts any more.
 * Chart constructors get three new optional attributes: auto_scale, x_range, y_range
 * Data type detection has been re-written roughly following guidelines at http://code.google.com/apis/chart/#chart_data
 * BarChart now allows `bar_width` to not be set.
 * GroupedBarChart now supports the optional third value for 'chbh': spacing between bar groups (the "group_spacing" attribute).
 * Updated examples/line.py updated to use x_range and y_range
 * Added examples bar.py and scatter.py to demonstrate new functionality
 * Converted pygooglechart.py to use UNIX line breaks
 * Division by zero bug fix by Rob Hudson

## 0.1.2 2007-12-16
 * Added more examples
 * Fixed pie labels encoding
 * Fixed MANIFEST.in to allow examples and COPYING in the source distribution
 * Added more metadata in setup.py

## 0.1.1 2007-12-14
 * Renamed download_chart() to download()
 * Axis code refactored to allow for multiple axis labels (see examples for changes)
 * Fixed set_axis_labels() bug with non escaped characters
 * Added a few examples
 * download() checks for content type and raises on bad http codes
 * Added BadContentTypeException for unexpected responses from Google.
 * add_data() returns the index of the dataset
 * Line doesn't allow being an instance
 * Source code is more PEP8 friendly
 * Added COPYING, the GNU GPL licence file

## 0.1.0 2007-12-12
 * Initial release

