import pytest
from src.orders import LineItem, calculate_discount, calculate_total


def test_calculate_discount_tiers():
    assert calculate_discount(100, "bronze") == 0
    assert calculate_discount(100, "silver") == 5
    assert calculate_discount(100, "gold") == 10
    assert calculate_discount(1000, "gold") == 50  # capped
    assert calculate_discount(100, "plat") == 15
    assert calculate_discount(10000, "plat") == 200  # capped


def test_calculate_total_basic():
    items = [LineItem("A", 10.0, 2), LineItem("B", 5.0, 1)]  # subtotal 25
    total = calculate_total(items, "silver")  # 5% off -> 23.75
    assert total == pytest.approx(23.75)


def test_calculate_total_handles_empty_cart():
    # An empty cart should return 0.0, not blow up with ZeroDivisionError.
    assert calculate_total([], "bronze") == 0.0
