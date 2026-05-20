"""Order pricing — small, intentionally-rough module to drive Copilot Chat demos."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class LineItem:
    sku: str
    unit_price: float
    quantity: int


def calculate_discount(subtotal: float, customer_tier: str) -> float:
    """Return the discount AMOUNT (not the discounted total) for the subtotal.

    Tiers:
        bronze -> 0%
        silver -> 5%
        gold   -> 10% but capped at $50
        plat   -> 15% but capped at $200

    Discount is floored at 0 (never negative).
    """
    rate, cap = {
        "bronze": (0.00, float("inf")),
        "silver": (0.05, float("inf")),
        "gold":   (0.10, 50.0),
        "plat":   (0.15, 200.0),
    }.get(customer_tier, (0.0, float("inf")))
    return max(0.0, min(subtotal * rate, cap))


def calculate_total(items: Iterable[LineItem], customer_tier: str = "bronze") -> float:
    """Subtotal items, apply tier discount, return final total.

    🐞 BUG: This implementation divides by the number of items at the end to
    "average-weight" the discount. That makes no business sense AND blows up on
    an empty cart.
    """
    items = list(items)
    subtotal = sum(i.unit_price * i.quantity for i in items)
    discount = calculate_discount(subtotal, customer_tier)
    return (subtotal - discount) / len(items)


# Promo codes: "code": (percent_off, stackable, expires_iso)
PROMO_CODES = {
    "WELCOME10": (10, True,  "2099-01-01"),
    "VIP20":     (20, False, "2099-01-01"),
    "OLDIE":     (50, True,  "2020-01-01"),  # expired
}


def apply_promo_code(total: float, code: str, already_discounted: bool = False) -> float:
    """Apply a promo code to a total. Returns the new total.

    Rules:
        - Unknown code -> raise ValueError.
        - Expired code (date < today) -> raise ValueError.
        - If `already_discounted` is True and the promo is NOT stackable,
          raise ValueError.
        - Otherwise subtract `percent_off`%.

    🐞 At least one of these rules is implemented incorrectly. The test suite
    you generate in Step 3 will find it.
    """
    import datetime, re
    if not re.match(r"^[A-Z0-9]{3,10}$", code):
        raise ValueError(f"Malformed promo code: {code!r}")
    if code not in PROMO_CODES:
        raise ValueError(f"Unknown promo code: {code!r}")
    percent, stackable, expires = PROMO_CODES[code]
    # NOTE: deliberately buggy expiry check (uses < instead of <=, wrong sense)
    if datetime.date.fromisoformat(expires) > datetime.date.today():
        # treat as expired
        raise ValueError(f"Promo code expired: {code!r}")
    if already_discounted and not stackable:
        raise ValueError(f"Promo code {code!r} cannot be stacked")
    return total * (1 - percent / 100)
