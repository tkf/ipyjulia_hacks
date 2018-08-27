import sys

from .wrappers import JuliaObject, autopeal, peal


def jl_name(name):
    if name.endswith('_b'):
        return name[:-2] + '!'
    return name


def py_name(name):
    if name.endswith('!'):
        return name[:-1] + '_b'
    return name


class JuliaAPI(object):

    def __init__(self, eval_str, api):
        self.eval_str = eval_str
        self.api = api
        get_jlwrap_prototype = eval_str("get_jlwrap_prototype", scope=api)
        self.jlwrap_type = type(get_jlwrap_prototype())

        # Use wrap=False when getting wrapcall to avoid infinite recursion.
        self.wrapcall = self.eval("wrapcall", wrap=False, scope=self.api)

        # After this point, self.<julia_name> works:
        self.getproperty = self.getproperty_str

    @autopeal
    def eval(self, code, *, wrap=None, **kwargs):
        """
        Evaluate `code` in `Main` scope of Julia.

        Parameters
        ----------
        code : str
            Julia code to be evaluated.

        Keyword Arguments
        -----------------
        wrap : {True, False, None}
            If `None` (default), wrap the output by a Python interface
            (`JuliaObject`) for some appropriate Julia objects.
            Force wrapping by passing None and
        scope : JuliaObject or PyCall.jlwrap
            A Julia module (default to `Main`).

        Examples
        --------
        .. (this is for checking availability in doctest)
           >>> _ = getfixture("julia")

        >>> from ipyjulia_hacks import get_api
        >>> jlapi = get_api()

        By default, most of Julia objects returned by this function
        are the the Python wrapper `.JuliaObject`.  This object just
        has a reference to the object held by Julia so that passing it
        back to Julia is easy.  However, you can suppress this
        behavior by passing `wrap=False`.  For example:

        >>> _ = jlapi.eval("dct = Dict()")
        >>> dct_jl = jlapi.eval("dct")
        >>> dct_py = jlapi.eval("dct", wrap=False)
        >>> dct_jl
        <JuliaObject Dict{Any,Any}()>
        >>> dct_py
        {}
        >>> assert isinstance(dct_py, dict)
        >>> dct_jl["a"] = 1
        >>> dct_py["b"] = 2
        >>> jlapi.eval("dct")
        <JuliaObject Dict{Any,Any}("a"=>1)>

        Note that `dct` object (living in Julia's `Main`) does not
        have the key `"b"`.  This is because `dct_py` is a copy of
        the original Julia object.

        Some objects such as `Array` are not wrapped by `.JuliaObject`
        by default.  Julia `Array` is automatically converted to
        `numpy.ndarray` in a copy-free manner by PyCall.jl:

        >>> _ = jlapi.eval("xs = [1, 2, 3]")
        >>> xs = jlapi.eval("xs")
        >>> xs
        array([1, 2, 3], dtype=int64)
        >>> xs[0] = 100
        >>> jlapi.eval("xs")
        array([100,   2,   3], dtype=int64)
        """
        assert wrap in (True, False, None)
        if wrap:
            kwargs.setdefault('force_jlwrap', True)
        elif wrap is False:
            kwargs.setdefault('auto_jlwrap', False)
        ans = self.eval_str(code, **kwargs)
        if wrap in (True, None):
            return self.maybe_wrap(ans)
        return ans

    def __getattr__(self, name):
        try:
            # return super().__getattr__(name, value)
            return object.__getattr__(self, name)
        except AttributeError:
            try:
                return self.eval(jl_name(name), scope=self.api)
            except Exception:
                raise AttributeError(name)

    def py_names(self, obj):
        names = self.dir(obj)
        names = map(py_name, names)
        if sys.version_info.major == 3:
            names = filter(str.isidentifier, names)
        return names

    def isjlwrap(self, obj):
        return isinstance(obj, self.jlwrap_type)

    def maybe_wrap(self, obj):
        if self.isjlwrap(obj):
            return JuliaObject(obj, self)
        else:
            return obj

    def maybe_unwrap(self, obj):
        return self.eval("identity", wrap=False, scope=self.api)(peal(obj))

    def getattr(self, obj, name):
        """
        Get attribute (property) named `name` of Julia object `obj`.
        """
        try:
            return self.maybe_wrap(self.getproperty(obj, jl_name(name)))
        except Exception:
            raise AttributeError(name)


def banner(julia, **kwargs):
    banner = julia.eval("""
    io = IOBuffer()
    Base.banner(IOContext(io, :color=>true))
    String(take!(io))
    """)
    print(banner.rstrip(), **kwargs)
