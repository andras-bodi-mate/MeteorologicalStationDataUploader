from pathlib import Path
import csv

from report import Report

class ReportSaver:
    def __init__(self, directory: Path):
        self.directory = directory
        self.directory.mkdir(parents = True, exist_ok = True)

    def save(self, report: Report):
        path = (self.directory / report.date.date().isoformat()).with_suffix(".csv")
        if not path.exists():
            path.touch()
            with open(path, "w", encoding = "utf-8", newline = '') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "id",
                    "date",
                    "indoorTemperature",
                    "indoorHumidity",
                    "outdoorTemperature",
                    "outdoorHumidity",
                    "windSpeed",
                    "gustSpeed",
                    "windDirection",
                    "dewPoint",
                    "windChill",
                    "relativeAirPressure",
                    "absoluteAirPressure",
                    "rainRate",
                    "dailyRain",
                    "weeklyRain",
                    "monthlyRain",
                    "yearlyRain"
                ])

        with open(path, "a", encoding = "utf-8", newline = '') as file:
            writer = csv.writer(file)
            writer.writerow([
                report.id,
                report.date,
                report.indoorTemperature,
                report.indoorHumidity,
                report.outdoorTemperature,
                report.outdoorHumidity,
                report.windSpeed,
                report.gustSpeed,
                report.windDirection,
                report.dewPoint,
                report.windChill,
                report.relativeAirPressure,
                report.absoluteAirPressure,
                report.rainRate,
                report.dailyRain,
                report.weeklyRain,
                report.monthlyRain,
                report.yearlyRain
            ])
