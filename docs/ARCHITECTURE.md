# Architecture

- tec.shared: ECS, components, systems, mapgen, fov, actions
- tec.server: simulation (ticks, energy), protocol (JSON Lines), TCP server
- tec.client: tcod roguelike client (100x40 viewport, FOV, keymap)

Dataflow: Client keys → Actions(JSON) → Server tick → World update → Events(JSON) → Client render
