from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Callable

T = TypeVar("T")

class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    def add(self, obj: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def get(self, obj_id: str) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    def update(self, obj_id: str, **changes) -> T:
        raise NotImplementedError

    @abstractmethod
    def delete(self, obj_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def exists(self, obj_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        raise NotImplementedError
