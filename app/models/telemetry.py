from datetime import datetime
import uuid
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, BigInteger, JSON, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .vehicle import Vehicle

class TelemetryLog(Base):
    __tablename__ = "telemetry_logs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    vehicle_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("vehicles.id"))
    timestamp: Mapped[datetime] = mapped_column(DateTime, index=True)
    data: Mapped[dict] = mapped_column(JSON)

    vehicle: Mapped["Vehicle"] = relationship(back_populates="telemetry_logs")
