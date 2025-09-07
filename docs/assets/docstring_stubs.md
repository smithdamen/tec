# Docstring stubs (auto-generated)
_Paste these inside the indicated module/class/function as the first statement._

## src/tec/__init__.py

**Module docstring (paste at very top):**

```python
"""TODO: Module summary for src/tec/__init__.py.

Key concepts:
- TODO
"""
```


## src/tec/client/keymap.py

**Module docstring (paste at very top):**

```python
"""TODO: Module summary for src/tec/client/keymap.py.

Key concepts:
- TODO
"""
```


## src/tec/client/tcod_client.py

**Module docstring (paste at very top):**

```python
"""TODO: Module summary for src/tec/client/tcod_client.py.

Key concepts:
- TODO
"""
```

**Class `ViewModel` docstring (paste inside class at line 22):**

```python
"""TODO: Summary for `ViewModel`.

Attributes:
    TODO
"""
```

**Class `Client` docstring (paste inside class at line 39):**

```python
"""TODO: Summary for `Client`.

Attributes:
    TODO
"""
```

**Method `Client.connect` docstring (paste inside method at line 49):**

```python
"""TODO: Summary for `connect`.

Args:
    host: str: TODO.
    port: int: TODO.
    name: str: TODO.

Returns:
    None: TODO.

Raises:
    (none)

"""
```

**Method `Client.send` docstring (paste inside method at line 54):**

```python
"""TODO: Summary for `send`.

Args:
    action: Action: TODO.

Returns:
    None: TODO.

Raises:
    (none)

"""
```

**Method `Client.recv_loop` docstring (paste inside method at line 58):**

```python
"""TODO: Summary for `recv_loop`.

Args:
    (none)

Returns:
    None: TODO.

Raises:
    (none)

"""
```

**Method `Client.draw` docstring (paste inside method at line 129):**

```python
"""TODO: Summary for `draw`.

Args:
    console: tcod.console.Console: TODO.

Returns:
    None: TODO.

Raises:
    (none)

"""
```

**Method `Client.run` docstring (paste inside method at line 209):**

```python
"""TODO: Summary for `run`.

Args:
    (none)

Returns:
    None: TODO.

Raises:
    (none)

"""
```

**Function `main` docstring (paste inside function at line 276):**

```python
"""TODO: Summary for `main`.

Args:
    (none)

Returns:
    None: TODO.

Raises:
    (none)

"""
```


## src/tec/server/main.py

**Module docstring (paste at very top):**

```python
"""TODO: Module summary for src/tec/server/main.py.

Key concepts:
- TODO
"""
```

**Function `sim_loop` docstring (paste inside function at line 8):**

```python
"""TODO: Summary for `sim_loop`.

Args:
    sim: Simulation: TODO.

Returns:
    None: TODO.

Raises:
    (none)

"""
```

**Function `main` docstring (paste inside function at line 18):**

```python
"""TODO: Summary for `main`.

Args:
    (none)

Returns:
    None: TODO.

Raises:
    (none)

"""
```


## src/tec/server/net.py

**Module docstring (paste at very top):**

```python
"""TODO: Module summary for src/tec/server/net.py.

Key concepts:
- TODO
"""
```

**Class `JsonServer` docstring (paste inside class at line 14):**

```python
"""TODO: Summary for `JsonServer`.

Attributes:
    TODO
"""
```

**Method `JsonServer.handle_client` docstring (paste inside method at line 59):**

```python
"""TODO: Summary for `handle_client`.

Args:
    reader: asyncio.StreamReader: TODO.
    writer: asyncio.StreamWriter: TODO.

Returns:
    None: TODO.

Raises:
    (none)

"""
```

**Method `JsonServer.dispatch` docstring (paste inside method at line 117):**

```python
"""TODO: Summary for `dispatch`.

Args:
    msg: dict[str, Any]: TODO.
    writer: asyncio.StreamWriter: TODO.
    eid: int: TODO.

Returns:
    None: TODO.

Raises:
    (none)

"""
```

**Method `JsonServer.start` docstring (paste inside method at line 147):**

```python
"""TODO: Summary for `start`.

Args:
    (none)

Returns:
    None: TODO.

Raises:
    (none)

"""
```


## src/tec/server/protocol.py

**Module docstring (paste at very top):**

