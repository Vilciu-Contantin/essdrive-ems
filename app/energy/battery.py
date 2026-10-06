from app.energy.models import BatteryData


class Battery:
    """
    Model simplificat pentru baterie.

    V1:
    - capacitate în kWh
    - SOC (%)
    - SOC minim / maxim
    - putere maximă de încărcare
    - putere maximă de descărcare
    - eficiență încărcare / descărcare
    - interval de 15 minute
    """

    def __init__(
        self,
        capacity_kwh: float = 257.0,
        soc_percent: float = 50.0,
        min_soc_percent: float = 10.0,
        max_soc_percent: float = 100.0,
        max_charge_power_kw: float = 60.0,
        max_discharge_power_kw: float = 60.0,
        charge_efficiency: float = 0.95,
        discharge_efficiency: float = 0.95,
    ):
        if capacity_kwh <= 0:
            raise ValueError(
                "Battery capacity must be greater than 0"
            )

        if not 0 <= soc_percent <= 100:
            raise ValueError(
                "SOC must be between 0 and 100"
            )

        if not 0 <= min_soc_percent <= 100:
            raise ValueError(
                "Minimum SOC must be between 0 and 100"
            )

        if not 0 <= max_soc_percent <= 100:
            raise ValueError(
                "Maximum SOC must be between 0 and 100"
            )

        if min_soc_percent > max_soc_percent:
            raise ValueError(
                "Minimum SOC cannot be greater than maximum SOC"
            )

        if not 0 < charge_efficiency <= 1:
            raise ValueError(
                "Charge efficiency must be between 0 and 1"
            )

        if not 0 < discharge_efficiency <= 1:
            raise ValueError(
                "Discharge efficiency must be between 0 and 1"
            )

        self.capacity_kwh = capacity_kwh
        self.soc_percent = soc_percent
        self.min_soc_percent = min_soc_percent
        self.max_soc_percent = max_soc_percent

        self.max_charge_power_kw = max_charge_power_kw
        self.max_discharge_power_kw = max_discharge_power_kw

        self.charge_efficiency = charge_efficiency
        self.discharge_efficiency = discharge_efficiency

    @property
    def energy_kwh(self) -> float:
        """
        Energia disponibilă în baterie.
        """
        return (
            self.capacity_kwh
            * self.soc_percent
            / 100
        )

    @property
    def min_energy_kwh(self) -> float:
        """
        Energia corespunzătoare SOC-ului minim.
        """
        return (
            self.capacity_kwh
            * self.min_soc_percent
            / 100
        )

    @property
    def max_energy_kwh(self) -> float:
        """
        Energia corespunzătoare SOC-ului maxim.
        """
        return (
            self.capacity_kwh
            * self.max_soc_percent
            / 100
        )

    def charge(
        self,
        power_kw: float,
        duration_hours: float = 0.25,
    ) -> float:
        """
        Încarcă bateria.

        duration_hours = 0.25 pentru interval de 15 minute.

        Returnează energia efectiv acceptată de baterie în kWh.
        """

        if power_kw < 0:
            raise ValueError(
                "Charge power cannot be negative"
            )

        if duration_hours <= 0:
            raise ValueError(
                "Duration must be greater than 0"
            )

        power_kw = min(
            power_kw,
            self.max_charge_power_kw,
        )

        requested_energy_kwh = (
            power_kw * duration_hours
        )

        available_capacity_kwh = (
            self.max_energy_kwh
            - self.energy_kwh
        )

        if available_capacity_kwh <= 0:
            return 0.0

        # Energia care poate intra în baterie
        max_input_energy_kwh = (
            available_capacity_kwh
            / self.charge_efficiency
        )

        input_energy_kwh = min(
            requested_energy_kwh,
            max_input_energy_kwh,
        )

        stored_energy_kwh = (
            input_energy_kwh
            * self.charge_efficiency
        )

        new_energy_kwh = (
            self.energy_kwh
            + stored_energy_kwh
        )

        self.soc_percent = (
            new_energy_kwh
            / self.capacity_kwh
            * 100
        )

        self.soc_percent = min(
            self.soc_percent,
            self.max_soc_percent,
        )

        return round(
            input_energy_kwh,
            3,
        )

    def discharge(
        self,
        power_kw: float,
        duration_hours: float = 0.25,
    ) -> float:
        """
        Descarcă bateria.

        duration_hours = 0.25 pentru interval de 15 minute.

        Returnează energia livrată către sarcină/rețea în kWh.
        """

        if power_kw < 0:
            raise ValueError(
                "Discharge power cannot be negative"
            )

        if duration_hours <= 0:
            raise ValueError(
                "Duration must be greater than 0"
            )

        power_kw = min(
            power_kw,
            self.max_discharge_power_kw,
        )

        requested_output_kwh = (
            power_kw * duration_hours
        )

        available_energy_kwh = (
            self.energy_kwh
            - self.min_energy_kwh
        )

        if available_energy_kwh <= 0:
            return 0.0

        # Pentru a livra requested_output,
        # bateria trebuie să consume mai mult
        # din energia internă din cauza eficienței.
        max_output_energy_kwh = (
            available_energy_kwh
            * self.discharge_efficiency
        )

        output_energy_kwh = min(
            requested_output_kwh,
            max_output_energy_kwh,
        )

        battery_energy_used_kwh = (
            output_energy_kwh
            / self.discharge_efficiency
        )

        new_energy_kwh = (
            self.energy_kwh
            - battery_energy_used_kwh
        )

        self.soc_percent = (
            new_energy_kwh
            / self.capacity_kwh
            * 100
        )

        self.soc_percent = max(
            self.soc_percent,
            self.min_soc_percent,
        )

        return round(
            output_energy_kwh,
            3,
        )

    def get_data(self) -> BatteryData:
        """
        Transformă starea internă a bateriei
        în modelul BatteryData.
        """

        return BatteryData(
            timestamp=None,
            power_kw=0.0,
            energy_kwh=round(
                self.energy_kwh,
                3,
            ),
            capacity_kwh=self.capacity_kwh,
            soc_percent=round(
                self.soc_percent,
                3,
            ),
            charge_power_kw=self.max_charge_power_kw,
            discharge_power_kw=self.max_discharge_power_kw,
            min_soc_percent=self.min_soc_percent,
            max_soc_percent=self.max_soc_percent,
        )