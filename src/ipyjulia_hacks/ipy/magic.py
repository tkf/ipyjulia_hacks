import asyncio
import warnings

from julia import magic
import IPython

from ..core import get_api, banner


class JuliaMagicsEnhanced(magic.JuliaMagics):

    def __init__(self, shell):
        super().__init__(shell)

        # Replace core.Julia with JuliaAPI:
        self._julia = get_api()
        banner(self._julia)


async def julia_eventloop(julia):
    while True:
        julia.eval("sleep(0)")
        await asyncio.sleep(0.05)


def start_julia_eventloop():
    if int(IPython.__version__.split(".", 1)[0]) < 7:
        warnings.warn("Julia event loop is not running in IPython < v7")
        return

    asyncio.ensure_future(julia_eventloop(get_api()))


def load_ipython_extension(ip):
    ip.register_magics(JuliaMagicsEnhanced)

    start_julia_eventloop()

    from . import completers
    completers.patch_ipcompleter()  # monkey patch to make cell magics work
# See:
# https://ipython.readthedocs.io/en/stable/api/generated/IPython.core.hooks.html
# IPython.core.interactiveshell.init_completer
# IPython.core.completerlib (quick_completer etc.)
