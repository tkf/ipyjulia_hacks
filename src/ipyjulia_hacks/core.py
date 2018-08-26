from pathlib import Path

from .utils import Singleton, reloadall
from .julia_api import JuliaAPI


def make_api(julia):
    julia_api_path = Path(__file__).parent.joinpath("julia_api.jl")
    api, eval_str = julia.eval("""
    path -> let m = Module()
        Base.include(m, path)
        (m.JuliaAPI, m.JuliaAPI.eval_str)
    end
    """)(str(julia_api_path))
    return JuliaAPI(eval_str, api)


class APIInitializer(Singleton):

    def __init__(self, *args, **kwargs):
        from julia.core import Julia
        self.api = make_api(Julia(*args, **kwargs))


def initialized_api(*args, **kwargs):
    return APIInitializer.instance(*args, **kwargs).api


def get_api(default=None):
    initializer = APIInitializer.initialized(default=default)
    if initializer is not None:
        return initializer.api


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
