from IPython.testing.globalipapp import get_ipython
import pytest

from .. import magic
from ...core.conftest import julia

if False:
    julia()


@pytest.fixture(scope="session")
def ipy_with_magic(julia):
    ip = get_ipython()
    magic.load_ipython_extension(ip)
    return ip
