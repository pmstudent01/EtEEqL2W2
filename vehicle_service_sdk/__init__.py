"""Vehicle Service SDK.

A lightweight Python client for the Vehicle Service REST API, derived from the
Postman "Vehicle Service Collection".

Exposes a full CRUD interface over the /vehicles resource:
    - create_vehicle
    - list_vehicles
    - get_vehicle
    - update_vehicle
    - delete_vehicle
"""

from .client import VehicleServiceClient
from .models import Vehicle
from .errors import (
    VehicleServiceError,
    VehicleNotFoundError,
    VehicleValidationError,
    VehicleAPIError,
)

__all__ = [
    "VehicleServiceClient",
    "Vehicle",
    "VehicleServiceError",
    "VehicleNotFoundError",
    "VehicleValidationError",
    "VehicleAPIError",
]

__version__ = "1.0.0"
