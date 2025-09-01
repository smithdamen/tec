# Coding Standards

- Layout: `src/tec` and `tests`. `src` layout imports as `from tec...`.
- Typing: PEP 484/604; `mypy` clean. No untyped defs in `src`; tests may be lighter but typed helpers preferred.
- Style: `ruff` clean; 100-col max; one statement per line.
- Messages: JSON Lines with `"type"`, documented in `docs/PROTOCOL.md`.
- Small PRs: aim for <300 LOC; split otherwise.
- Tests: add at least one test for each new server behavior or protocol change.
- Docs: update `ARCHITECTURE.md`, `PROTOCOL.md`, and `GDD.md` when behavior that users see changes.
