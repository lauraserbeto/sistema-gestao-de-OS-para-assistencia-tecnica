from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.ordem_servico import OSPriority, OSStatus


class _ClientSummary(BaseModel):
    id: int
    name: str
    cpf: str
    phone: str

    model_config = ConfigDict(from_attributes=True)


class _UserSummary(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class OSCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=1)
    priority: OSPriority = OSPriority.media
    client_id: int
    technician_id: Optional[int] = None


class OSUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=200)
    description: Optional[str] = Field(default=None, min_length=1)
    priority: Optional[OSPriority] = None
    client_id: Optional[int] = None


class OSAssign(BaseModel):
    technician_id: int


class OSCancel(BaseModel):
    cancellation_reason: str = Field(min_length=5, max_length=500)


class OSResponse(BaseModel):
    id: int
    numero: str
    title: str
    description: str
    status: OSStatus
    priority: OSPriority
    client: _ClientSummary
    technician: Optional[_UserSummary]
    opened_by: _UserSummary
    cancellation_reason: Optional[str]
    assigned_at: Optional[datetime]
    closed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
