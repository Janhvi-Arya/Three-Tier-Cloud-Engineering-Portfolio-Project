import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import create_app
from app.repository import ServiceRepository
from app.services import CloudOpsService


TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"


@pytest.fixture
def client():
    app = create_app(TEST_DATABASE_URL)
    with TestClient(app) as test_client:
        yield test_client


def login(client, username: str, password: str) -> dict[str, str]:
    response = client.post(
        "/api/auth/login",
        json={"username": username, "password": password},
    )
    access_token = response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def service_layer():
    return CloudOpsService(ServiceRepository())


@pytest.fixture
def app_session():
    app = create_app(TEST_DATABASE_URL)
    with TestClient(app):
        session_factory = app.state.session_factory
        session = session_factory()
        try:
            yield session
        finally:
            session.close()


@pytest.fixture
def admin_headers(client):
    return login(client, "admin", "AdminPass123!")


@pytest.fixture
def customer_headers(client):
    return login(client, "customer", "CustomerPass123!")
