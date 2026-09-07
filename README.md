# Demo 02 — Python Quickfix with Copilot Chat 🐍

> **Difficulty:** ⭐⭐
> **GHCP surfaces:** Copilot **Chat** in the IDE — slash-commands (`/explain`,
> `/fix`, `/tests`, `/doc`) and `#file` / `@workspace` references.
> **Stack:** Python 3.10+ (standard library + `pytest`)
> **Time:** ~20 minutes

Demo 01 showed you ghost-text completions. Now you'll learn the **conversational**
side of Copilot — Chat. A different interaction pattern, useful for
**understanding existing code**, **fixing bugs**, and **generating tests**.

**Go deeper:** [WORKSHOP.md](WORKSHOP.md) includes a root-cause exercise,
a promo-code decision table, deterministic date cases, and a review rubric.
The pricing bugs are intentionally left in the starter.

**Editor compatibility:** checked against the current VS Code documentation on
**7 September 2026**. Use the `/` picker to discover commands available in your
session. `/doc` is documented for editor inline chat. If a command or an older
`@workspace` example is unavailable, attach the named files with **Add Context**
and use the equivalent natural-language request. Arbitrary slash names are not
automatically registered commands.

---

## What you'll learn
1. The four high-leverage chat slash-commands: `/explain`, `/fix`, `/tests`, `/doc`.
2. How to point Chat at a *specific file* (`#file:src/orders.py`) or the whole
   workspace (`@workspace`).
3. How to apply Chat's suggested edits with one click (Apply / Insert at cursor).
4. The "show your work" pattern — ask Copilot to *explain why* before accepting a fix.

## Prerequisites
- VS Code with the Copilot **Chat** view (Cmd+Ctrl+I / Ctrl+Alt+I) — comes bundled
  with the Copilot extension.
- Python 3.10+ and `pip`.

## Setup
```bash
git clone https://github.com/xavierxmorris/ghcp-demo-02-python-quickfix.git
cd ghcp-demo-02-python-quickfix
python -m venv .venv
# macOS/Linux:  source .venv/bin/activate
# Windows:      .venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest          # see what's currently passing / failing
```

You should see **2 failing tests** in `tests/test_orders.py`. Don't fix them yet —
let Copilot do it.

---

## Walkthrough

### Step 1 — `/explain` an unfamiliar function

Open `src/orders.py`. Highlight the entire `calculate_discount` function.
Open the Chat view and type:

```
/explain
```

✅ **Expected:** Copilot describes the function in prose, calls out the discount
tiers, and notes the floor at zero.

> **Pro tip:** Use `/explain` as your first move in any unfamiliar codebase
> instead of `git blame`-ing or reading top-down.

### Step 2 — `/fix` a failing test

In the Test Explorer (or `pytest -x` in the terminal) you'll see this failure:

```
FAILED tests/test_orders.py::test_calculate_total_handles_empty_cart
  ZeroDivisionError: division by zero
```

1. Open `src/orders.py` and highlight `calculate_total`.
2. In Chat, type:
   ```
   /fix the failing test test_calculate_total_handles_empty_cart in tests/test_orders.py
   ```
3. Review the proposed diff. Click **Apply in Editor**.
4. Re-run `pytest`.

✅ **Expected:** Both total tests pass. Returning zero for an empty cart is the
specified behavior, but an empty-cart special case alone leaves the ordinary
cart incorrectly divided by its number of line items. Fix the shared cause.

### Step 3 — `/tests` for the untested function

`apply_promo_code` has **no tests**. Highlight the function and ask:

```
/tests cover all branches including invalid codes, expired codes,
and stackable vs non-stackable promos
```

1. Copilot drafts a new test module.
2. Click **Insert into New File** → save as `tests/test_promos.py`.
3. Run `pytest tests/test_promos.py -v`.

✅ **Expected:** Contract-based tests expose the reversed expiry comparison:
future-dated codes are rejected while an expired code is accepted. Which tests
fail depends on the cases generated. Confirm each expected result against the
rules before changing production code.

### Step 4 — `/doc` adds docstrings

Open `src/inventory.py`. Highlight the class `InventoryLedger`. In Chat:

```
/doc add Google-style docstrings to every public method, including
Args, Returns, and Raises sections
```

Apply the edits. Notice Copilot reads the *implementation* to write the docs,
not the other way around.

### Step 5 — `@workspace` for repo-wide questions

Open Chat and ask (no slash-command, just):

```
@workspace where is the discount logic defined and where is it called?
```

✅ **Expected:** Copilot finds `calculate_discount` in `src/orders.py` and lists
its callers, citing file paths.

> `@workspace` is a *retrieval-augmented* query — Copilot indexes your repo so
> answers reference real files instead of hallucinating.

---

## Try it yourself

1. Use `/explain this regex` on the regex in `apply_promo_code`. Was it correct?
2. Ask Chat: *"Convert calculate_total to use a generator expression and explain
   the trade-offs."*
3. Ask: *"What edge cases am I missing in apply_promo_code?"* Then write tests
   for the ones you agree with.
4. Highlight a chunk of code and ask "Simplify this without changing behavior."
   Compare it with "Optimize this and explain the trade-offs." Use ordinary
   text unless your `/` picker actually lists those commands.

## Talking points
- Chat shines on **existing code** (read/understand/fix); completions shine on
  **new code** (write/draft).
- `/tests` is gold for test backfill, but the **tests can be wrong** — Copilot
  will sometimes write a test that asserts the buggy behaviour.
- Always `/explain` *before* you `/fix`. The explanation is the audit trail.
- `@workspace` works best when files are well named and modular — Copilot's
  retrieval is keyword + embedding-based.

## Next demo →
[Demo 03 — Todo API in TypeScript](https://github.com/xavierxmorris/ghcp-demo-03-todo-api-ts) — multi-file
scaffolding with Copilot Chat.
