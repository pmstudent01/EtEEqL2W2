"""Exception types raised by the Vehicle Service SDK."""

from __future__ import annotations

from typing import Optional


class VehicleServiceError(Exception):
    """Base class for all SDK errors."""


class VehicleAPIError(VehicleServiceError):
    """Raised when the API returns an unexpected (non-success) status code."""

    def __init__(self, status_code: int, message: str, body: Optional[str] = None):
        self.status_code = status_code
        self.body = body
        super().__init__(f"[HTTP {status_code}] {message}")


class VehicleNotFoundError(VehicleAPIError):
    """Raised when a vehicle with the given id does not exist (HTTP 404)."""


class VehicleValidationError(VehicleAPIError):
    """Raised when the request payload is rejected by the API (HTTP 400/422)."""
