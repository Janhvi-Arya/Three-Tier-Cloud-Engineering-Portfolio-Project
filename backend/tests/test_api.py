def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_login_returns_role_aware_user_profile(client):
    response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "AdminPass123!"},
    )

    assert response.status_code == 200
    assert response.json()["user"]["role"] == "admin"
    assert response.json()["token_type"] == "bearer"


def test_protected_endpoint_requires_authentication(client):
    response = client.get("/api/services")

    assert response.status_code == 401
    assert response.json() == {"detail": "Authentication required"}


def test_customer_is_forbidden_from_mutating_services(client, customer_headers):
    response = client.post(
        "/api/services",
        headers=customer_headers,
        json={
            "name": "Payments API",
            "environment": "Production",
            "owner": "Platform Team",
            "status": "Healthy",
            "endpoint": "https://payments.internal",
            "notes": "Serving checkout traffic",
        },
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin access required"}


def test_create_list_update_delete_service_flow(client, admin_headers):
    create_response = client.post(
        "/api/services",
        headers=admin_headers,
        json={
            "name": "Payments API",
            "environment": "Production",
            "owner": "Platform Team",
            "status": "Healthy",
            "endpoint": "https://payments.internal",
            "notes": "Serving checkout traffic",
        },
    )

    assert create_response.status_code == 201
    created_service = create_response.json()
    assert created_service["name"] == "Payments API"

    list_response = client.get("/api/services", headers=admin_headers)
    assert list_response.status_code == 200
    services = list_response.json()
    assert len(services) == 1

    summary_response = client.get("/api/summary", headers=admin_headers)
    assert summary_response.status_code == 200
    assert summary_response.json() == {
        "total": 1,
        "healthy": 1,
        "warning": 0,
        "critical": 0,
    }

    update_response = client.put(
        f"/api/services/{created_service['id']}",
        headers=admin_headers,
        json={"status": "Warning", "notes": "Latency is trending up"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "Warning"

    summary_after_update = client.get("/api/summary", headers=admin_headers)
    assert summary_after_update.json() == {
        "total": 1,
        "healthy": 0,
        "warning": 1,
        "critical": 0,
    }

    delete_response = client.delete(
        f"/api/services/{created_service['id']}",
        headers=admin_headers,
    )
    assert delete_response.status_code == 204

    final_summary = client.get("/api/summary", headers=admin_headers)
    assert final_summary.json() == {
        "total": 0,
        "healthy": 0,
        "warning": 0,
        "critical": 0,
    }


def test_update_missing_service_returns_404(client, admin_headers):
    response = client.put(
        "/api/services/999",
        headers=admin_headers,
        json={"status": "Critical"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Service not found"}
