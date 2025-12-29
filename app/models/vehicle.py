import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Enum, DateTime, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.base import Base

class ComponentType(str, enum.Enum):
    SENSOR = "SENSOR"
    ACTUATOR = "ACTUATOR"
    MCU = "MCU"

class ComponentStatus(str, enum.Enum):
    OK = "OK"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vin: Mapped[str] = mapped_column(String, unique=True, index=True)
    model: Mapped[str] = mapped_column(String)
    firmware_version: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    components: Mapped[List["Component"]] = relationship(back_populates="vehicle", cascade="all, delete-orphan")
    telemetry_logs: Mapped[List["TelemetryLog"]] = relationship(back_populates="vehicle")
    faults: Mapped[List["Fault"]] = relationship(back_populates="vehicle")

class Component(Base):
    __tablename__ = "components"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("vehicles.id"))
    name: Mapped[str] = mapped_column(String)
    type: Mapped[ComponentType] = mapped_column(Enum(ComponentType))
    status: Mapped[ComponentStatus] = mapped_column(Enum(ComponentStatus), default=ComponentStatus.OK)

    vehicle: Mapped["Vehicle"] = relationship(back_populates="components")
