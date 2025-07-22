import pytest

@pytest.fixture(scope='session')
def setup_environment():
    pass  # Add any setup code if necessary

def pytest_configure():
    pytest.register_assert_rewrite('tests.test_app_free')