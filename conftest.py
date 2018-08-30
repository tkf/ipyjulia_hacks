from ipyjulia_hacks import get_api


def pytest_addoption(parser):
    parser.addoption(
        "--no-julia",
        action="store_false",
        dest="julia",
        help="Skip tests that require julia.",
    )


def pytest_configure(config):
    if config.getoption("julia"):
        get_api()
        # The above call initialize the global julia instance. It is
        # then used via `julia` fixture:
        # [[./src/ipyjulia_hacks/tests/conftest.py::def julia]]
