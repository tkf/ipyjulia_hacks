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


def test_symbol_to_str(julia):
    a = julia.eval(":a")
    assert str(a) == "a"


def test_docstring(julia):
    sin = julia.eval("sin")
    assert isinstance(sin.__doc__, str)
    assert "sine" in sin.__doc__


def test_array_contains(julia):
    a = julia.eval('[1, 2, 3]', wrap=True)
    assert 1 in a


def test_missing(julia):
    missing = julia.missing

    def isa_missing(x):
        return julia.eval("===")(x, missing)

    assert isa_missing(missing + 1)
    assert isa_missing(missing - 1)
    assert isa_missing(missing * 1)
    assert isa_missing(missing / 1)
    # assert isa_missing(missing // 1)
    d, r = divmod(missing, 1)
    assert isa_missing(d)
    assert isa_missing(r)
    assert isa_missing(missing % 1)
    assert isa_missing(missing ** 1)


def test_string_mul(julia):
    a = julia.eval('"a"', wrap=True)
    b = julia.eval('"b"', wrap=True)
    assert a * b == "ab"
