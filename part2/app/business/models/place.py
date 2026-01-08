from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

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


def _require_float(name: str, value: object, min_value: float | None = None, max_value: float | None = None) -> float:
    try:
        v = float(value)
    except (TypeError, ValueError):
        raise ValidationError(f"{name} must be a number.")
    if min_value is not None and v < min_value:
        raise ValidationError(f"{name} must be >= {min_value}.")
    if max_value is not None and v > max_value:
        raise ValidationError(f"{name} must be <= {max_value}.")
    return v


@dataclass
class Place(BaseModel):
    title: str = field(default="")
    description: str = field(default="")
    price_per_night: float = field(default=0.0)
    latitude: float = field(default=0.0)
    longitude: float = field(default=0.0)

    owner_id: str = field(default="")  # relationship: Place -> User
    amenity_ids: List[str] = field(default_factory=list)  # relationship: Place <-> Amenity (many-to-many style)

    def __post_init__(self) -> None:
        self.title = _require_str("title", self.title, 1, 100)
        # description can be empty but must be string
        if not isinstance(self.description, str):
            raise ValidationError("description must be a string.")
        if len(self.description) > 1000:
            raise ValidationError("description must be at most 1000 characters.")
        self.description = self.description.strip()

        self.price_per_night = _require_float("price_per_night", self.price_per_night, min_value=0.0)
        self.latitude = _require_float("latitude", self.latitude, min_value=-90.0, max_value=90.0)
        self.longitude = _require_float("longitude", self.longitude, min_value=-180.0, max_value=180.0)

        self.owner_id = _require_str("owner_id", self.owner_id, 1, 64)

        # normalize amenity ids
        if not isinstance(self.amenity_ids, list):
            raise ValidationError("amenity_ids must be a list of strings.")
        self.amenity_ids = self._normalize_ids(self.amenity_ids)

    @staticmethod
    def _normalize_ids(ids: list) -> list[str]:
        out: list[str] = []
        for x in ids:
            if not isinstance(x, str) or not x.strip():
                raise ValidationError("amenity_ids must contain non-empty strings.")
            val = x.strip()
            if val not in out:
                out.append(val)
        return out

    # Relationship helpers
    def add_amenity(self, amenity_id: str) -> None:
        aid = _require_str("amenity_id", amenity_id, 1, 64)
        if aid not in self.amenity_ids:
            self.amenity_ids.append(aid)
            self.touch()

    def remove_amenity(self, amenity_id: str) -> None:
        aid = _require_str("amenity_id", amenity_id, 1, 64)
        if aid in self.amenity_ids:
            self.amenity_ids.remove(aid)
            self.touch()

    def update(self, **changes) -> None:
        allowed = {
            "title", "description", "price_per_night",
            "latitude", "longitude", "owner_id",
            "amenity_ids"
        }
        for key in changes:
            if key not in allowed:
                raise ValidationError(f"Cannot update unknown field '{key}' for Place.")

        if "title" in changes:
            self.title = _require_str("title", changes["title"], 1, 100)
        if "description" in changes:
            if not isinstance(changes["description"], str):
                raise ValidationError("description must be a string.")
            if len(changes["description"]) > 1000:
                raise ValidationError("description must be at most 1000 characters.")
            self.description = changes["description"].strip()

        if "price_per_night" in changes:
            self.price_per_night = _require_float("price_per_night", changes["price_per_night"], 0.0)
        if "latitude" in changes:
            self.latitude = _require_float("latitude", changes["latitude"], -90.0, 90.0)
        if "longitude" in changes:
            self.longitude = _require_float("longitude", changes["longitude"], -180.0, 180.0)

        if "owner_id" in changes:
            self.owner_id = _require_str("owner_id", changes["owner_id"], 1, 64)

        if "amenity_ids" in changes:
            if not isinstance(changes["amenity_ids"], list):
                raise ValidationError("amenity_ids must be a list of strings.")
            self.amenity_ids = self._normalize_ids(changes["amenity_ids"])

        self.touch()

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "title": self.title,
            "description": self.description,
            "price_per_night": self.price_per_night,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "amenity_ids": list(self.amenity_ids),
        })
        return data
