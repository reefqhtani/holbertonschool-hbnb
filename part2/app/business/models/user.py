from __future__ import annotations

from dataclasses import dataclass, field
import re

from .base import BaseModel
from app.business.exceptions import ValidationError

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


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
class User(BaseModel):
    email: str = field(default="")
    first_name: str = field(default="")
    last_name: str = field(default="")
    password: str = field(default="")  # auth/hashing will be handled in Part 3+

    def __post_init__(self) -> None:
        self.email = self._validate_email(self.email)
        self.first_name = _require_str("first_name", self.first_name, min_len=1, max_len=50)
        self.last_name = _require_str("last_name", self.last_name, min_len=1, max_len=50)

        # Keep password validation light in Part 2 (no hashing yet)
        if self.password:
            self.password = _require_str("password", self.password, min_len=6, max_len=128)

    @staticmethod
    def _validate_email(email: object) -> str:
        e = _require_str("email", email, min_len=3, max_len=254).lower()
        if not _EMAIL_RE.match(e):
            raise ValidationError("email must be a valid email address.")
        return e

    def update(self, **changes) -> None:
        allowed = {"email", "first_name", "last_name", "password"}
        for key in changes:
            if key not in allowed:
                raise ValidationError(f"Cannot update unknown field '{key}' for User.")

        if "email" in changes:
            self.email = self._validate_email(changes["email"])
        if "first_name" in changes:
            self.first_name = _require_str("first_name", changes["first_name"], 1, 50)
        if "last_name" in changes:
            self.last_name = _require_str("last_name", changes["last_name"], 1, 50)
        if "password" in changes:
            # still plain for Part 2
            self.password = _require_str("password", changes["password"], 6, 128)

        self.touch()

    def to_dict(self) -> dict:
        # NOTE: In real systems, never expose password.
        # For Part 2, keep it excluded.
        data = super().to_dict()
        data.update({
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
        })
        return data
