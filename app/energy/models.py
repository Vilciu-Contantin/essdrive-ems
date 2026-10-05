from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class DeviceType(str, Enum):
    PV = "pv"
    BATTERY = "battery"
    LOAD = "load"
    GRID = "grid"
    METER = "meter"
    INVERTER = "inverter"


class EnergyData(BaseModel):
    timestamp: datetime
    power_kw: float = 0.0
    energy_kwh: float = 0.0
    voltage_v: float | None = None
    current_a: float | None = None
    reactive_power_kvar: float | None = None
    reactive_energy_kvarh: float | None = None


class PVData(EnergyData):
    device_type: DeviceType = DeviceType.PV


class LoadData(EnergyData):
    device_type: DeviceType = DeviceType.LOAD


class GridData(EnergyData):
    device_type: DeviceType = DeviceType.GRID


class BatteryData(EnergyData):
    device_type: DeviceType = DeviceType.BATTERY

    capacity_kwh: float
    soc_percent: float = Field(ge=0, le=100)

    charge_power_kw: float = 0.0
    discharge_power_kw: float = 0.0

    min_soc_percent: float = 10.0
    max_soc_percent: float = 100.0


class EnergySnapshot(BaseModel):
    timestamp: datetime

    pv: PVData
    load: LoadData
    battery: BatteryData
    grid: GridData