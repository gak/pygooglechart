from distutils.core import setup

try: from setuptools import setup
except ImportError: pass

from pygooglechart import __version__

setup(name='pygooglechart',
    version=__version__,
    py_modules=['pygooglechart'],
    description='A complete Python wrapper for the Google Chart API',
    author='Gerald Kaszuba',
    author_email='gerald@geraldkaszuba.com',
    url='https://github.com/gak/pygooglechart',
    download_url='http://slowchop.com/pygooglechart/download/' \
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

