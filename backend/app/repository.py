from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.models import ServiceStatus, TrackedService, User, UserRole
from app.schemas import ServiceCreate, ServiceUpdate, SummaryRead


class ServiceRepository:
    def list_services(self, session: Session) -> list[TrackedService]:
        query = select(TrackedService).order_by(TrackedService.created_at.desc())
        return list(session.scalars(query))

    def get_service(self, session: Session, service_id: int) -> TrackedService | None:
        return session.get(TrackedService, service_id)

    def create_service(self, session: Session, payload: ServiceCreate) -> TrackedService:
        service = TrackedService(**payload.model_dump())
        session.add(service)
        session.commit()
        session.refresh(service)
        return service

    def update_service(
        self,
        session: Session,
        service: TrackedService,
        payload: ServiceUpdate,
    ) -> TrackedService:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(service, field, value)
        session.add(service)
        session.commit()
        session.refresh(service)
        return service

    def delete_service(self, session: Session, service: TrackedService) -> None:
        session.delete(service)
        session.commit()

    def summary(self, session: Session) -> SummaryRead:
        count_query = select(
            func.count(TrackedService.id),
            func.sum(case((TrackedService.status == ServiceStatus.HEALTHY, 1), else_=0)),
            func.sum(case((TrackedService.status == ServiceStatus.WARNING, 1), else_=0)),
            func.sum(case((TrackedService.status == ServiceStatus.CRITICAL, 1), else_=0)),
        )
        total, healthy, warning, critical = session.execute(count_query).one()
        return SummaryRead(
            total=total or 0,
            healthy=healthy or 0,
            warning=warning or 0,
            critical=critical or 0,
        )


class UserRepository:
    def get_by_username(self, session: Session, username: str) -> User | None:
        query = select(User).where(User.username == username)
        return session.scalar(query)

    def create_user(
        self,
        session: Session,
        username: str,
        full_name: str,
        role: UserRole,
        password_hash: str,
    ) -> User:
        user = User(
            username=username,
            full_name=full_name,
            role=role,
            password_hash=password_hash,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
