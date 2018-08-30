==================
 `ipyjulia_hacks`
==================

.. automodule:: ipyjulia_hacks


API
===

.. automodule:: ipyjulia_hacks.wrappers
.. automodule:: ipyjulia_hacks.julia_api
.. autofunction:: ipyjulia_hacks.initialize_api
.. autofunction:: ipyjulia_hacks.get_api
.. autoclass:: ipyjulia_hacks.core.JuliaAPI
   :members:


Using ForwardDiff from Python
=============================

>>> from ipyjulia_hacks import initialize_api, jlfunction
>>> @jlfunction
... def f(xs):
...     return sum(xs * 2)
>>> julia = initialize_api()
>>> ForwardDiff = julia.import_("ForwardDiff")
>>> ForwardDiff.gradient(f, [0.0, 1.0])
array([2., 2.])
