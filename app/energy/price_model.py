
from datetime import datetime, timedelta, timezone

from pydantic import BaseModel, Field


class EnergyPrice(BaseModel):
    """Prețul energiei pentru un interval de timp."""

    timestamp: datetime
    price_ron_mwh: float
    interval_minutes: int = 15


class PriceSimulator:
    """
    Simulator de prețuri pentru 24 de ore.
    Generează 96 de intervale a câte 15 minute.
    """

    def __init__(self, base_price_ron_mwh: float = 500.0):
        if base_price_ron_mwh < 0:
            raise ValueError("Base price cannot be negative")

        self.base_price_ron_mwh = base_price_ron_mwh

    def calculate_price(self, hour: float) -> float:
        """Creează un profil simplificat al prețului."""

        if 0 <= hour < 6:
            factor = 0.70
        elif 6 <= hour < 10:
            factor = 1.00
        elif 10 <= hour < 16:
            factor = 0.85
        elif 16 <= hour < 21:
            factor = 1.50
        else:
            factor = 0.90

        return round(self.base_price_ron_mwh * factor, 2)

    def generate_day(
        self,
        date: datetime | None = None,
    ) -> list[EnergyPrice]:
        if date is None:
            date = datetime.now(timezone.utc)

        start = date.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        prices = []

        for interval in range(96):
            timestamp = start + timedelta(minutes=interval * 15)

            hour = timestamp.hour + timestamp.minute / 60

            prices.append(
                EnergyPrice(
                    timestamp=timestamp,
                    price_ron_mwh=self.calculate_price(hour),
                )
            )

        return prices
