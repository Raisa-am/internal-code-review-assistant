# Internal Code Review Assistant
### Case Study 72 — Intelligent Diff Analysis and Comment Suggestion System

A local Flask prototype that accepts unified Git diffs, identifies changed lines, runs selected rule-based checks, deduplicates findings, and lets a reviewer record decisions.

## Features
- Paste a unified Git diff or upload `.diff`, `.patch`, or `.txt`.
- Parse changed files and added-line locations.
- Demonstration rules for suspicious range conditions, credential-like assignments, bare `except`, and production `print()` calls.
- Severity, explanation, file/line reference, and suggested correction.
- Duplicate-finding filtering.
- Accept, reject, or dismiss findings with optional notes.
- SQLite review history.
- Submitted source code is never executed.

## Technology
Python, Flask, HTML, CSS, JavaScript, SQLite, Pytest.

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create and activate a virtual environment:
   - Windows: `py -m venv .venv` then `.venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Start the app: `python app.py`
6. Open `http://127.0.0.1:5000`.

## Run tests
```bash
pytest -q
```

## Sample diff
Use `samples/example.diff` in the home page to try the demo rules.

## Project structure
```text
app.py
config.py
app/
  __init__.py
  routes/
  services/
  database/
  templates/
  static/
tests/
samples/
docs/
```

## Important prototype boundaries
The rules are illustrative heuristics, not a complete static analyser. They can miss issues or flag valid code that needs context. The optional AI provider integration described in the case report is not connected in this first runnable version. Do not submit confidential source code to external services. This prototype is for academic demonstration, not production deployment.

## Case study report
See `docs/Case_72_Internal_Code_Review_Assistant_Report.docx`.
