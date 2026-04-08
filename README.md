# Address Book API

This project implements the Eastvantage FastAPI assignment as a small address book service. It lets API consumers create, update, delete, list, and search addresses stored in SQLite. Address coordinates are validated at the API boundary, and nearby searches are calculated using geodesic distance.

## Features

- FastAPI application with built-in Swagger UI
- SQLite persistence through SQLAlchemy ORM
- Input validation with Pydantic
- CRUD endpoints for address records
- Nearby address search by latitude, longitude, and distance in kilometers
- Environment-based configuration
- Application logging for major request and persistence events
- Basic API tests with `pytest`

## Project Structure

```text
app/
  api/routes/addresses.py
  core/config.py
  core/logging.py
  db/base.py
  db/session.py
  main.py
  models.py
  schemas.py
  services/address_service.py
tests/
  test_api.py
```

## Requirements

- Python 3.11 to 3.13 recommended
- `pip`

## Run The Application

1. Create a virtual environment:

```powershell
python -m venv .venv
```

2. Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Copy the example environment file:

```powershell
Copy-Item .env.example .env
```

5. Start the API:

```powershell
python -m uvicorn app.main:app --reload
```

6. Open the docs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

- `GET /` - health check
- `GET /api/v1/addresses` - list all addresses
- `POST /api/v1/addresses` - create an address
- `GET /api/v1/addresses/{address_id}` - fetch a single address
- `PUT /api/v1/addresses/{address_id}` - update an address
- `DELETE /api/v1/addresses/{address_id}` - delete an address
- `GET /api/v1/addresses/search/nearby?latitude=...&longitude=...&distance_km=...` - search nearby addresses

## Example Request

```powershell
curl -Method POST "http://127.0.0.1:8000/api/v1/addresses" `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"label":"Home","street":"221B Baker Street","city":"London","country":"United Kingdom","latitude":51.523767,"longitude":-0.1585557}'
```

## Run Tests

```powershell
pytest
```

## Notes

- The SQLite database file is created automatically on first startup.
- Coordinates are validated using latitude and longitude bounds.
- Nearby searches use `geopy.distance.geodesic` for accurate distance calculation.
