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
.. autoclass:: ipyjulia_hacks.core.JuliaMain
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


Fake `asyncio` integration
--------------------------

Executable scripts of the following examples can be fond in
`examples directory`_.

.. _`examples directory`:
   https://github.com/tkf/ipyjulia_hacks/tree/master/src/ipyjulia_hacks/py3/examples/


Simple example
^^^^^^^^^^^^^^

.. literalinclude:: examples/simple_async.py
   :pyobject: main

Interleaving Python and Julia "background" tasks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Suppose you have a Python coroutine that waits for I/O (here just
calling `asyncio.sleep`) most of the time:

.. literalinclude:: examples/background_tasks.py
   :pyobject: py_repeat

and its Julia equivalent:

.. literalinclude:: examples/background_tasks.py
   :pyobject: jl_repeat

Then you can interleave the execution of those tasks in the event loop
of `asyncio`:

.. literalinclude:: examples/background_tasks.py
   :pyobject: main

This should output something like::

  Julia [A] i = 1
  Julia [B] i = 1
  Python [A] i = 0
  Python [B] i = 0
  Julia [A] i = 2
  Julia [B] i = 2
  Python [A] i = 1
  Python [B] i = 1
  Julia [B] i = 3
  Python [B] i = 2
  Python [B] i = 3
  Julia [B] i = 4
  Python [B] i = 4
  Julia [B] i = 5
  Julia [B] done
  Python [B] done
  Python [A] done
  Julia [A] done
