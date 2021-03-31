import pytest

def pytest_addoption(parser):
    parser.addoption("--name", action="store")
    parser.addoption("--arg", action="store")


@pytest.fixture(scope='session')
def name(request):
    name_value = request.config.option.name
    if name_value is None:
        pytest.exit()
    return name_value


@pytest.fixture(scope='session')
def arg(request):
    arg_value = request.config.option.arg
    if arg_value is None:
        pytest.exit()
    return arg_value
    