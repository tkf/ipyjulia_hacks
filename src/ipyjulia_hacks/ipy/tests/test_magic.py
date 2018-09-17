from textwrap import dedent

from ...core.wrappers import JuliaObject


def test_line_magic_simple(ipy_with_magic):
    result = ipy_with_magic.run_cell(dedent("""
    %julia :symbol
    """))
    ans = result.result
    assert isinstance(ans, JuliaObject)
    assert str(ans) == "symbol"


def test_cell_magic_simple(ipy_with_magic):
    result = ipy_with_magic.run_cell(dedent("""\
    %%julia
    :symbol
    """))
    ans = result.result
    assert isinstance(ans, JuliaObject)
    assert str(ans) == "symbol"


def test_line_magic_help(ipy_with_magic, julia):
    result = ipy_with_magic.run_cell(dedent("""
    %julia ?sin
    """))
    ans = result.result
    assert isinstance(ans, JuliaObject)
    MD = julia.eval("import Markdown; Markdown.MD")
    assert julia.isa(ans, MD)


def test_cell_magic_help(ipy_with_magic, julia):
    result = ipy_with_magic.run_cell(dedent("""\
    %%julia
    ?sin
    """))
    ans = result.result
    assert isinstance(ans, JuliaObject)
    MD = julia.eval("import Markdown; Markdown.MD")
    assert julia.isa(ans, MD)
