# Workshop: fix the cause, not the failing example

**Audience:** developers learning Copilot Chat. **Time:** 45 minutes.
**Outcome:** a reviewed pricing fix, meaningful promo tests, and documentation
that distinguishes implemented behavior from desired behavior.

## 1. Baseline and repository map - 5 minutes

Follow the [README setup](README.md#setup) in an isolated Python environment.
The repository targets **Python 3.10+** and uses pytest with `pytest.ini`
setting the import path. Run commands from the repository root.

```powershell
python -m pytest -q
```

The unmodified starter was run on **2026-09-07 with Python 3.14.2**:
**two failures and one pass**. The ordinary silver cart returned `11.875`
instead of `23.75`; the empty cart raised `ZeroDivisionError`.
These are exercise failures, not an instruction to weaken the tests.

If unrelated globally installed pytest plugins fail during collection, use an
isolated environment. For this repository's plugin-free suite, a diagnostic
alternative in PowerShell is:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = "1"
python -m pytest -q
```

| File | Responsibility | Initial coverage |
| --- | --- | --- |
| [src/orders.py](src/orders.py) | Tier discount, total, promo eligibility | Three tests; no promo tests |
| [tests/test_orders.py](tests/test_orders.py) | Independent pricing expectations | Tier cases, ordinary cart, empty cart |
| [src/inventory.py](src/inventory.py) | Stock and reservation ledger | Documentation exercise, no shipped tests |
| [pytest.ini](pytest.ini) | Import path and test discovery | Avoids hand-written `sys.path` workarounds |

## 2. Diagnose without editing - 8 minutes

Attach `src/orders.py` and `tests/test_orders.py`. Use `/explain` when available,
or this plain-language prompt:

```text
Explain calculate_total using the failing tests. Distinguish the subtotal,
discount amount, and final total. Calculate the expected ordinary-cart result
independently. Identify the operation shared by both failures. Do not edit yet.
```

The supplied cart is `10 * 2 + 5 * 1 = 25`. Silver takes 5%, so the discount
is `1.25` and the final total is `23.75`. Dividing that by two explains
`11.875`; dividing an empty cart by zero explains the exception.

Ask what a patch containing only `if not items: return 0` would leave broken.
This is the central lesson: a locally correct special case can miss the root cause.

## 3. Make one bounded repair - 7 minutes

```text
Fix calculate_total so both existing total tests pass without changing their
expectations or the discount tiers. Preserve support for a one-shot iterable.
Add a generator-input regression test and one multi-line cart case.
Do not refactor unrelated inventory or promo code in this change.
```

Review the diff before accepting it. A generator may be exhausted by a
"validation pass" before the subtotal is computed; the annotation is
`Iterable[LineItem]`, not merely a list.

```powershell
python -m pytest -q tests\test_orders.py
```

**Checkpoint:** the ordinary and empty-cart tests pass together, and the
generator test checks a real nonzero total. No expected amount was changed
to fit the implementation.

## 4. Turn promo rules into a decision table - 12 minutes

Write down expected outcomes first. For a starting total of 100:

| Input | Prior discount? | Expected outcome | Rule |
| --- | --- | --- | --- |
| `WELCOME10` | No | 90 | Future-dated, 10% off |
| `WELCOME10` | Yes | 90 | Stackable |
| `VIP20` | No | 80 | Future-dated, 20% off |
| `VIP20` | Yes | `ValueError` | Non-stackable |
| `OLDIE` | No | `ValueError` | Expired |
| `NOPE` | No | `ValueError` | Well-formed but unknown |
| `x!` | No | `ValueError` | Malformed code |
| Test-only code expiring today | No | Accepted | Contract says expired when date is **before** today |
| Test-only code expired yesterday | No | `ValueError` | Expiry boundary |

The 2099 fixture dates are future dates at the recorded baseline, not a
permanent way to make date-dependent tests deterministic.

```text
Create tests/test_promos.py from this decision table. Use pytest monkeypatch
or local test data to control dates and restore PROMO_CODES after each test.
No clock-freezing dependency. Explain any disagreement between the function's
docstring, its implementation, and the nearby bug comment before fixing it.
```

Run the new tests while the bug is present, confirm the failures, then repair
the expiry condition. The comment describing the bug is not the specification:
the docstring's `< today` rule makes expiry-day behavior explicit.

```powershell
python -m pytest -q tests\test_orders.py tests\test_promos.py
```

**Checkpoint:** a future code and a genuinely expired code are both covered.
A test that only checks an unknown code never exercises the expiry branch.

## 5. Document what the ledger does - 8 minutes

Use editor inline chat `/doc`, or attach [src/inventory.py](src/inventory.py)
and request Google-style docstrings without behavior changes.

Have a second reader check the generated descriptions against each method.
For example, `receive` checks positive quantity, but that does not establish
the same validation for every other method. `release` clamps reserved stock
at zero; do not describe it as raising on an excessive release.

```text
Document the public InventoryLedger methods exactly as implemented, including
mutation and errors. Separately list any missing validation you notice.
Do not silently claim those missing checks exist and do not implement them.
```

If you choose to extend the ledger, make that a separate task with its own
agreed contract and tests.

## 6. Review and debrief - 5 minutes

Keep the first failure, the root-cause explanation, the focused diff, and the
final test output. Ask a reviewer to check that the tests would fail against
the original implementation, not merely confirm the new implementation's shape.

An optional extension is to specify negative quantities and monetary precision.
Do not smuggle a float-to-Decimal migration into this debugging exercise:
that is a public contract change, developed explicitly in demo 05.

## Troubleshooting and reset

| Symptom | Likely issue | Next action |
| --- | --- | --- |
| Imports fail | Wrong directory/interpreter | Run `python -m pytest` from the repo root |
| A slash command is missing | Different chat surface/version | Use Add Context and a natural-language equivalent |
| Promo tests depend on today's date | Uncontrolled clock or fixture | Fix the test setup, not the production date |
| A fix changes tests only | Expected value copied from faulty code | Recalculate from the stated rule |
| Inventory docs promise nonexistent checks | Documentation inferred intent | Describe actual behavior; track a separate change |

Use a fresh exercise clone for a repeat session. Preserve the original tests
and your work; no hard reset is needed.

## Current sources

Checked **2026-09-07**:
[VS Code's command reference](https://code.visualstudio.com/docs/agents/reference/ai-features-cheat-sheet)
lists `/explain`, `/fix`, `/tests`, and editor-inline `/doc`.
Command availability is surface-dependent; record the editor version you used.

Next: [Demo 03](https://github.com/xavierxmorris/ghcp-demo-03-todo-api-ts)
applies the same contract-first process across multiple files.
