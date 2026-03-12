from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models import ServiceStatus, UserRole


class LoginRequest(BaseModel):
    username: str = Field(min_length=2, max_length=80)
    password: str = Field(min_length=8, max_length=128)


class UserRead(BaseModel):
    username: str
    full_name: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead


class ServiceBase(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    environment: str = Field(min_length=2, max_length=64)
    owner: str = Field(min_length=2, max_length=80)
    status: ServiceStatus
    endpoint: str | None = Field(default=None, max_length=255)
    notes: str | None = Field(default=None, max_length=1000)


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    environment: str | None = Field(default=None, min_length=2, max_length=64)
    owner: str | None = Field(default=None, min_length=2, max_length=80)
    status: ServiceStatus | None = None
    endpoint: str | None = Field(default=None, max_length=255)
    notes: str | None = Field(default=None, max_length=1000)


class ServiceRead(ServiceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SummaryRead(BaseModel):
    total: int
    healthy: int
    warning: int
    critical: int
