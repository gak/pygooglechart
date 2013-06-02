Python Google Chart
===================

pygooglechart is a complete Python wrapper for the Google Chart API.

pygooglechart works with Linux, Windows and Mac OS X.

## Deprecation Warning

Unfortunatelly Google has deprecated this API:

    The Image Charts portion of Google Chart Tools has been officially deprecated as of April 20, 2012.
    After April 20, 2015, this Deprecation Policy will not apply. 

Example
-------

    from pygooglechart import PieChart3D

    # Create a chart object of 250x100 pixels
    chart = PieChart3D(250, 100)

    # Add some data
    chart.add_data([20, 10])

    # Assign the labels to the pie data
    chart.set_pie_labels(['Hello', 'World'])

    # Print the chart URL
    print chart.get_url()

    # Download the chart
    chart.download('pie-hello-world.png')

There are more examples in [the examples directory](https://github.com/gak/pygooglechart/tree/master/examples).

Installation
------------
There are a few ways of installing it from source:

If you have setuptools installed, simply run the following:

    easy_install pygooglechart

Or get the sources and run:

    python setup.py install

