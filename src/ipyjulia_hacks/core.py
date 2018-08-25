from pathlib import Path

from .utils import Singleton
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
    return APIInitializer.initialized(default=default).api
