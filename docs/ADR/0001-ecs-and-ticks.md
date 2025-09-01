# 0001 – ECS and Fixed Tick
Status: Accepted
Context: We need modular systems and server-authoritative pacing that feels roguelike.
Decision: Dataclass ECS + 10Hz tick + per-action energy costs.
Consequences: Easy to test; deterministic; works for MMO later.
