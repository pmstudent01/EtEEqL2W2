"""Data models for the Vehicle Service SDK.

The Vehicle schema is derived from the Postman "Vehicle Service Collection"
request bodies:

    nickName : str
    vin      : str
    make     : str
    model    : str
    year     : str        (kept as a string to match the API contract)
    miles    : int
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, fields
from typing import Any, Dict, Optional


@dataclass
class Vehicle:
    """Represents a vehicle resource."""

    nickName: Optional[str] = None
    vin: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[str] = None
    miles: Optional[int] = None
    # The API assigns an id on creation; it is not part of the request body.
    id: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Vehicle":
        """Build a Vehicle from an API response dict, ignoring unknown keys."""
        known = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in (data or {}).items() if k in known})

    def to_payload(self) -> Dict[str, Any]:
        """Serialize to a request body, omitting ``id`` and ``None`` values."""
        data = asdict(self)
        data.pop("id", None)
        return {k: v for k, v in data.items() if v is not None}
