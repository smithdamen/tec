from __future__ import annotations

from collections.abc import Iterable, MutableMapping
from dataclasses import dataclass, field
from typing import TypeVar

EID = int
T = TypeVar("T")


@dataclass
class World:
    next_id: int = 1
    tables: dict[type[object], MutableMapping[EID, object]] = field(default_factory=dict)

    def create(self) -> EID:
        eid = self.next_id
        self.next_id += 1
        return eid

    def add(self, eid: EID, comp: object) -> None:
        self.tables.setdefault(type(comp), {})[eid] = comp

    def get(self, ctype: type[T]) -> MutableMapping[EID, T]:
        return self.tables.setdefault(ctype, {})  # type: ignore[return-value]

    def entities_with(self, *ctypes: type[object]) -> Iterable[EID]:
        if not ctypes:
            return []
        tables = [self.get(t) for t in ctypes]
        tables.sort(key=lambda t: len(t))
        ids = set(tables[0].keys())
        for t in tables[1:]:
            ids &= set(t.keys())
        return ids
