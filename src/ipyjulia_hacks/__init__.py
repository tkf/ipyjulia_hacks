"""
==============================================
 Horrible hacks for Julia-IPython integration
==============================================

|readthedocs| |build-status| |coveralls|

Screenshots
===========

The full notebook for the screenshot below can be found here_.

.. _here:
   https://nbviewer.jupyter.org/gist/tkf/f46826bb21ea1377562428beed00a799

.. image:: https://raw.githubusercontent.com/tkf/ipyjulia_hacks/master/notebook.png
   :align: center
   :alt: Julia in IPython kernel in Jupyter notebook

.. image:: https://raw.githubusercontent.com/tkf/ipyjulia_hacks/master/terminal.png
   :align: center
   :alt: Julia in IPython terminal


Features
========

* `Julia's Multimedia I/O`_ hooked into `IPython's display system`_
* Code completion inside Julia magic (by **monkey-patching** IPython)
* ``@async`` works in Jupyter (Julia's event loop is integrated to
  ipykernel's asyncio event loop)
* ``print`` works in Jupyter (Julia's standard streams are integrated
  to ipykernel's I/O)
* Syntax highlighting works in ``%%julia`` magic of ``ipython`` CLI
  (but not in Jupyter)
* Copy-free access to Julia objects from Python

Those are build on top of the great libraries PyCall.jl_ and PyJulia_.
(It would be nice to merge some features to PyJulia_ at some point.
But I wanted to do some experiments on Python interface for handling
Julia objects.)

.. _PyJulia: https://github.com/JuliaPy/pyjulia
.. _PyCall.jl: https://github.com/JuliaPy/PyCall.jl
.. _`Julia's Multimedia I/O`:
   https://docs.julialang.org/en/stable/base/io-network/#Multimedia-I/O-1
.. _`IPython's display system`:
   https://ipython.readthedocs.io/en/stable/config/integrating.html


Installation
============

::

  pip install https://github.com/tkf/ipyjulia_hacks/archive/master.zip#egg=ipyjulia_hacks

IPython extension usage
-----------------------
::

  %load_ext ipyjulia_hacks.ipy.magic


.. budges

.. |build-status|
   image:: https://travis-ci.org/tkf/ipyjulia_hacks.svg?branch=master
   :target: https://travis-ci.org/tkf/ipyjulia_hacks
   :alt: Build Status

.. |coveralls|
   image:: https://coveralls.io/repos/github/tkf/ipyjulia_hacks/badge.svg?branch=master
   :target: https://coveralls.io/github/tkf/ipyjulia_hacks?branch=master
   :alt: Test Coverage

.. |readthedocs| image:: https://readthedocs.org/projects/ipyjulia-hacks/badge/?version=latest
   :target: https://ipyjulia-hacks.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
"""

__version__ = "0.0.0"
__author__ = "Takafumi Arakaki"
__license__ = "MIT"

from .core import get_api, get_cached_api, \
    get_main, get_cached_main, \
    jlfunction, revise
from .core.config import IPyJuliaHacks
