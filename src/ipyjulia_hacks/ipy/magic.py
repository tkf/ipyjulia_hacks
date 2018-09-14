import asyncio
import sys

from julia import magic

from ..core import get_api, banner
from ..core.config import IPyJuliaHacks


class JuliaMagicsEnhanced(magic.JuliaMagics):

    def __init__(self, shell):
        super().__init__(shell)

        # Replace core.Julia with JuliaAPI:
        self._julia = get_api()
        banner(self._julia)


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


def load_ipython_extension(ip):
    config = IPyJuliaHacks.instance()

    ip.register_magics(JuliaMagicsEnhanced)

    maybe_start_polling_julia()
    if config.patch_stdio:
        maybe_patch_stdio()

    from . import interactiveshell
    interactiveshell.patch_interactiveshell(ip)

    from . import completers
    completers.patch_ipcompleter()  # monkey patch to make cell magics work
# See:
# https://ipython.readthedocs.io/en/stable/api/generated/IPython.core.hooks.html
# IPython.core.interactiveshell.init_completer
# IPython.core.completerlib (quick_completer etc.)
