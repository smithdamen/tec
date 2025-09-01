# Coding Standards

- **Layout:** `src/tec` + `tests`.
- **Typing:** PEP 484/604, `mypy` strict. No `Any` unless unavoidable.
- **Style:** `ruff` clean; 100-col limit; one statement per line.
- **Server is authoritative.** All client actions go to server; server sends events.
- **Protocol:** JSON Lines, message has `"type"` plus a stable schema. Document changes in `docs/PROTOCOL.md`.
- **Small PRs:** Prefer < 300 lines per change; split otherwise.
- **Tests:** Add at least one pytest for new server behavior or protocol shapes.
- **Docs:** Update GDD/ARCHITECTURE/ADR when you make an architectural change.
