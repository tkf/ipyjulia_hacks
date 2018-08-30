==================
 `ipyjulia_hacks`
==================

.. automodule:: ipyjulia_hacks


API
===

.. automodule:: ipyjulia_hacks.core.wrappers
.. autofunction:: ipyjulia_hacks.initialize_api
.. autofunction:: ipyjulia_hacks.get_api
.. autoclass:: ipyjulia_hacks.core.JuliaAPI
   :members:


Using ForwardDiff from Python
=============================

>>> from ipyjulia_hacks import initialize_main, jlfunction
>>> @jlfunction
... def f(xs):
...     return sum(xs * 2)
>>> Main = initialize_main()
>>> ForwardDiff = Main.import_("ForwardDiff")
>>> ForwardDiff.gradient(f, [0.0, 1.0])
array([2., 2.])
