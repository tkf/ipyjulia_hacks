from traitlets.config.configurable import SingletonConfigurable
from traitlets.config import get_config
from traitlets import Unicode, Bool, List


class IPyJuliaHacks(SingletonConfigurable):

    def __init__(self, **kwargs):
        c = get_config()
        if "IPyJuliaHacks" in c:
            kwargs = dict(c.IPyJuliaHacks, **kwargs)
        super(IPyJuliaHacks, self).__init__(**kwargs)

    patch_stdio = Bool(
        True,
        help="Try patching Julia's stdio if it makes sense.",
    ).tag(config=True)

    enable_revise = Bool(
        True,
        help="Enable Revise.jl",
    ).tag(config=True)

    mime_include = List(
        Unicode,
        [],
        help="Default list of MIME to include in rich display.",
    ).tag(config=True)

    mime_exclude = List(
        Unicode,
        [],
        help="Default list of MIME to exclude from rich display.",
    ).tag(config=True)
