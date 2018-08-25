def load_ipython_extension(ip):
    from julia import magic
    magic.load_ipython_extension(ip)

    from . import completers
    jlcompleter = completers.JuliaCompleter.instance()
    ip.set_hook("complete_command", jlcompleter.complete_command,
                str_key="%julia")

    completers.patch_ipcompleter()  # monkey patch to make cell magics work
# See:
# https://ipython.readthedocs.io/en/stable/api/generated/IPython.core.hooks.html
# IPython.core.interactiveshell.init_completer
# IPython.core.completerlib (quick_completer etc.)
