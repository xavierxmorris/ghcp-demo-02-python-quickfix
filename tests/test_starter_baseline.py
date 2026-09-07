"""A different wrong result must not hide behind the teaching test's xfail."""

from __future__ import annotations

import pytest

from src.orders import LineItem, calculate_total


def test_known_total_failure_has_not_changed(pytestconfig: pytest.Config) -> None:
    if not pytestconfig.getoption("--starter-baseline"):
        pytest.skip("This assertion protects only the intentionally broken starter")
    items = [LineItem("A", 10.0, 2), LineItem("B", 5.0, 1)]
    assert calculate_total(items, "silver") == pytest.approx(11.875)
