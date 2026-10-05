from datetime import datetime, timedelta, timezone

from app.energy.models import PVData


class PVSimulator:
    """
    Simulează producția unei instalații fotovoltaice.

    V1:
    - producție pe 24h
    - interval de 15 minute
    - 96 intervale/zi
    """

    def __init__(
        self,
        capacity_kw: float,
        peak_factor: float = 1.0,
    ):
        if capacity_kw <= 0:
            raise ValueError(
                "PV capacity must be greater than 0"
            )

        if not 0 < peak_factor <= 1:
            raise ValueError(
                "Peak factor must be between 0 and 1"
            )

        self.capacity_kw = capacity_kw
        self.peak_factor = peak_factor

    def calculate_power(self, hour: float) -> float:

        if hour < 6 or hour >= 18:
            return 0.0

        if hour < 12:
            factor = (hour - 6) / 6
        else:
            factor = (18 - hour) / 6

        power_kw = (
            self.capacity_kw
            * factor
            * self.peak_factor
        )

        return round(power_kw, 3)

    def generate_day(
        self,
        date: datetime | None = None,
    ) -> list[PVData]:

        if date is None:
            date = datetime.now(timezone.utc)

        start = date.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        data = []

        for interval in range(96):

            timestamp = start + timedelta(
                minutes=interval * 15
            )

            hour = (
                timestamp.hour
                + timestamp.minute / 60
            )

            power_kw = self.calculate_power(hour)

            energy_kwh = power_kw * 0.25

            data.append(
                PVData(
                    timestamp=timestamp,
                    power_kw=power_kw,
                    energy_kwh=round(
                        energy_kwh,
                        3,
                    ),
                )
            )

        return data