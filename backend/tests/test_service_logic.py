from app.models import ServiceStatus
from app.schemas import ServiceCreate, ServiceUpdate


def test_service_layer_summary_reflects_state_changes(service_layer, app_session):
    created = service_layer.create_service(
        app_session,
        ServiceCreate(
            name="Alerts Worker",
            environment="Staging",
            owner="SRE",
            status=ServiceStatus.HEALTHY,
            endpoint="https://alerts.internal",
            notes="Processes operational alerts",
        ),
    )

    summary = service_layer.summary(app_session)
    assert summary.total == 1
    assert summary.healthy == 1

    updated = service_layer.update_service(
        app_session,
        created.id,
        ServiceUpdate(status=ServiceStatus.CRITICAL, notes="Queue is blocked"),
    )
    assert updated.status == ServiceStatus.CRITICAL

    summary_after_update = service_layer.summary(app_session)
    assert summary_after_update.total == 1
    assert summary_after_update.critical == 1

    service_layer.delete_service(app_session, created.id)
    empty_summary = service_layer.summary(app_session)
    assert empty_summary.total == 0

