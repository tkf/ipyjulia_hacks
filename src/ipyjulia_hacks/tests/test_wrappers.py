def test_peal(Main):
    xs = Main.map(Main.identity, range(3))
    assert all(xs == [0, 1, 2])


def test_wrapped_dict(Main, julia):
    dct = julia.eval("dct = Dict()", force_jlwrap=True)
    dct["key"] = "value"
    assert Main.dct == {"key": "value"}


def test_symbol_eval(julia):
    a = julia.eval(":a")
    assert julia.eval("a -> a isa Symbol")(a)
