# ADR 0002 — Server-side FOV & Memory

## Context
We need authoritative visibility to prevent client exploits and to support lighting/stealth.

## Decision
- Compute FOV on the server using symmetric shadowcasting with Euclidean radius.
- Messages carry masked `tiles`, plus `base` (truth) and `mem` (explored).
- Walls are considered visible surfaces.
- Day/night modulates FOV radius; later: item lights & environment modifiers.

## Consequences
- Client code stays dumb about world truth; it just renders.
- Server snapshots are slightly larger (`base` & `mem`), but compress well and are simple.
- Future lighting and stealth can compose on server without protocol churn.
