import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parent))

from pywabt import __author__, __version__, __email__
from pathlib import Path
from setuptools import setup
from setuptools import find_packages
from sys import version_info

setup(
    name='pywabt',
    version=__version__,
    author=__author__,
    author_email=__email__,
    description='WebAssembly Binary Toolkit (WABT) for Python',
    long_description=(Path(__file__).parent/'README.md').read_text('utf-8'),
    long_description_content_type='text/markdown',
    url='https://github.com/fabriciopashaj/pywabt',
    project_urls={
      'Documentation': 'https://github.com/fabriciopashaj/pywabt#readme',
      'Bug Tracker': 'https://github.com/fabriciopashaj/pywabt/issues'
    },
    license='MIT',
    license_files=['LICENSE'],
    platform=['any'],
    classifiers=[
      "Development Status :: 5 - Production",
      "Target Audience :: Developers",
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent"
    ],
    install_requires=[
      "leb128"
    ],
    package_dir={'': '.'},
    packages=find_packages(where="pywabt"),
    setup_requires=[
      "setuptools >=46.4.0"
    ] if version_info >= (3,) else []
)
