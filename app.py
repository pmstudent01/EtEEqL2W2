"""Demo app for the Vehicle Service API.

Implements the full CRUD workflow using the generated Vehicle Service SDK,
mirroring the requests in the Postman "Vehicle Service Collection".

Usage:
    pip install -r requirements.txt
    # Point at your running service / Postman mock server:
    set BASE_URL=http://localhost:3000        (Windows)
    export BASE_URL=http://localhost:3000     (macOS/Linux)
    python app.py
"""

from __future__ import annotations

import os
import sys

from vehicle_service_sdk import (
    VehicleServiceClient,
    Vehicle,
    VehicleServiceError,
)


def main() -> int:
    base_url = os.environ.get("BASE_URL", "http://localhost:3000")
    api_key = os.environ.get("API_KEY")  # optional; maps to {{vault:apiKey}}

    print(f"Connecting to Vehicle Service at: {base_url}\n")

    with VehicleServiceClient(base_url=base_url, api_key=api_key) as client:
        try:
            # 1. Create a vehicle  (POST /vehicles)
            new_vehicle = Vehicle(
                nickName="The Lisa Marie",
                vin="4M2DV11W4RDJ53329",
                make="Mercury",
                model="Villager",
                year="1994",
                miles=159864,
            )
            created = client.create_vehicle(new_vehicle)
            print(f"Created vehicle: {created}")

            vehicle_id = created.id if created.id is not None else 1

            # 2. List all vehicles  (GET /vehicles)
            vehicles = client.list_vehicles()
            print(f"\nAll vehicles ({len(vehicles)}):")
            for v in vehicles:
                print(f"  - {v}")

            # 3. Retrieve one vehicle  (GET /vehicles/:id)
            fetched = client.get_vehicle(vehicle_id)
            print(f"\nRetrieved vehicle {vehicle_id}: {fetched}")

            # 4. Update the vehicle  (PATCH /vehicles/:id)
            updated = client.update_vehicle(vehicle_id, {"miles": 159999})
            print(f"\nUpdated vehicle {vehicle_id}: {updated}")

            # 5. Delete the vehicle  (DELETE /vehicles/:id)
            client.delete_vehicle(vehicle_id)
            print(f"\nDeleted vehicle {vehicle_id}. Done.")

        except VehicleServiceError as exc:
            print(f"\nVehicle Service error: {exc}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
