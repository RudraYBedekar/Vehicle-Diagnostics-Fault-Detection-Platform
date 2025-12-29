import asyncio
import random
import uuid
import sys
import os
from datetime import datetime

# Add app to path
sys.path.append(os.getcwd())

from app.db.session import AsyncSessionLocal
from app.models import Vehicle, Component, TelemetryLog, Fault, ComponentType, ComponentStatus, FaultSeverity

async def create_demo_data(db):
    # 1. Create a Test Vehicle
    # Using ORM for safety
    from sqlalchemy import select
    res = await db.execute(select(Vehicle).where(Vehicle.vin == "TESLA_SIM_001"))
    vehicle = res.scalar_one_or_none()

    if not vehicle:
        print("Creating demo vehicle... TESLA_SIM_001")
        vehicle = Vehicle(
            vin="TESLA_SIM_001",
            model="Model S Plaid",
            firmware_version="2025.44.25"
        )
        db.add(vehicle)
        await db.commit()
        await db.refresh(vehicle)
        
        # Add a battery component
        comp = Component(
            vehicle_id=vehicle.id,
            name="HV_BATTERY",
            type=ComponentType.SENSOR,
            status=ComponentStatus.OK
        )
        db.add(comp)
        await db.commit()
    else:
        print("Using existing vehicle... TESLA_SIM_001")
    
    return vehicle

async def simulate_telemetry():
    async with AsyncSessionLocal() as db:
        try:
            vehicle = await create_demo_data(db)
            print(f"\n🚀 STARTING SIMULATION for Vehicle: {vehicle.vin}")
        except Exception as e:
            print(f"\n⚠️ Database Error (Running in Demo Mode without DB saving): {e}")
            # Mock vehicle object for display
            from collections import namedtuple
            VehicleMock = namedtuple('Vehicle', ['id', 'vin'])
            vehicle = VehicleMock(id=uuid.uuid4(), vin="DEMO_MODE_CAR")
            print(f"\n🚀 STARTING SIMULATION (NO DB) for Vehicle: {vehicle.vin}")

        print("-----------------------------------------------------")
        print("Sending telemetry packets (Press Ctrl+C to stop)...")

        try:
            while True:
                # Simulate Sensors
                speed = random.randint(55, 120)  # mph
                battery_temp = random.uniform(30.0, 50.0) # Celsius
                voltage = random.uniform(350, 400)
                
                # Logic: Check for faults (Simple Rule Engine)
                status = "OK"
                fault_msg = ""
                
                if battery_temp > 45.0:
                    status = "CRITICAL"
                    fault_msg = "overheating"
                    # Log fault to DB (Simplified logic)
                    try:
                        fault = Fault(
                            vehicle_id=vehicle.id,
                            code="BAT_TEMP_HIGH",
                            severity=FaultSeverity.CRITICAL,
                            description=f"Battery Temp {battery_temp:.1f}C exceeds limit 45C"
                        )
                        db.add(fault)
                    except:
                        pass # Ignore DB error in loop

                elif speed > 100:
                    status = "WARNING"
                    fault_msg = "high_speed"

                # Create Telemetry Record
                try:
                    log = TelemetryLog(
                        vehicle_id=vehicle.id,
                        timestamp=datetime.utcnow(),
                        data={
                            "speed_mph": speed,
                            "battery_temp_c": battery_temp,
                            "voltage_hv": voltage
                        }
                    )
                    db.add(log)
                    await db.commit()
                except Exception:
                    await db.rollback() # Rollback on error
                    # Continue loop

                # Print Status to Terminal
                color = "\033[92m" if status == "OK" else "\033[91m"
                reset = "\033[0m"
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {color}{status:8s}{reset} | Speed: {speed:3d} mph | Batt Temp: {battery_temp:4.1f}°C | {fault_msg}")

                await asyncio.sleep(1) # Send every 1 second

        except KeyboardInterrupt:
            print("\n🛑 Simulation stopped.")

if __name__ == "__main__":
    try:
        if sys.platform == 'win32':
           asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(simulate_telemetry())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")
