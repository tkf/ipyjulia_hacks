from IPython.terminal.interactiveshell import TerminalInteractiveShell
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers import JuliaLexer

from ..core.utils import Singleton


class TerminalInteractiveShellPatcher(Singleton):

    def __init__(self):
        self.patch_extra_prompt_options(TerminalInteractiveShell)

    def patch_extra_prompt_options(self, TerminalInteractiveShell):
        orig__extra_prompt_options = self.orig__extra_prompt_options = \
            TerminalInteractiveShell._extra_prompt_options

        def _extra_prompt_options(self):
            options = orig__extra_prompt_options(self)
            options["lexer"].magic_lexers["julia"] = PygmentsLexer(JuliaLexer)
            return options

        TerminalInteractiveShell._extra_prompt_options = _extra_prompt_options


def patch_interactiveshell(ip):
    if isinstance(ip, TerminalInteractiveShell):
        TerminalInteractiveShellPatcher.instance()
