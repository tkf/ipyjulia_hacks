def test_peal(Main):
    xs = Main.map(Main.identity, range(3))
    assert all(xs == [0, 1, 2])


def test_wrapped_dict(julia):
    dct = julia.eval("Dict()")
    dct["key"] = "value"
    unwrapped = julia.maybe_unwrap(dct)
    assert unwrapped == {"key": "value"}


def test_unwrapped_dict(julia):
    dct = julia.eval('Dict("a" => 1)', wrap=False)
    assert dct == {"a": 1}


def test_symbol_eval(julia):
    a = julia.eval(":a")
    assert julia.eval("a -> a isa Symbol")(a)


def test_symbol_call(julia):
    a = julia.eval("() -> :a")()
    assert julia.eval("a -> a isa Symbol")(a)
