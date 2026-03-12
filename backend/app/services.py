from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repository import ServiceRepository
from app.schemas import ServiceCreate, ServiceUpdate, SummaryRead


class CloudOpsService:
    def __init__(self, repository: ServiceRepository):
        self.repository = repository

    def list_services(self, session: Session):
        return self.repository.list_services(session)

    def create_service(self, session: Session, payload: ServiceCreate):
        return self.repository.create_service(session, payload)

    def update_service(self, session: Session, service_id: int, payload: ServiceUpdate):
        service = self.repository.get_service(session, service_id)
        if service is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found",
            )
        return self.repository.update_service(session, service, payload)

    def delete_service(self, session: Session, service_id: int) -> None:
        service = self.repository.get_service(session, service_id)
        if service is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found",
            )
        self.repository.delete_service(session, service)

    def summary(self, session: Session) -> SummaryRead:
        return self.repository.summary(session)

