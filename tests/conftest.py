import pytest
import logging

@pytest.fixture(autouse=True)
def log_test_name(request):
    test_name = request.node.name
    logging.debug(f"__Pytest: Start running test: {test_name}")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        test_name = item.nodeid
        logging.error(f"__Pytest: FAILED - {test_name}")

