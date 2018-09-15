from textwrap import dedent

from ....core.wrappers import JuliaObject


def test_line_magic_simple(ipy_with_magic):
    ans = ipy_with_magic.run_cell(dedent("""
    %julia :symbol
    """))
    assert isinstance(ans, JuliaObject)
    assert str(ans) == "symbol"


def test_cell_magic_simple(ipy_with_magic):
    ans = ipy_with_magic.run_cell(dedent("""
    %%julia
    :symbol
    """))
    assert isinstance(ans, JuliaObject)
    assert str(ans) == "symbol"


def test_line_magic_help(ipy_with_magic, Main):
    ans = ipy_with_magic.run_cell(dedent("""
    %julia ?sin
    """))
    assert isinstance(ans, JuliaObject)
    MD = Main.eval("import Markdown; Markdown.MD")
    assert Main.isa(ans, MD)


def test_cell_magic_help(ipy_with_magic, Main):
    ans = ipy_with_magic.run_cell(dedent("""
    %%julia
    ?sin
    """))
    assert isinstance(ans, JuliaObject)
    MD = Main.eval("import Markdown; Markdown.MD")
    assert Main.isa(ans, MD)
