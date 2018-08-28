from ..wrappers import JuliaObject


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


def test_three_valued_logic_left(julia):
    true = julia.eval("true", wrap=True)
    false = julia.eval("false", wrap=True)
    missing = julia.eval("missing")

    def isa_missing(x):
        return julia.eval("===")(x, missing)

    assert isa_missing(true & missing)
    assert not false & missing
    assert true | missing
    assert isa_missing(false | missing)
    assert true ^ False
    assert not true ^ True
    assert isa_missing(true ^ missing)
    assert not false ^ False


def test_three_valued_logic_right(julia):
    true = julia.eval("true", wrap=True)
    false = julia.eval("false", wrap=True)
    missing = julia.eval("missing")

    def isa_missing(x):
        return julia.eval("===")(x, missing)

    assert isa_missing(True & missing)
    assert not False & missing
    assert True | missing
    assert isa_missing(False | missing)
    assert True ^ false
    assert not True ^ true
    assert isa_missing(True ^ missing)
    assert not False ^ false


def test_string_mul(julia):
    a = julia.eval('"a"', wrap=True)
    b = julia.eval('"b"', wrap=True)
    assert a * b == "ab"


def test_bitarray_lshift(julia):
    x = julia.eval("""
    x = BitArray([0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1])
    """)
    actual = x << 2
    desired = julia.eval("x << 2")
    assert actual == desired
    # assert isinstance(actual, JuliaObject)
    # assert isinstance(desired, JuliaObject)


def test_bitarray_rshift(julia):
    x = julia.eval("""
    x = BitArray([0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1])
    """)
    actual = x >> 2
    desired = julia.eval("x >> 2")
    assert actual == desired
    # assert isinstance(actual, JuliaObject)
    # assert isinstance(desired, JuliaObject)



def test_constructor(julia):
    BitArray = julia.BitArray
    ba = BitArray([1, 0, 1, 0])
    assert isinstance(ba, JuliaObject)
