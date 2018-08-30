import os

from .utils import Singleton, reloadall
from .julia_api import JuliaAPI, JuliaMain


def make_api(julia):
    """
    Initialize `.JuliaAPI` using PyJulia.

    Parameters
    ----------
    julia : julia.Julia
        PyJulia's julia interface.
    """
    julia_api_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "julia_api.jl")
    api, eval_str = julia.eval("""
    path -> let m = Module()
        Base.include(m, path)
        (m.JuliaAPI, m.JuliaAPI.eval_str)
    end
    """)(julia_api_path)
    return JuliaAPI(eval_str, api)


class APIInitializer(Singleton):

    def __init__(self, *args, **kwargs):
        from julia.core import Julia
        self.api = make_api(Julia(*args, **kwargs))


def initialize_api(*args, **kwargs):
    """
    Initialize `.JuliaAPI`.

    Positional and keyword arguments are passed directly to `julia.Julia`

    >>> from ipyjulia_hacks import initialize_api
    >>> initialize_api(jl_runtime_path="PATH/TO/CUSTOM/JULIA") # doctest: +SKIP
    <JuliaAPI ...>
    """
    return APIInitializer.instance(*args, **kwargs).api


def get_api():
    """
    Get pre-initialized `.JuliaAPI` instance or `None` if not ready.

    .. (this is for checking availability in doctest)
       >>> _ = getfixture("julia")

    >>> from ipyjulia_hacks import get_api
    >>> jlapi = get_api()
    >>> jlapi.eval("1 + 1")
    2
    """
    initializer = APIInitializer.initialized()
    if initializer is not None:
        return initializer.api


class JuliaMainInitializer(Singleton):

    def __init__(self, *args, **kwargs):
        self.Main = JuliaMain(initialize_api(*args, **kwargs))


def initialize_main(*args, **kwargs):
    return JuliaMainInitializer.instance(*args, **kwargs).Main


def get_main():
    if get_api() is not None:
        return initialize_main()


def revise():
    """Ad-hoc hot reload."""
    import ipyjulia_hacks
    reloadall(ipyjulia_hacks, [
        ipyjulia_hacks.utils,
        ipyjulia_hacks.wrappers,
        ipyjulia_hacks.julia_api,
        ipyjulia_hacks.core,
        ipyjulia_hacks.completers,
        ipyjulia_hacks.magic,
    ])
