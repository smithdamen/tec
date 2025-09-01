# TEC

![CI](https://github.com/smithdamen/tec/actions/workflows/ci.yml/badge.svg)

Server-first roguelike MMO prototype (terminal client).

## Current feature slices
- Server-authoritative tick loop & JSONL protocol
- Roguelike input (arrows, vi, numpad), centered viewport
- **Field of View**: Euclidean radius, day/night dynamic radius, explored memory (fog of war)
- CI: ruff / mypy / pytest guardrails

## Getting started
```bash
# first time in repo
direnv allow
make run-server     # terminal 1
make run-client     # terminal 2

# dev checks
make fmt && make lint && make test
