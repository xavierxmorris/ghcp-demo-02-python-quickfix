"""Tiny in-memory inventory ledger — used by the /doc demo."""

from __future__ import annotations
from collections import defaultdict


class InventoryLedger:
    def __init__(self):
        self._stock = defaultdict(int)
        self._reserved = defaultdict(int)

    def receive(self, sku, qty):
        if qty <= 0:
            raise ValueError("qty must be positive")
        self._stock[sku] += qty

    def reserve(self, sku, qty):
        if self.available(sku) < qty:
            raise ValueError(f"insufficient stock for {sku}")
        self._reserved[sku] += qty

    def release(self, sku, qty):
        self._reserved[sku] = max(0, self._reserved[sku] - qty)

    def ship(self, sku, qty):
        if self._reserved[sku] < qty:
            raise ValueError(f"cannot ship more than reserved for {sku}")
        self._reserved[sku] -= qty
        self._stock[sku] -= qty

    def available(self, sku):
        return self._stock[sku] - self._reserved[sku]

    def snapshot(self):
        return {
            sku: {"on_hand": self._stock[sku], "reserved": self._reserved[sku]}
            for sku in self._stock
        }
