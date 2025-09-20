from typing import Optional
from datetime import datetime
from http.client import responses

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

from core import Core
from logger import Logger
from report import Report
from reportSaver import ReportSaver

class Server:
    OptionalFloat = Optional[str]

    def parseOptionalFloat(optionalFloat: OptionalFloat):
        return None if (optionalFloat == "" or optionalFloat == None) else float(optionalFloat)

    def __init__(self):
        Logger.logInfo("Server starting...")
        self.app = FastAPI()

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins = [
                "http://127.0.0.1:8080",
            ],
            allow_credentials = True,
            allow_methods = ["*"],
            allow_headers = ["*"],
        )

        self.reportSaver = ReportSaver(Core.getPath("out"))

        # "GET /weatherstation/updateweatherstation.php?ID=10&PASSWORD=10&intemp=24.0&outtemp=15.0&dewpoint=11.4&windchill=15.0&inhumi=48&outhumi=79&windspeed=0.3&windgust=0.3&winddir=225&absbaro=996.0&relbaro=1018.5&rainrate=&dailyrain=6.0&weeklyrain=12.0&monthlyrain=12.0&yearlyrain=12.0&dateutc=2025-9-18%2020:53:41&softwaretype=EasyWeather%20V9.3.0&action=updateraw&realtime=1&rtfreq=5 HTTP/1.0"
        @self.app.get("/weatherstation/updateweatherstation.php")
        async def download(username: str = Query(alias = "ID"),
                           password: str = Query(alias = "PASSWORD"),
                           indoorTemperature: float = Query(alias = "intemp"),
                           outdoorTemperature: float = Query(alias = "outtemp"),
                           dewPoint: float = Query(alias = "dewpoint"),
                           windChill: float = Query(alias = "windchill"),
                           indoorHumidity: float = Query(alias = "inhumi"),
                           outdoorHumidity: float = Query(alias = "outhumi"),
                           windSpeed: float = Query(alias = "windspeed"),
                           gustSpeed: float = Query(alias = "windgust"),
                           windDirection: int = Query(alias = "winddir"),
                           absoluteAirPressure: float = Query(alias = "absbaro"),
                           relativeAirPressure: float = Query(alias = "relbaro"),
                           rainRate: Server.OptionalFloat = Query(alias = "rainrate", default = None),
                           dailyRain: Server.OptionalFloat = Query(alias = "dailyrain", default = None),
                           weeklyRain: Server.OptionalFloat = Query(alias = "weeklyrain", default = None),
                           monthlyRain: Server.OptionalFloat = Query(alias = "monthlyrain", default = None),
                           yearlyRain: Server.OptionalFloat = Query(alias = "yearlyrain", default = None),
                           date: str = Query(alias = "dateutc")):
            rainRate = Server.parseOptionalFloat(rainRate)
            dailyRain = Server.parseOptionalFloat(dailyRain)
            weeklyRain = Server.parseOptionalFloat(weeklyRain)
            monthlyRain = Server.parseOptionalFloat(monthlyRain)
            yearlyRain = Server.parseOptionalFloat(yearlyRain)
            yearMonthDay, hourMinuteSecond = date.split(' ')
            date = datetime(*map(int, yearMonthDay.split('-')), *map(int, hourMinuteSecond.split(':')))

            report = Report(
                date,
                indoorTemperature,
                indoorHumidity,
                outdoorTemperature,
                outdoorHumidity,
                windSpeed,
                gustSpeed,
                windDirection,
                dewPoint,
                windChill,
                relativeAirPressure,
                absoluteAirPressure,
                rainRate,
                dailyRain,
                weeklyRain,
                monthlyRain,
                yearlyRain
            )
            self.reportSaver.save(report)

            # GET https://idokep.hu/sendws.php?user=10&pass=10&ev=2025&ho=9&nap=16&ora=18&perc=9&mp=32&hom=21&rh=50&p=101.03&szelirany=30&szelero=4.78&csap=8.3
            response = requests.get(
                "https://idokep.hu/sendws.php",
                params = {
                    "user": username,
                    "pass": password,
                    "ev": report.date.year,
                    "ho": report.date.month,
                    "nap": report.date.day,
                    "ora": report.date.hour,
                    "perc": report.date.minute,
                    "mp": report.date.second,
                    "hom": report.outdoorTemperature,
                    "rh": report.outdoorHumidity,
                    "p": report.relativeAirPressure,
                    "szelirany": report.windDirection,
                    "szelero": report.windSpeed,
                    "csap": report.rainRate
                }
            )

            if response.status_code != requests.status_codes.codes.OK:
                Logger.logError(f"Couldn't send report. Reason: \"{response.reason}\"  {response.status_code} {responses[response.status_code].upper()}")

            Logger.logInfo(f"username: {username}\n"
                           f"password: {password}\n"
                           f"indoor temperature: {indoorTemperature}\n"
                           f"dew point: {dewPoint}\n"
                           f"outdoor temperature: {outdoorTemperature}\n"
                           f"windChill: {windChill}\n"
                           f"indoor humidity: {indoorHumidity}\n"
                           f"outdoor humidity: {outdoorHumidity}\n"
                           f"wind speed: {windSpeed}\n"
                           f"gust speed: {gustSpeed}\n"
                           f"wind direction: {windDirection}\n"
                           f"absolute air pressure: {absoluteAirPressure}\n"
                           f"relative air pressure: {relativeAirPressure}\n"
                           f"rain rate: {rainRate}\n"
                           f"daily rain: {dailyRain}\n"
                           f"weekly rain: {weeklyRain}\n"
                           f"monthly rain: {monthlyRain}\n"
                           f"yearly rain: {yearlyRain}\n"
                           f"date: {date}")

            return {"status": "ok"}