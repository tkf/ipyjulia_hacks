"""
Pythonic wrapper of Julia objects.

.. (this is for checking availability in doctest)
   >>> _ = getfixture("julia")

>>> from ipyjulia_hacks import get_api
>>> jlapi = get_api()

**Named tuple**:

>>> nt = jlapi.eval("(a = 1, b = 2)")
>>> nt.a
1
>>> nt.b
2
>>> nt[1]
1
>>> nt[2]
2
>>> len(nt)
2
>>> {"a", "b"} <= set(dir(nt))
True

**Dictionary**:

>>> dct = jlapi.eval('Dict("b" => 2)')
>>> dct["a"] = 1
>>> del dct["b"]
>>> dct["a"]
1
>>> dct
<JuliaObject Dict("a"=>1)>
"""

from types import FunctionType
import functools
import json


unspecified = object()


class JuliaObject(object):
    """
    Python interface for Julia object.

    Parameters
    ----------
    jlwrap : PyCall.jlwrap
        Julia object wrapped as PyCall.jlwrap.
    julia : JuliaAPI
        Python interface for calling Julia functions.

        See:
        ./core.py
        ../julia_api.jl
    """

    def __init__(self, jlwrap, julia):
        self.__jlwrap = jlwrap
        self.__julia = julia

    def __str__(self):
        return self.__julia.string(self.__jlwrap)

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__,
                                self.__julia.repr(self.__jlwrap))

    @property
    def __doc__(self):
        return self.__jlwrap.__doc__

    def __getattr__(self, name):
        return self.__julia.getattr(self.__jlwrap, name)

    def __dir__(self):
        return self.__julia.py_names(self.__jlwrap)

    def __call__(self, *args, **kwargs):
        return self.__julia.wrapcall(self.__jlwrap, *args, **kwargs)

    def __eq__(self, other):
        return self.__julia.eval("==")(self.__jlwrap, other)

    def __len__(self):
        return self.__julia.length(self.__jlwrap)

    def __getitem__(self, key):
        if not isinstance(key, tuple):
            key = (key,)
        return self.__julia.getindex(self.__jlwrap, *key)

    def __setitem__(self, key, value):
        if not isinstance(key, tuple):
            key = (key,)
        self.__julia.setindex_b(self.__jlwrap, value, *key)

    def __delitem__(self, key):
        if not isinstance(key, tuple):
            key = (key,)
        self.__julia.delete_b(self.__jlwrap, *key)

    def __iter__(self):
        iterate = self.__julia.eval("iterate")
        pair = iterate(self.__jlwrap)
        while True:
            if pair is None:
                return
            yield pair[1]
            pair = iterate(self.__jlwrap, pair[2])

    def __contains__(self, item):
        return self.__julia.eval("in")(item, self.__jlwrap)

    def __add__(self, other):
        return self.__julia.eval("+")(self.__jlwrap, other)

    def __sub__(self, other):
        return self.__julia.eval("-")(self.__jlwrap, other)

    def __mul__(self, other):
        return self.__julia.eval("*")(self.__jlwrap, other)

    # def __matmul__(self, other):
    #     return self.__julia.eval("???")(self.__jlwrap, other)

    def __truediv__(self, other):
        return self.__julia.eval("/")(self.__jlwrap, other)

    def __floordiv__(self, other):
        return self.__julia.eval("//")(self.__jlwrap, other)

    def __mod__(self, other):
        return self.__julia.eval("mod")(self.__jlwrap, other)

    def __divmod__(self, other):
        return self.__julia.eval("divrem")(self.__jlwrap, other)

    def __pow__(self, other, modulo=unspecified):
        if modulo is unspecified:
            return self.__julia.eval("^")(self.__jlwrap, other)
        else:
            return self.__julia.eval("powermod")(self.__jlwrap, other, modulo)

    def __lshift__(self, other):
        return self.__julia.eval("<<")(self.__jlwrap, other)

    def __rshift__(self, other):
        return self.__julia.eval(">>")(self.__jlwrap, other)

    def __and__(self, other):
        return self.__julia.eval("&")(self.__jlwrap, other)

    def __xor__(self, other):
        return self.__julia.eval("xor")(self.__jlwrap, other)

    def __or__(self, other):
        return self.__julia.eval("|")(self.__jlwrap, other)

    def _repr_mimebundle_(self, include=None, exclude=None):
        mimes = include or [
            "text/plain",
            "text/html",
            "text/markdown",
            "text/latex",
            "application/json",
            "application/javascript",
            "application/pdf",
            "image/png",
            "image/jpeg",
            "image/svg+xml",
        ]
        exclude = exclude or []

        showable = self.__julia.eval("showable")
        showraw = self.__julia.eval("""
        (obj, mimetype) -> begin
            io = IOBuffer()
            show(IOContext(io, :color => true), mimetype, obj)
            take!(io)
        end
        """)

        format_dict = {}
        for mimetype in mimes:
            if mimetype in exclude:
                continue
            if showable(mimetype, self.__jlwrap):
                data = showraw(self.__jlwrap, mimetype)
                if (mimetype.startswith("text/") or
                        mimetype in ("application/javascript",
                                     "image/svg+xml")):
                    data = data.decode()
                elif mimetype == "application/json":
                    data = json.loads(data)
                else:
                    data = bytes(data)
                format_dict[mimetype] = data
        return format_dict

# https://ipython.readthedocs.io/en/stable/api/generated/IPython.core.formatters.html#IPython.core.formatters.DisplayFormatter.format
# https://ipython.readthedocs.io/en/stable/config/integrating.html#MyObject._repr_mimebundle_


def peal(obj):
    return obj._JuliaObject__jlwrap if isinstance(obj, JuliaObject) else obj


def autopeal(fun):
    @functools.wraps(fun)
    def wrapper(self, *args, **kwds):
        # Peal off all arguments if they are wrapped by JuliaObject.
        # This is required for, e.g., Main.map(Main.identity, range(3))
        # to work.
        args = [peal(a) for a in args]
        kwds = {k: peal(v) for (k, v) in kwds.items()}
        return fun(self, *args, **kwds)
    return wrapper


for name, fun in vars(JuliaObject).items():
    if name in ("__module__", "__init__", "__doc__"):
        continue
    if name.startswith('_JuliaObject__'):
        continue
    if not isinstance(fun, FunctionType):
        continue
    # TODO: skip single-argument (i.e., `self`-only) methods (optimization)
    setattr(JuliaObject, name, autopeal(fun))
