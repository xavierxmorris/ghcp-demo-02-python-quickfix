"""Keep the two teaching defects explicit without weakening normal pytest runs."""

from __future__ import annotations

import pytest

EXPECTED_FAILURES = {
    "tests/test_orders.py::test_calculate_total_basic": (
        AssertionError,
        "Workshop exercise: total is incorrectly divided by the item count",
    ),
    "tests/test_orders.py::test_calculate_total_handles_empty_cart": (
        ZeroDivisionError,
        "Workshop exercise: empty cart divides by zero",
    ),
}


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--starter-baseline", action="store_true", help="Require the documented starter failures")


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if config.getoption("--starter-baseline"):
        missing = EXPECTED_FAILURES.keys() - {item.nodeid for item in items}
        if missing:
            raise pytest.UsageError(f"Starter baseline tests are missing: {sorted(missing)}")
        for item in items:
            if item.nodeid in EXPECTED_FAILURES:
                exception, reason = EXPECTED_FAILURES[item.nodeid]
                item.add_marker(pytest.mark.xfail(strict=True, raises=exception, reason=reason))
