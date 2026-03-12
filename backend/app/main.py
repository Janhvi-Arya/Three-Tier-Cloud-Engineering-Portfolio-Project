from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import Base, build_session_factory, get_session_from_factory
from app.models import User, UserRole
from app.repository import ServiceRepository, UserRepository
from app.schemas import (
    LoginRequest,
    LoginResponse,
    ServiceCreate,
    ServiceRead,
    ServiceUpdate,
    SummaryRead,
    UserRead,
)
from app.security import create_access_token, decode_access_token, hash_password, verify_password
from app.services import CloudOpsService


bearer_scheme = HTTPBearer(auto_error=False)


def get_service_layer() -> CloudOpsService:
    return CloudOpsService(ServiceRepository())


def get_user_repository() -> UserRepository:
    return UserRepository()


def get_session(request: Request):
    yield from get_session_from_factory(request.app.state.session_factory)


def seed_default_users(app: FastAPI) -> None:
    settings = app.state.settings
    session = app.state.session_factory()
    user_repository = UserRepository()
    try:
        if user_repository.get_by_username(session, settings.admin_username) is None:
            user_repository.create_user(
                session=session,
                username=settings.admin_username,
                full_name="Operations Admin",
                role=UserRole.ADMIN,
                password_hash=hash_password(settings.admin_password),
            )
        if user_repository.get_by_username(session, settings.customer_username) is None:
            user_repository.create_user(
                session=session,
                username=settings.customer_username,
                full_name="CloudOps Customer",
                role=UserRole.CUSTOMER,
                password_hash=hash_password(settings.customer_password),
            )
    finally:
        session.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=app.state.engine)
    seed_default_users(app)
    yield
    app.state.engine.dispose()


def get_current_user(
    request: Request,
    session: Session = Depends(get_session),
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> User:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    payload = decode_access_token(credentials.credentials, request.app.state.settings.app_secret)
    user = UserRepository().get_by_username(session, payload["sub"])
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


def create_app(database_url: str | None = None) -> FastAPI:
    settings = get_settings(database_url)
    engine, session_factory = build_session_factory(settings.database_url)

    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    app.state.engine = engine
    app.state.session_factory = session_factory
    app.state.settings = settings

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health_check(session: Session = Depends(get_session)):
        session.execute(text("SELECT 1"))
        return {"status": "ok"}

    @app.post("/api/auth/login", response_model=LoginResponse)
    def login(
        payload: LoginRequest,
        session: Session = Depends(get_session),
        user_repository: UserRepository = Depends(get_user_repository),
    ):
        user = user_repository.get_by_username(session, payload.username)
        if user is None or not verify_password(payload.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        access_token = create_access_token(
            username=user.username,
            role=user.role.value,
            secret=settings.app_secret,
        )
        return LoginResponse(access_token=access_token, user=UserRead.model_validate(user))

    @app.get("/api/auth/me", response_model=UserRead)
    def read_current_user(current_user: User = Depends(get_current_user)):
        return current_user

    @app.get("/api/services", response_model=list[ServiceRead])
    def list_services(
        session: Session = Depends(get_session),
        service_layer: CloudOpsService = Depends(get_service_layer),
        current_user: User = Depends(get_current_user),
    ):
        return service_layer.list_services(session)

    @app.post("/api/services", response_model=ServiceRead, status_code=status.HTTP_201_CREATED)
    def create_service(
        payload: ServiceCreate,
        session: Session = Depends(get_session),
        service_layer: CloudOpsService = Depends(get_service_layer),
        current_user: User = Depends(require_admin),
    ):
        return service_layer.create_service(session, payload)

    @app.put("/api/services/{service_id}", response_model=ServiceRead)
    def update_service(
        service_id: int,
        payload: ServiceUpdate,
        session: Session = Depends(get_session),
        service_layer: CloudOpsService = Depends(get_service_layer),
        current_user: User = Depends(require_admin),
    ):
        return service_layer.update_service(session, service_id, payload)

    @app.delete("/api/services/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_service(
        service_id: int,
        session: Session = Depends(get_session),
        service_layer: CloudOpsService = Depends(get_service_layer),
        current_user: User = Depends(require_admin),
    ):
        service_layer.delete_service(session, service_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @app.get("/api/summary", response_model=SummaryRead)
    def get_summary(
        session: Session = Depends(get_session),
        service_layer: CloudOpsService = Depends(get_service_layer),
        current_user: User = Depends(get_current_user),
    ):
        return service_layer.summary(session)

    return app


app = create_app()
