from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from math import floor

@dataclass
class Report:
    id: int = field(init = False)
    date: datetime
    indoorTemperature: float
    indoorHumidity: float
    outdoorTemperature: float
    outdoorHumidity: float
    windSpeed: float
    gustSpeed: float
    windDirection: float
    dewPoint: float
    windChill: float
    relativeAirPressure: float
    absoluteAirPressure: float
    rainRate: Optional[float]
    dailyRain: Optional[float]
    weeklyRain: Optional[float]
    monthlyRain: Optional[float]
    yearlyRain: Optional[float]

    def __post_init__(self):
        self.id = floor(self.date.timestamp())