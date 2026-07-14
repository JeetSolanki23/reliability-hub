import uuid
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, TypeDecorator
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
import sqlalchemy.types as types

class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """
    impl = types.CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(types.CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        else:
            return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(value)
            return value

class Service(Base):
    __tablename__ = "services"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True, nullable=False)
    owner = Column(String)
    endpoint_url = Column(String, nullable=False)
    environment = Column(String, default="prod") # dev, staging, prod
    check_interval_seconds = Column(Integer, default=60)

    health_checks = relationship("HealthCheck", back_populates="service", cascade="all, delete-orphan")
    incidents = relationship("Incident", back_populates="service", cascade="all, delete-orphan")
    slos = relationship("SLO", back_populates="service", cascade="all, delete-orphan")

class HealthCheck(Base):
    __tablename__ = "health_checks"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    service_id = Column(GUID(), ForeignKey("services.id"))
    checked_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String) # up, down, degraded
    latency_ms = Column(Integer)
    response_code = Column(Integer, nullable=True)

    service = relationship("Service", back_populates="health_checks")

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    service_id = Column(GUID(), ForeignKey("services.id"))
    title = Column(String, nullable=False)
    severity = Column(String) # sev1, sev2, sev3, sev4
    status = Column(String) # open, investigating, mitigated, resolved
    started_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    service = relationship("Service", back_populates="incidents")

class SLO(Base):
    __tablename__ = "slos"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    service_id = Column(GUID(), ForeignKey("services.id"))
    name = Column(String, nullable=False)
    target_availability = Column(Float, default=0.99)
    window_days = Column(Integer, default=30)

    service = relationship("Service", back_populates="slos")
