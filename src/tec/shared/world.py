"""Minimal ECS-style world with typed component tables."""

from __future__ import annotations

from collections.abc import Iterable, MutableMapping
from dataclasses import dataclass, field
from typing import TypeVar

EID = int
T = TypeVar("T")


@dataclass
class World:
    """Entity id allocator and component storage."""

    next_id: int = 1
    tables: dict[type[object], MutableMapping[EID, object]] = field(default_factory=dict)

    def create(self) -> EID:
        """Allocate and return a fresh entity id."""
        eid = self.next_id
        self.next_id += 1
        return eid

    def add(self, eid: EID, comp: object) -> None:
        """Attach a component instance to an entity."""
        self.tables.setdefault(type(comp), {})[eid] = comp

    def get(self, ctype: type[T]) -> MutableMapping[EID, T]:
        """Get (and create if missing) the table for a component type."""
        return self.tables.setdefault(ctype, {})  # type: ignore[return-value]

    def entities_with(self, *ctypes: type[object]) -> Iterable[EID]:
        """Yield entity ids that have all of the given component types.

        Args:
            *ctypes: Component classes to match.

        Returns:
            Iterable of entity ids possessing all listed components.
        """
        if not ctypes:
            return []
        tables = [self.get(t) for t in ctypes]
        tables.sort(key=lambda t: len(t))
        ids = set(tables[0].keys())
        for t in tables[1:]:
            ids &= set(t.keys())
        return ids
