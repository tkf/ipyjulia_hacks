from ipyjulia_hacks import initialized_api


def pytest_addoption(parser):
    parser.addoption(
        "--no-julia",
        action="store_false",
        dest="julia",
        help="Skip tests that require julia.",
    )


def pytest_configure(config):
    if config.getoption("julia"):
        initialized_api()
