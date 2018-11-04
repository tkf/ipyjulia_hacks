import asyncio
import re
import sys
import warnings

from IPython.core.magic import line_cell_magic
from julia import magic

from ..core import get_api, banner
from ..core.config import IPyJuliaHacks


class JuliaMagicsEnhanced(magic.JuliaMagics):

    def __init__(self, shell):
        super().__init__(shell)

        # Replace core.Julia with JuliaAPI:
        self._julia = get_api()
        banner(self._julia)

    @line_cell_magic
    def julia(self, line, cell=None):
        src = line if cell is None else cell
        src = re.sub(r"^ *\?", "@doc ", src)
        if cell is None:
            line = src
        else:
            cell = src
        return super().julia(line, cell)


async def polling_julia():
    from julia.Base import sleep
    while True:
        sleep(0)
        await asyncio.sleep(0.05)

future_polling_julia = None


def maybe_start_polling_julia():
    global future_polling_julia
    if asyncio.get_event_loop().is_running():
        # asyncio is running (inside ipykernel?).  Let's start polling.
        future_polling_julia = asyncio.ensure_future(polling_julia())


def maybe_patch_stdio():
    if "ipykernel" not in sys.modules:
        return

    from ipykernel.iostream import OutStream
    if not isinstance(sys.stdout, OutStream):
        return

    julia = get_api()
    julia.connect_stdio()


def enable_revise(ip):
    get_api()
    try:
        from julia.Revise import revise
    except ImportError:
        warnings.warn("Failed to import Revise.jl")
        return

    ip.events.register("pre_execute", lambda: revise())
    # Note that `lambda` is required to bypass signature check.


def load_ipython_extension(ip):
    config = IPyJuliaHacks.instance()

    ip.register_magics(JuliaMagicsEnhanced)

    maybe_start_polling_julia()
    if config.patch_stdio:
        maybe_patch_stdio()

    if config.enable_revise:
        enable_revise(ip)

    from . import interactiveshell
    interactiveshell.patch_interactiveshell(ip)

    from . import completers
    completers.patch_ipcompleter()  # monkey patch to make cell magics work
# See:
# https://ipython.readthedocs.io/en/stable/api/generated/IPython.core.hooks.html
# IPython.core.interactiveshell.init_completer
# IPython.core.completerlib (quick_completer etc.)
