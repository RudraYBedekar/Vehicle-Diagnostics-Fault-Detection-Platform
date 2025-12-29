import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, Enum, DateTime, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.base import Base

if TYPE_CHECKING:
    from .vehicle import Vehicle

class FaultSeverity(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class Fault(Base):
    __tablename__ = "faults"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("vehicles.id"))
    component_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), ForeignKey("components.id"), nullable=True)
    code: Mapped[str] = mapped_column(String, index=True)
    severity: Mapped[FaultSeverity] = mapped_column(Enum(FaultSeverity))
    description: Mapped[str] = mapped_column(String)
    detected_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    vehicle: Mapped["Vehicle"] = relationship(back_populates="faults")
    recommendations: Mapped[List["Recommendation"]] = relationship(back_populates="fault", cascade="all, delete-orphan")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fault_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("faults.id"))
    action: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    fault: Mapped["Fault"] = relationship(back_populates="recommendations")
