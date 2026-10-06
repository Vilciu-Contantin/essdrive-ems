from fastapi import FastAPI
from app.core.config import settings
from app.energy.pv_simulator import PVSimulator
from app.energy.load_simulator import LoadSimulator
from app.energy.battery import Battery


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="ESSDRIVE Energy Management System API",
)


@app.get("/")
def root():
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }

@app.get("/api/v1/energy/pv/simulate")
def simulate_pv(
    capacity_kw: float = 100,
):
    simulator = PVSimulator(
        capacity_kw=capacity_kw,
    )

    data = simulator.generate_day()

    return {
        "device": "PV_SIMULATOR",
        "capacity_kw": capacity_kw,
        "interval_minutes": 15,
        "intervals": len(data),
        "data": data,
    }

@app.get("/api/v1/energy/load/simulate")
def simulate_load(
    base_load_kw: float = 10.0,
    peak_load_kw: float = 30.0,
):
    simulator = LoadSimulator(
        base_load_kw=base_load_kw,
        peak_load_kw=peak_load_kw,
    )

    data = simulator.generate_day()

    return {
        "device": "LOAD_SIMULATOR",
        "base_load_kw": base_load_kw,
        "peak_load_kw": peak_load_kw,
        "interval_minutes": 15,
        "intervals": len(data),
        "data": data,
    }

@app.get("/api/v1/energy/battery/test")
def test_battery():
    battery = Battery(
        capacity_kwh=257.0,
        soc_percent=50.0,
        min_soc_percent=10.0,
        max_soc_percent=100.0,
        max_charge_power_kw=60.0,
        max_discharge_power_kw=60.0,
    )

    initial_energy = battery.energy_kwh

    charged_energy = battery.charge(
        power_kw=60.0,
        duration_hours=0.25,
    )

    soc_after_charge = battery.soc_percent

    discharged_energy = battery.discharge(
        power_kw=60.0,
        duration_hours=0.25,
    )

    soc_after_discharge = battery.soc_percent

    return {
        "battery": "BATTERY_SIMULATOR",
        "capacity_kwh": battery.capacity_kwh,
        "initial_soc_percent": 50.0,
        "initial_energy_kwh": round(initial_energy, 3),
        "charge_power_kw": 60.0,
        "charge_duration_minutes": 15,
        "charged_energy_kwh": charged_energy,
        "soc_after_charge_percent": round(
            soc_after_charge,
            3,
        ),
        "discharge_power_kw": 60.0,
        "discharge_duration_minutes": 15,
        "discharged_energy_kwh": discharged_energy,
        "soc_after_discharge_percent": round(
            soc_after_discharge,
            3,
        ),
        "final_energy_kwh": round(
            battery.energy_kwh,
            3,
        ),
    }