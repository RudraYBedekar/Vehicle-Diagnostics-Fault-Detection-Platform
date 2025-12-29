from app.db.base import Base
from .vehicle import Vehicle, Component, ComponentType, ComponentStatus
from .telemetry import TelemetryLog
from .fault import Fault, Recommendation, FaultSeverity
