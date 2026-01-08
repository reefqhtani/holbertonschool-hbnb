from __future__ import annotations

from dataclasses import dataclass, field

from .base import BaseModel
from app.business.exceptions import ValidationError


def _require_str(name: str, value: object, min_len: int = 1, max_len: int | None = None) -> str:
    if not isinstance(value, str):
        raise ValidationError(f"{name} must be a string.")
    v = value.strip()
    if len(v) < min_len:
        raise ValidationError(f"{name} must be at least {min_len} characters.")
    if max_len is not None and len(v) > max_len:
        raise ValidationError(f"{name} must be at most {max_len} characters.")
    return v


@dataclass
class Amenity(BaseModel):
    name: str = field(default="")

    def __post_init__(self) -> None:
        self.name = _require_str("name", self.name, 1, 50)

    def update(self, **changes) -> None:
        allowed = {"name"}
        for key in changes:
            if key not in allowed:
                raise ValidationError(f"Cannot update unknown field '{key}' for Amenity.")
        if "name" in changes:
            self.name = _require_str("name", changes["name"], 1, 50)
        self.touch()

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({"name": self.name})
        return data
