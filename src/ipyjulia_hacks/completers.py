from types import SimpleNamespace

from cached_property import cached_property


class JuliaCompleter:

    def __init__(self, julia=None):
        from julia import Julia
        self.julia = Julia() if julia is None else julia

    @cached_property
    def jlcomplete(self):
        return self.julia.eval("""
        import REPL
        (str, pos) -> begin
            ret, _, should_complete =
                REPL.completions(str, pos)
            if should_complete
                return map(REPL.completion_text, ret)
            else
                return String[]
            end
        end
        """)

    def complete_command(self, ip, event):
        pos = event.line.find("%julia")
        if pos < 0:
            return []
        pos += len("%julia")  # pos: beginning of Julia code
        julia_code = event.line[pos:]
        julia_pos = len(event.text_until_cursor) - pos

        completions = self.jlcomplete(julia_code, julia_pos)
        if "." in event.symbol:
            # When completing (say) "Base.s" we need to add the prefix "Base."
            prefix = event.symbol.rsplit(".", 1)[0]
            completions = [".".join((prefix, c)) for c in completions]
        return completions

    def julia_matches(self, ip_completer, text):
        self.last_text = text
        if not ip_completer.text_until_cursor.startswith("%%julia"):
            return []
        prefix_len = len("%%julia")
        julia_pos = len(ip_completer.text_until_cursor) - prefix_len
        julia_code = text[prefix_len:]
        completions = self.jlcomplete(julia_code, julia_pos)
        self.last_completions = completions
        return completions

    def make_julia_matcher(self, ip_completer):
        def julia_matches(text):
            return self.julia_matches(ip_completer, text)
        return julia_matches

    @classmethod
    def instance(cls, *args, **kwargs):
        try:
            return cls.__initialized
        except AttributeError:
            pass
        cls.__initialized = self = cls(*args, **kwargs)
        return self



patch_ipcompleter_info = None


def patch_ipcompleter():
    global patch_ipcompleter_info
    if patch_ipcompleter_info is not None:
        return

    from IPython.core.completer import IPCompleter
    patch_ipcompleter_info = _patch_ipcompleter(IPCompleter,
                                                JuliaCompleter.instance())


def _patch_ipcompleter(IPCompleter, jlcompleter):
    orig_matchers = IPCompleter.matchers

    @property
    def matchers(self):
        methods = [
            jlcompleter.make_julia_matcher(self),
        ]
        methods.extend(orig_matchers.__get__(self, IPCompleter))
        return methods

    IPCompleter.matchers = matchers

    return SimpleNamespace(
        orig_matchers=orig_matchers,
        patched_matchers=matchers,
        IPCompleter=IPCompleter,
    )
