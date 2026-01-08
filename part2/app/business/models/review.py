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


def _require_int(name: str, value: object, min_value: int | None = None, max_value: int | None = None) -> int:
    if isinstance(value, bool):
        raise ValidationError(f"{name} must be an integer.")
    try:
        v = int(value)
    except (TypeError, ValueError):
        raise ValidationError(f"{name} must be an integer.")
    if min_value is not None and v < min_value:
        raise ValidationError(f"{name} must be >= {min_value}.")
    if max_value is not None and v > max_value:
        raise ValidationError(f"{name} must be <= {max_value}.")
    return v


@dataclass
class Review(BaseModel):
    text: str = field(default="")
    rating: int = field(default=1)

    user_id: str = field(default="")   # relationship: Review -> User
    place_id: str = field(default="")  # relationship: Review -> Place

    def __post_init__(self) -> None:
        self.text = _require_str("text", self.text, 1, 1000)
        self.rating = _require_int("rating", self.rating, 1, 5)
        self.user_id = _require_str("user_id", self.user_id, 1, 64)
        self.place_id = _require_str("place_id", self.place_id, 1, 64)

    def update(self, **changes) -> None:
        allowed = {"text", "rating"}
        for key in changes:
            if key not in allowed:
                raise ValidationError(f"Cannot update unknown field '{key}' for Review.")

        if "text" in changes:
            self.text = _require_str("text", changes["text"], 1, 1000)
        if "rating" in changes:
            self.rating = _require_int("rating", changes["rating"], 1, 5)

        self.touch()

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
        })
        return data
