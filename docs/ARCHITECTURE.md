# Architecture Overview

## Goals
- **Server-authoritative** simulation and visibility.
- Text client first; graphics-ready later.
- Modular systems (movement, needs, FOV, items) with small interfaces.

## Components
- **Server**
  - `tec.server.sim.Simulation` — tick loop, world time, action queues.
  - `tec.server.net.JsonServer` — async TCP, sessions, snapshots.
  - `tec.server.protocol` — JSONL event builders (strict shapes).
  - Systems: movement, needs, FOV.
- **Shared**
  - `tec.shared.world` — ECS-lite containers (entities, components).
  - `tec.shared.components` — Position, Actor, Needs, etc.
  - `tec.shared.fov` — symmetric shadowcasting (Euclidean cutoff).
  - `tec.shared.mapgen` — placeholder map generator.
- **Client (TUI)**
  - `tec.client.tcod_client` — draw loop, input mapping, network.
  - `tec.client.keymap` — roguelike key translation.
  - `ViewModel` — snapshot of server state for rendering.

## Data flow (happy path)
1. **Input** (KeyDown) → client sends action (`MOVE`, `WAIT`).
2. **Server** enqueues action; on tick resolves if energy suffices.
3. After input (and periodically), **server sends snapshot**:
   - `POS` (player world coords),
   - `VIEW` (top-left origin, masked `tiles`, plus `base` & `mem`),
   - `STATS` (derived).
4. **Client** renders: visible tiles; explored dim tiles; draws `@` at `POS - VIEW.origin`.

## Authoritative visibility
- FOV computed on server; client never gets unearned info.
- Protocol masks `tiles` for current visibility, and separately sends `base` (true glyphs) & `mem` (explored).
- Future: stealth, lighting levels, multi-light composition remain server-side.
