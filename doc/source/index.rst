==================
 `ipyjulia_hacks`
==================

.. automodule:: ipyjulia_hacks


API
===

.. automodule:: ipyjulia_hacks.core.wrappers
.. autofunction:: ipyjulia_hacks.get_api
.. autofunction:: ipyjulia_hacks.get_cached_api
.. autoclass:: ipyjulia_hacks.core.JuliaAPI
   :members:


Demos
=====

* Using Plots.jl etc. inside IPython Jupyter kernel: `Notebook <nb-plots.jl>`_

.. _nb-plots.jl:
   https://nbviewer.jupyter.org/gist/tkf/f46826bb21ea1377562428beed00a799


Using ForwardDiff from Python
-----------------------------

>>> from ipyjulia_hacks import get_main, jlfunction
>>> @jlfunction
... def f(xs):
...     return sum(xs * 2)
>>> Main = get_main()
>>> ForwardDiff = Main.import_("ForwardDiff")
>>> ForwardDiff.gradient(f, [0.0, 1.0])
array([2., 2.])
