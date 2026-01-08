from __future__ import annotations

from typing import Dict, Any
from app.persistence.repository.in_memory import InMemoryRepository

class HBnBFacade:
    """
    Facade to decouple Presentation (API) from Persistence (repositories).
    """

    def __init__(self) -> None:
        self._repos: Dict[str, InMemoryRepository] = {
            "users": InMemoryRepository(),
            "places": InMemoryRepository(),
            "reviews": InMemoryRepository(),
            "amenities": InMemoryRepository(),
        }

    def repo(self, name: str) -> InMemoryRepository:
        if name not in self._repos:
            raise ValueError(f"Unknown repository '{name}'")
        return self._repos[name]

    def create(self, repo_name: str, obj: Any) -> Any:
        return self.repo(repo_name).add(obj)

    def get(self, repo_name: str, obj_id: str) -> Any:
        return self.repo(repo_name).get(obj_id)

    def list(self, repo_name: str) -> list:
        return self.repo(repo_name).get_all()
