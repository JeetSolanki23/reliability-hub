from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

# Service Schemas
class ServiceBase(BaseModel):
    name: str
    owner: str
    endpoint_url: str
    environment: str = "prod"
    check_interval_seconds: int = 60

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    owner: Optional[str] = None
    endpoint_url: Optional[str] = None
    environment: Optional[str] = None
    check_interval_seconds: Optional[int] = None

class Service(ServiceBase):
    id: UUID
    class Config:
        from_attributes = True

# HealthCheck Schemas
class HealthCheckBase(BaseModel):
    status: str
    latency_ms: int
    response_code: Optional[int] = None

class HealthCheckCreate(HealthCheckBase):
    service_id: UUID

class HealthCheck(HealthCheckBase):
    id: UUID
    service_id: UUID
    checked_at: datetime
    class Config:
        from_attributes = True

# Incident Schemas
class IncidentBase(BaseModel):
    title: str
    severity: str
    status: str = "open"

class IncidentCreate(IncidentBase):
    service_id: UUID

class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    resolved_at: Optional[datetime] = None

class Incident(IncidentBase):
    id: UUID
    service_id: UUID
    started_at: datetime
    resolved_at: Optional[datetime] = None
    class Config:
        from_attributes = True

# SLO Schemas
class SLOBase(BaseModel):
    name: str
    target_availability: float = 0.99
    window_days: int = 30

class SLOCreate(SLOBase):
    service_id: UUID

class SLO(SLOBase):
    id: UUID
    service_id: UUID
    class Config:
        from_attributes = True

class SLOStatus(BaseModel):
    service_name: str
    target: float
    current_availability: float
    status: str # healthy, breaching
