==============================================
 Horrible hacks for Julia-IPython integration
==============================================

|readthedocs| |build-status| |coveralls|

Screenshots
===========

The full notebook for the screenshot below can be found here_.

.. _here:
   https://nbviewer.jupyter.org/gist/tkf/f46826bb21ea1377562428beed00a799

.. image:: notebook.png
   :align: center
   :alt: Julia in IPython kernel in Jupyter notebook

.. image:: terminal.png
   :align: center
   :alt: Julia in IPython terminal


Features
========

* `Julia's Multimedia I/O`_ hooked into `IPython's display system`_
* Code completion inside Julia magic (by **monkey-patching** IPython)
* Copy-free access to Julia objects from IPython

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

Pretty much everything has to be installed from development version::

  pip install https://github.com/ipython/ipython/archive/master.zip#egg=ipython
  pip install https://github.com/tkf/pyjulia/archive/venv.zip#egg=julia
  pip install https://github.com/tkf/ipyjulia_hacks/archive/master.zip#egg=ipyjulia_hacks


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
