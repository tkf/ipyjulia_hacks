from IPython.core.magic import Magics
from julia import magic

from .core import initialized_api
from .julia_api import banner


class JuliaMagicsEnhanced(magic.JuliaMagics):

    def __init__(self, shell):
        super().__init__(shell)

        # Replace core.Julia with JuliaAPI:
        self._julia = initialized_api()
        banner(self._julia)


def load_ipython_extension(ip):
    ip.register_magics(JuliaMagicsEnhanced)

    from . import completers

    # jlcompleter = completers.JuliaCompleter.instance()
    # ip.set_hook("complete_command", jlcompleter.complete_command,
    #             str_key="%julia")

    completers.patch_ipcompleter()  # monkey patch to make cell magics work
# See:
# https://ipython.readthedocs.io/en/stable/api/generated/IPython.core.hooks.html
# IPython.core.interactiveshell.init_completer
# IPython.core.completerlib (quick_completer etc.)
