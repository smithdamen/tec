# TEC Development Workflow

This project uses a **strict check → fix → test → commit → push** loop to keep the codebase clean and easy to grow.

---

## 🔄 Daily Workflow

Whenever you finish writing code or reach a stopping point:

# runs ruff format to auto-fix style (quotes, indentation, spacing)
make fmt

# runs ruff check --fix to find unused imports, long lines, multiple statements on one line, etc
# runs mypy to enforce static type correctness
# runs pytest
make lint

# shortcut for pytest -q and needs to be run when changing or adding logic
make test

# run the game
make run-server
make run-client

# adds all files
git add -A

# commit with clear message
# feat: new feature
# fix: bug fix
# docs: documentation only
# refactor: internal restructuring
# test: test-related changes
# chore: maintenance (tooling, configs, dependencies)
git commit -m "feat: <short description>"

# can also use git push origin main if not set up yet
git push

🔍 Pre-Commit Hooks
- Every git commit runs pre-commit hooks:
  - Ruff lint/format
  - Mypy type-check
  - Trailing whitespace / EOF newline fixes

If pre-commit makes auto-fixes:
  1. Run git add -A
  2. Commit again

✅ Summary
  1. Write code
  2. make fmt → format
  3. make lint → check (fix errors until clean)
  4. make test → verify logic
  5. git add -A && git commit -m "..." → save work
  6. git push → sync to GitHub

Keep this cycle tight. Short commits, clean diffs, green checks.

Run locally
  1. make run-server
  2. make run-client
