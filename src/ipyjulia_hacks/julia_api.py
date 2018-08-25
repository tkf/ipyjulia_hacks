import sys

from .wrappers import JuliaObject


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
        self.eval = eval_str
        self.api = api
        # After this point, self.<julia_name> works:
        self.jlwrap_type = type(self.get_jlwrap_prototype())
        self.getproperty = self.getproperty_str

    def __getattr__(self, name):
        try:
            # return super().__getattr__(name, value)
            return object.__getattr__(self, name)
        except AttributeError:
            return self.eval(self.api, jl_name(name))

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
        return self.maybe_wrap(self.getproperty(obj, jl_name(name)))