```python
"""TODO: Module summary for src/tec/server/protocol.py.

Key concepts:
- TODO
"""
```

**Function `ev_welcome` docstring (paste inside function at line 9):**

```python
"""TODO: Summary for `ev_welcome`.

Args:
    msg: str: TODO.

Returns:
    bytes: TODO.

Raises:
    (none)

"""
```

**Function `ev_pos` docstring (paste inside function at line 13):**

```python
"""TODO: Summary for `ev_pos`.

Args:
    x: int: TODO.
    y: int: TODO.

Returns:
    bytes: TODO.

Raises:
    (none)

"""
```

**Function `ev_stats` docstring (paste inside function at line 73):**

```python
"""TODO: Summary for `ev_stats`.

Args:
    speed: float: TODO.
    energy: float: TODO.
    aps: float: TODO.
    eta: float: TODO.

Returns:
    bytes: TODO.

Raises:
    (none)

"""
```

**Function `derive_stats` docstring (paste inside function at line 84):**

```python
"""TODO: Summary for `derive_stats`.

Args:
    actor: Actor: TODO.
    move_cost: float: TODO.

Returns:
    dict[str, float]: TODO.

Raises:
    (none)

"""
```


## src/tec/server/sim.py

**Module docstring (paste at very top):**

```python
"""TODO: Module summary for src/tec/server/sim.py.

Key concepts:
- TODO
"""
```

**Class `Simulation` docstring (paste inside class at line 20):**

```python
"""TODO: Summary for `Simulation`.

Attributes:
    TODO
"""
```

**Method `Simulation.ensure_queue` docstring (paste inside method at line 27):**

```python
"""TODO: Summary for `ensure_queue`.

Args:
    eid: EID: TODO.

Returns:
    deque[Action]: TODO.

Raises:
    (none)

"""
```

**Method `Simulation.spawn_player` docstring (paste inside method at line 30):**

```python
"""TODO: Summary for `spawn_player`.

Args:
    (none)

Returns:
    EID: TODO.

Raises:
    (none)

"""
```

**Method `Simulation.enqueue_move` docstring (paste inside method at line 38):**

```python
"""TODO: Summary for `enqueue_move`.

Args:
    eid: EID: TODO.
    dx: int: TODO.
    dy: int: TODO.

Returns:
    None: TODO.

Raises:
    (none)

"""
```

**Method `Simulation.enqueue_wait` docstring (paste inside method at line 41):**

```python
"""TODO: Summary for `enqueue_wait`.

Args:
    eid: EID: TODO.

Returns:
    None: TODO.

Raises:
    (none)

"""
```

**Method `Simulation.tick` docstring (paste inside method at line 44):**

```python
"""TODO: Summary for `tick`.

Args:
    (none)

Returns:
    None: TODO.

Raises:
    (none)

"""
```


## src/tec/settings.py

**Module docstring (paste at very top):**

```python
"""TODO: Module summary for src/tec/settings.py.

Key concepts:
- TODO
"""
```

**Class `Settings` docstring (paste inside class at line 5):**

```python
"""TODO: Summary for `Settings`.

Attributes:
    TODO
"""
```


## src/tec/shared/actions.py

**Module docstring (paste at very top):**

```python
"""TODO: Module summary for src/tec/shared/actions.py.

Key concepts:
- TODO
"""
```

**Class `ActLogin` docstring (paste inside class at line 6):**

```python
"""TODO: Summary for `ActLogin`.

Attributes:
    TODO
"""
```

**Class `ActMove` docstring (paste inside class at line 12):**

```python
"""TODO: Summary for `ActMove`.

Attributes:
    TODO
"""
```

**Class `ActWait` docstring (paste inside class at line 19):**

```python
"""TODO: Summary for `ActWait`.

Attributes:
    TODO
"""
```


## src/tec/shared/components.py

**Module docstring (paste at very top):**

```python
"""TODO: Module summary for src/tec/shared/components.py.

Key concepts:
- TODO
"""
```

**Class `Position` docstring (paste inside class at line 5):**

```python
"""TODO: Summary for `Position`.

Attributes:
    TODO
"""
```

**Class `Actor` docstring (paste inside class at line 11):**

```python
"""TODO: Summary for `Actor`.

Attributes:
    TODO
"""
```

