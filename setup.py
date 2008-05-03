from distutils.core import setup
from setuptools import setup
from pygooglechart import __version__

setup(name='pygooglechart',
    version=__version__,
    py_modules=['pygooglechart'],
    description='A complete Python wrapper for the Google Chart API',
    author='Gerald Kaszuba',
    author_email='gerald@geraldkaszuba.com',
    url='http://pygooglechart.slowchop.com/',
    download_url='http://pygooglechart.slowchop.com/files/download/' \
        'pygooglechart-%s.tar.gz' % __version__,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
)

