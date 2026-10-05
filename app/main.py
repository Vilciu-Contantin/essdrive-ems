from fastapi import FastAPI
from app.core.config import settings
from app.energy.pv_simulator import PVSimulator
from app.energy.load_simulator import LoadSimulator


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