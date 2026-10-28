"""HTTP client for the Vehicle Service API.

Each method maps directly to a request in the Postman "Vehicle Service Collection":

    POST   /vehicles       -> create_vehicle   (expects 201)
    GET    /vehicles       -> list_vehicles    (expects 200)
    GET    /vehicles/:id    -> get_vehicle      (expects 200)
    PATCH  /vehicles/:id    -> update_vehicle   (expects 200)
    DELETE /vehicles/:id    -> delete_vehicle   (expects 204)
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

import requests

from .models import Vehicle
from .errors import (
    VehicleAPIError,
    VehicleNotFoundError,
    VehicleValidationError,
)


class VehicleServiceClient:
    """Client for the Vehicle Service API.

    Args:
        base_url: Base URL of the service, e.g. ``http://localhost:3000``.
                  Corresponds to the ``{{baseUrl}}`` variable in the collection.
        api_key:  Optional API key. When provided it is sent as the
                  ``x-api-key`` header (maps to the ``{{vault:apiKey}}`` value).
        timeout:  Per-request timeout in seconds.
        session:  Optional pre-configured ``requests.Session``.
    """

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: float = 30.0,
        session: Optional[requests.Session] = None,
    ) -> None:
        if not base_url:
            raise ValueError("base_url is required")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = session or requests.Session()
        self._session.headers.update({"Accept": "application/json"})
        if api_key:
            self._session.headers.update({"x-api-key": api_key})

    # ----------------------------------------------------------------- helpers
    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _request(
        self,
        method: str,
        path: str,
        json_body: Optional[Dict[str, Any]] = None,
        expected: Union[int, tuple] = 200,
    ) -> requests.Response:
        try:
            response = self._session.request(
                method,
                self._url(path),
                json=json_body,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:  # network-level failure
            raise VehicleAPIError(0, f"Request failed: {exc}") from exc

        expected_codes = (expected,) if isinstance(expected, int) else expected
        if response.status_code not in expected_codes:
            self._raise_for_status(response)
        return response

    @staticmethod
    def _raise_for_status(response: requests.Response) -> None:
        body = response.text
        code = response.status_code
        if code == 404:
            raise VehicleNotFoundError(code, "Vehicle not found", body)
        if code in (400, 422):
            raise VehicleValidationError(code, "Invalid vehicle payload", body)
        raise VehicleAPIError(code, "Unexpected response from Vehicle Service", body)

    @staticmethod
    def _as_vehicle(data: Any) -> Vehicle:
        if isinstance(data, dict):
            return Vehicle.from_dict(data)
        return Vehicle()

    # ------------------------------------------------------------- operations
    def create_vehicle(self, vehicle: Union[Vehicle, Dict[str, Any]]) -> Vehicle:
        """Create a vehicle. Maps to ``POST /vehicles`` (expects HTTP 201)."""
        payload = vehicle.to_payload() if isinstance(vehicle, Vehicle) else dict(vehicle)
        response = self._request("POST", "/vehicles", json_body=payload, expected=201)
        return self._as_vehicle(self._safe_json(response))

    def list_vehicles(self) -> List[Vehicle]:
        """List all vehicles. Maps to ``GET /vehicles`` (expects HTTP 200)."""
        response = self._request("GET", "/vehicles", expected=200)
        data = self._safe_json(response)
        items = data if isinstance(data, list) else data.get("vehicles", []) if isinstance(data, dict) else []
        return [self._as_vehicle(item) for item in items]

    def get_vehicle(self, vehicle_id: Union[int, str]) -> Vehicle:
        """Retrieve one vehicle. Maps to ``GET /vehicles/:id`` (expects HTTP 200)."""
        response = self._request("GET", f"/vehicles/{vehicle_id}", expected=200)
        return self._as_vehicle(self._safe_json(response))

    def update_vehicle(
        self,
        vehicle_id: Union[int, str],
        changes: Union[Vehicle, Dict[str, Any]],
    ) -> Vehicle:
        """Update a vehicle. Maps to ``PATCH /vehicles/:id`` (expects HTTP 200)."""
        payload = changes.to_payload() if isinstance(changes, Vehicle) else dict(changes)
        response = self._request(
            "PATCH", f"/vehicles/{vehicle_id}", json_body=payload, expected=200
        )
        return self._as_vehicle(self._safe_json(response))

    def delete_vehicle(self, vehicle_id: Union[int, str]) -> None:
        """Delete a vehicle. Maps to ``DELETE /vehicles/:id`` (expects HTTP 204)."""
        self._request("DELETE", f"/vehicles/{vehicle_id}", expected=(204, 200))

    # --------------------------------------------------------------- internals
    @staticmethod
    def _safe_json(response: requests.Response) -> Any:
        if not response.content:
            return {}
        try:
            return response.json()
        except ValueError:
            return {}

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> "VehicleServiceClient":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()
