from ..wrappers import JuliaObject


def test_mimebundle_doc(julia):
    obj = julia.eval("@doc sin")
    assert isinstance(obj, JuliaObject)
    format_dict = obj._repr_mimebundle_()
    mimes = set(format_dict)
    assert mimes >= {
        "text/plain",
        "text/html",
        "text/markdown",
        "text/latex",
    }
