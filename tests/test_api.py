from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db_session
from app.main import app


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db_session() -> Generator[Session, None, None]:
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db_session] = override_get_db_session
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_health_check(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Address Book API is running"


def test_create_and_fetch_address(client: TestClient) -> None:
    payload = {
        "label": "Home",
        "street": "221B Baker Street",
        "city": "London",
        "country": "United Kingdom",
        "latitude": 51.523767,
        "longitude": -0.1585557,
    }

    create_response = client.post("/api/v1/addresses", json=payload)
    assert create_response.status_code == 201

    address_id = create_response.json()["id"]
    get_response = client.get(f"/api/v1/addresses/{address_id}")

    assert get_response.status_code == 200
    assert get_response.json()["label"] == "Home"


def test_nearby_search_returns_created_address(client: TestClient) -> None:
    payload = {
        "label": "Office",
        "city": "London",
        "country": "United Kingdom",
        "latitude": 51.523767,
        "longitude": -0.1585557,
    }
    create_response = client.post("/api/v1/addresses", json=payload)
    assert create_response.status_code == 201

    nearby_response = client.get(
        "/api/v1/addresses/search/nearby",
        params={
            "latitude": 51.523767,
            "longitude": -0.1585557,
            "distance_km": 1,
        },
    )

    assert nearby_response.status_code == 200
    assert any(item["label"] == "Office" for item in nearby_response.json())