**Class `PlayerTag` docstring (paste inside class at line 17):**

```python
"""TODO: Summary for `PlayerTag`.

Attributes:
    TODO
"""
```

**Class `Needs` docstring (paste inside class at line 22):**

```python
"""TODO: Summary for `Needs`.

Attributes:
    TODO
"""
```


## src/tec/shared/fov.py

**Module docstring (paste at very top):**

```python
"""TODO: Module summary for src/tec/shared/fov.py.

Key concepts:
- TODO
"""
```


## src/tec/shared/mapgen.py

**Module docstring (paste at very top):**

```python
"""TODO: Module summary for src/tec/shared/mapgen.py.

Key concepts:
- TODO
"""
```

**Function `generate_map` docstring (paste inside function at line 6):**

```python
"""TODO: Summary for `generate_map`.

Args:
    width: int: TODO.
    height: int: TODO.
    seed: int: TODO.

Returns:
    list[list[bool]]: TODO.

Raises:
    (none)

"""
```


## src/tec/shared/systems/movement.py

**Module docstring (paste at very top):**

```python
"""TODO: Module summary for src/tec/shared/systems/movement.py.

Key concepts:
- TODO
"""
```

**Function `try_move` docstring (paste inside function at line 4):**

```python
"""TODO: Summary for `try_move`.

Args:
    pos: Position: TODO.
    dx: int: TODO.
    dy: int: TODO.
    tiles: list[list[bool]]: TODO.

Returns:
    None: TODO.

Raises:
    (none)

"""
```


## src/tec/shared/systems/needs.py

**Module docstring (paste at very top):**

```python
"""TODO: Module summary for src/tec/shared/systems/needs.py.

Key concepts:
- TODO
"""
```

**Function `tick_needs` docstring (paste inside function at line 6):**

```python
"""TODO: Summary for `tick_needs`.

Args:
    needs: Needs: TODO.
    actor: Actor: TODO.

Returns:
    None: TODO.

Raises:
    (none)

"""
```


## src/tec/shared/types.py

**Module docstring (paste at very top):**

```python
"""TODO: Module summary for src/tec/shared/types.py.

Key concepts:
- TODO
"""
```

**Class `MsgWelcome` docstring (paste inside class at line 6):**

```python
"""TODO: Summary for `MsgWelcome`.

Attributes:
    TODO
"""
```

**Class `MsgPos` docstring (paste inside class at line 11):**

```python
"""TODO: Summary for `MsgPos`.

Attributes:
    TODO
"""
```

**Class `MsgView` docstring (paste inside class at line 17):**

```python
"""TODO: Summary for `MsgView`.

Attributes:
    TODO
"""
```

**Class `MsgLog` docstring (paste inside class at line 26):**

```python
"""TODO: Summary for `MsgLog`.

Attributes:
    TODO
"""
```

**Class `MsgStats` docstring (paste inside class at line 31):**

```python
"""TODO: Summary for `MsgStats`.

Attributes:
    TODO
"""
```


## src/tec/shared/world.py

**Module docstring (paste at very top):**

```python
"""TODO: Module summary for src/tec/shared/world.py.

Key concepts:
- TODO
"""
```

**Class `World` docstring (paste inside class at line 12):**

```python
"""TODO: Summary for `World`.

Attributes:
    TODO
"""
```

**Method `World.create` docstring (paste inside method at line 16):**

```python
"""TODO: Summary for `create`.

Args:
    (none)

Returns:
    EID: TODO.

Raises:
    (none)

"""
```

**Method `World.add` docstring (paste inside method at line 21):**

```python
"""TODO: Summary for `add`.

Args:
    eid: EID: TODO.
    comp: object: TODO.

Returns:
    None: TODO.

Raises:
    (none)

"""
```

**Method `World.get` docstring (paste inside method at line 24):**

```python
"""TODO: Summary for `get`.

Args:
    ctype: type[T]: TODO.

Returns:
    MutableMapping[EID, T]: TODO.

Raises:
    (none)

"""
```

**Method `World.entities_with` docstring (paste inside method at line 27):**

```python
"""TODO: Summary for `entities_with`.

Args:
    *ctypes: type[object]: TODO.

Returns:
    Iterable[EID]: TODO.

Raises:
    (none)

"""
```
