# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
import os
import sys

# file read helper
def read_from_file(path):
    if os.path.exists(path):
        with open(path,"rb","utf-8") as input:
            return input.read()

setup(
    name='rvo',
    version='20.0.0',
    description='Managing text data from the commandline',
    long_description=read_from_file('README.rst'),
    url='https://github.com/noqqe/rvo',
    author='Florian Baumann',
    author_email='flo@noqqe.de',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Operating System :: POSIX :: BSD :: OpenBSD',
        'Topic :: Terminals',
        'Topic :: Utilities',
        'Topic :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='links mongodb quotes notes journal diary',
    packages=find_packages(),
    zip_safe=True,
    install_requires=['pymongo', 'configparser', 'BeautifulSoup4',
                      'pynacl', 'pyblake2', 'tabulate', 'click',
                      'python-dateutil', 'python-simplemail', 'nltk',
                      'hurry.filesize'],
    entry_points={
        'console_scripts': [
            'rvo=rvo.cli:cli',
        ],
    },
)
