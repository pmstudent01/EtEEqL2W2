# Vehicle Service SDK + Demo App (Python)

A Python implementation of the Vehicle Service API, derived from the Postman
**Vehicle Service Collection**. It contains:

- `vehicle_service_sdk/` — a reusable SDK client
- `app.py` — a runnable demo that exercises the full CRUD flow

## API surface

| SDK method                         | HTTP request            | Expected status |
|------------------------------------|-------------------------|-----------------|
| `create_vehicle(vehicle)`          | `POST /vehicles`        | 201             |
| `list_vehicles()`                  | `GET /vehicles`         | 200             |
| `get_vehicle(id)`                  | `GET /vehicles/:id`     | 200             |
| `update_vehicle(id, changes)`      | `PATCH /vehicles/:id`   | 200             |
| `delete_vehicle(id)`               | `DELETE /vehicles/:id`  | 204             |

### Vehicle model
`nickName` (str), `vin` (str), `make` (str), `model` (str), `year` (str), `miles` (int).

## Install

```bash
pip install -r requirements.txt
```

## Usage

```python
from vehicle_service_sdk import VehicleServiceClient, Vehicle

client = VehicleServiceClient(base_url="http://localhost:3000", api_key="optional")

created = client.create_vehicle(Vehicle(
    nickName="The Lisa Marie", vin="4M2DV11W4RDJ53329",
    make="Mercury", model="Villager", year="1994", miles=159864,
))

vehicles = client.list_vehicles()
one = client.get_vehicle(created.id or 1)
client.update_vehicle(created.id or 1, {"miles": 159999})
client.delete_vehicle(created.id or 1)
```

## Run the demo

Point `BASE_URL` at your running service or Postman mock server
(`{{baseUrl}}` in the collection):

```bash
# Windows
set BASE_URL=http://localhost:3000 && python app.py

# macOS / Linux
BASE_URL=http://localhost:3000 python app.py
```

Set `API_KEY` if your service requires the `x-api-key` header
(maps to the `{{vault:apiKey}}` value in the workspace).

## Errors

All errors subclass `VehicleServiceError`:
`VehicleNotFoundError` (404), `VehicleValidationError` (400/422),
and `VehicleAPIError` (other non-success responses).
