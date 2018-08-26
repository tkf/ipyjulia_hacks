import pytest

from .. import initialized_api


def pytest_addoption(parser):
    parser.addoption(
        "--no-julia",
        action="store_false",
        dest="julia",
        default=True,
        help="Skip tests that require julia.",
    )


@pytest.fixture
def julia(request):
    """ pytest fixture for providing a `JuliaAPI` instance. """
    if not request.config.getoption("julia"):
        pytest.skip("--no-julia is passed")
    return initialized_api()
