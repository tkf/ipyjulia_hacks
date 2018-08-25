import sys

from .wrappers import JuliaObject, autopeal


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

        # After this point, self.<julia_name> works:
        self.getproperty = self.getproperty_str

    @autopeal
    def eval(self, code, *, wrap=True, **kwargs):
        """
        Evaluate `code` in `Main` scope of Julia.

        Parameters
        ----------
        code : str
            Julia code to be evaluated.

        Keyword Arguments
        -----------------
        wrap : bool
            If `True` (default), wrap the output by a Python interface
            (`JuliaObject`) for some appropriate Julia objects.
        scope : JuliaObject or PyCall.jlwrap
            A Julia module (default to `Main`).

        """
        ans = self.eval_str(code, **kwargs)
        if wrap:
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

    def getattr(self, obj, name):
        try:
            return self.maybe_wrap(self.getproperty(obj, jl_name(name)))
        except Exception:
            raise AttributeError(name)
