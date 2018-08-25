from types import SimpleNamespace
import re

from IPython.core.completer import Completion, IPCompleter
from cached_property import cached_property


class JuliaCompleter:

    def __init__(self, julia=None):
        from julia import Julia
        self.julia = Julia() if julia is None else julia
        self.magic_re = re.compile(r"\s*%%?julia\s*")

    @cached_property
    def jlcomplete_texts(self):
        return self.julia.eval("""
        import REPL
        (str, pos) -> begin
            ret, _, should_complete =
                REPL.completions(str, pos)
            if should_complete
                return map(REPL.completion_text, ret)
            else
                return []
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

        completions = self.jlcomplete_texts(julia_code, julia_pos)
        if "." in event.symbol:
            # When completing (say) "Base.s" we need to add the prefix "Base."
            prefix = event.symbol.rsplit(".", 1)[0]
            completions = [".".join((prefix, c)) for c in completions]
        return completions

    @cached_property
    def jlcomplete(self):
        return self.julia.eval("""
        import REPL
        (str, pos) -> begin
            ret, ran, should_complete = REPL.completions(str, pos)
            return (
                map(REPL.completion_text, ret),
                (first(ran), last(ran)),
                should_complete,
            )
        end
        """)

    def julia_completions(self, full_text: str, offset: int):
        self.last_text = full_text
        match = self.magic_re.match(full_text)
        if not match:
            return []
        prefix_len = match.end()
        jl_pos = offset - prefix_len
        jl_code = full_text[prefix_len:]
        texts, (jl_start, jl_end), should_complete = \
            self.jlcomplete(jl_code, jl_pos)
        start = jl_start - 1 + prefix_len
        end = jl_end + prefix_len
        completions = [Completion(start, end, txt) for txt in texts]
        self.last_completions = completions
        # if not should_complete:
        #     return []
        return completions

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

    patch_ipcompleter_info = _patch_ipcompleter(IPCompleter,
                                                JuliaCompleter.instance())


def _patch_ipcompleter(IPCompleter, jlcompleter):
    orig__completions = IPCompleter._completions

    def _completions(self, full_text: str, offset: int, **kwargs):
        completions = jlcompleter.julia_completions(full_text, offset)
        if completions:
            yield from completions
        else:
            yield from orig__completions(self, full_text, offset, **kwargs)

    IPCompleter._completions = _completions

    return SimpleNamespace(
        orig__completions=orig__completions,
        patched__completions=_completions,
        IPCompleter=IPCompleter,
    )
