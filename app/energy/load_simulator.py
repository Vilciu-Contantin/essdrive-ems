from datetime import datetime, timedelta, timezone

from app.energy.models import LoadData


class LoadSimulator:
    """
    Simulează consumul unei instalații.

    V1:
    - consum pe 24h
    - interval de 15 minute
    - 96 intervale/zi
    """

    def __init__(
        self,
        base_load_kw: float = 10.0,
        peak_load_kw: float = 30.0,
    ):
        if base_load_kw < 0:
            raise ValueError(
                "Base load must be greater than or equal to 0"
            )

        if peak_load_kw < base_load_kw:
            raise ValueError(
                "Peak load must be greater than or equal to base load"
            )

        self.base_load_kw = base_load_kw
        self.peak_load_kw = peak_load_kw

    def calculate_power(self, hour: float) -> float:
        """
        Curba simplificată de consum.

        00:00–06:00 -> consum redus
        06:00–09:00 -> creștere
        09:00–17:00 -> consum normal
        17:00–21:00 -> consum ridicat
        21:00–24:00 -> scădere
        """

        if 0 <= hour < 6:
            factor = 0.35

        elif 6 <= hour < 9:
            factor = 0.35 + (
                (hour - 6) / 3
            ) * 0.45

        elif 9 <= hour < 17:
            factor = 0.80

        elif 17 <= hour < 21:
            factor = 0.80 + (
                (hour - 17) / 4
            ) * 0.20

        else:
            factor = 0.50

        power_kw = (
            self.base_load_kw
            + (
                self.peak_load_kw
                - self.base_load_kw
            ) * factor
        )

        return round(power_kw, 3)

    def generate_day(
        self,
        date: datetime | None = None,
    ) -> list[LoadData]:

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
                LoadData(
                    timestamp=timestamp,
                    power_kw=power_kw,
                    energy_kwh=round(
                        energy_kwh,
                        3,
                    ),
                )
            )

        return data