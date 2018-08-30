======
 Demo
======

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
