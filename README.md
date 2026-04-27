# Personal Expense Tracker

A command-line expense tracking application built in Python as a Simplilearn course-end project.

---

## Prerequisites

- Python 3.8 or higher
- `pyenv` (recommended for managing Python versions)

Verify your Python version:
```bash
python --version
```

---

## Project Setup

**1. Clone or navigate to the project directory:**
```bash
cd personal-expense-tracker
```

**2. Create a virtual environment:**
```bash
python -m venv .venv
```

**3. Activate the virtual environment:**
```bash
# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

**4. Install dev dependencies (pytest):**
```bash
pip install pytest pytest-cov
```

> No runtime dependencies — the app uses Python standard library only (`csv`, `datetime`, `pathlib`, `sys`).

---

## Running the Application

```bash
PYTHONPATH=src .venv/bin/python main.py
```

Or with the venv activated:
```bash
PYTHONPATH=src python main.py
```

---

## Menu Options

When the application starts, you are presented with this menu:

```
============================
   Personal Expense Tracker
============================
  1. Add expense
  2. View expenses
  3. Track budget
  4. Save expenses
  5. Exit
============================
```

| Option | Description | Function | File |
|--------|-------------|----------|------|
| 1 | Add a new expense — prompts for date, category, amount, description | `handle_add()` | `src/expense_tracker/cli.py` |
| 2 | Display all recorded expenses in a formatted table | `handle_view()` → `print_expenses()` | `cli.py` → `reports.py` |
| 3 | Set a monthly budget and compare it against total spending | `handle_budget()` → `calculate_budget_summary()` | `cli.py` → `budget.py` |
| 4 | Save all current expenses to `expenses.csv` | `handle_save()` → `save_expenses()` | `cli.py` → `storage.py` |
| 5 | Save expenses and exit the program | `save_expenses()` | `cli.py` → `storage.py` |

### Input Validation (applied on every prompt)

| Field | Validation | Function | File |
|-------|-----------|----------|------|
| Date | Must be `YYYY-MM-DD`, not empty, not in the future | `validate_date()` | `src/expense_tracker/validators.py` |
| Amount | Must be a positive number greater than zero | `validate_positive_float()` | `validators.py` |
| Category / Description | Must not be blank | `validate_non_empty_str()` | `validators.py` |

### Auto-save on Interrupt

If you press `Ctrl+C` at any time, the app catches the `KeyboardInterrupt`, saves expenses to `expenses.csv`, and exits cleanly — handled in `run()` in `cli.py`.

---

## Data Persistence

Expenses are stored in `expenses.csv` (created in the working directory on first save). On startup, `load_expenses()` in `src/expense_tracker/storage.py` reads the file automatically and restores your previous session. Rows with invalid data or future dates are skipped with a warning.

---

## Project Structure

```
personal-expense-tracker/
├── pyproject.toml                  # Build config and dev dependencies
├── main.py                         # Entry point
├── resources/
│   └── sample_expenses.csv         # Sample data for testing manually
├── src/
│   └── expense_tracker/
│       ├── __init__.py
│       ├── models.py               # Expense dataclass, CSV_FIELDS, DATE_FORMAT
│       ├── validators.py           # Input validation functions
│       ├── storage.py              # CSV load/save
│       ├── prompts.py              # Interactive input retry loops
│       ├── reports.py              # Formatted output functions
│       ├── budget.py               # Budget calculations
│       └── cli.py                  # Menu loop and option handlers
└── tests/
    ├── conftest.py
    ├── test_models.py
    ├── test_validators.py
    ├── test_storage.py
    ├── test_reports.py
    └── test_budget.py
```

---

## Running Tests

Run all tests:
```bash
PYTHONPATH=src .venv/bin/python -m pytest
```

Run with coverage report:
```bash
PYTHONPATH=src .venv/bin/python -m pytest --cov=expense_tracker
```

Run a specific test file:
```bash
PYTHONPATH=src .venv/bin/python -m pytest tests/test_validators.py
```

Run a specific test:
```bash
PYTHONPATH=src .venv/bin/python -m pytest tests/test_validators.py::TestValidateDate::test_future_date_raises
```

---

## Loading Sample Data

A sample CSV is provided in `resources/`. To use it as a starting point:
```bash
cp resources/sample_expenses.csv expenses.csv
python main.py
```
