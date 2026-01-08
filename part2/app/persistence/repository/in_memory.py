from __future__ import annotations

from typing import Dict, Generic, List, Optional, TypeVar, Callable

from .base_repository import BaseRepository

T = TypeVar("T")

class RepositoryError(Exception):
    pass

class NotFoundError(RepositoryError):
    pass

class ValidationError(RepositoryError):
    pass

class InMemoryRepository(BaseRepository[T], Generic[T]):
    def __init__(self) -> None:
        self._store: Dict[str, T] = {}

    def _validate_obj(self, obj: T) -> None:
        obj_id = getattr(obj, "id", None)
        if not obj_id or not isinstance(obj_id, str):
            raise ValidationError("Object must have a non-empty string 'id' attribute.")

    def add(self, obj: T) -> T:
        self._validate_obj(obj)
        obj_id = getattr(obj, "id")
        if obj_id in self._store:
            raise ValidationError(f"Object with id '{obj_id}' already exists.")
        self._store[obj_id] = obj
        return obj

    def get(self, obj_id: str) -> Optional[T]:
        return self._store.get(obj_id)

    def get_all(self) -> List[T]:
        return list(self._store.values())

    def exists(self, obj_id: str) -> bool:
        return obj_id in self._store

    def update(self, obj_id: str, **changes) -> T:
        obj = self._store.get(obj_id)
        if obj is None:
            raise NotFoundError(f"Object with id '{obj_id}' not found.")

        for key, value in changes.items():
            if not hasattr(obj, key):
                raise ValidationError(f"Cannot update unknown attribute '{key}'.")
            setattr(obj, key, value)

        touch = getattr(obj, "touch", None)
        if callable(touch):
            touch()

        self._store[obj_id] = obj
        return obj

    def delete(self, obj_id: str) -> None:
        if obj_id not in self._store:
            raise NotFoundError(f"Object with id '{obj_id}' not found.")
        del self._store[obj_id]

    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        return [obj for obj in self._store.values() if predicate(obj)]
