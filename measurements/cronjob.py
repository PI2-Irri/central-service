import os
import requests
from .models import Controller
from django_cron import CronJobBase, Schedule
from zones.models import Zone
from measurements.models import ZoneMeasurement
from django.utils.timezone import datetime

class WeatherMeasurementCronjob(CronJobBase):
    RUN_EVERY_MINS = 0
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'measurements.cronjob.WeatherMeasurementCronJob'

    def do(self):

        zones = Zone.objects.filter(is_active=True)

        for zone in zones:
            latitude = zone.latitude
            longitude = zone.longitude
            location = zone.location
            response_air = None
            response_forecast = None

            air_temperature = None
            precipitation = None

            if latitude == 0 and longitude == 0:
                response_air = requests.get(os.getenv('WEATHER_URL') + '/minutely_measurement/',
                            data={'location_name':  zone.location}).json()
                response_forecast = requests.get(os.getenv('WEATHER_URL') + '/forecast_measurement/',
                            data={'location_name':  zone.location}).json()
            else:
                response_air = requests.get(os.getenv('WEATHER_URL') + '/minutely_measurement/',
                            data={'latitude':  zone.latitude, 'longitude': zone.longitude}).json()
                response_forecast = requests.get(os.getenv('WEATHER_URL') + '/forecast_measurement/',
                            data={'latitude':  zone.latitude, 'longitude': zone.longitude}).json()

            if response_air != []:
                air_temperature = response_air[0]['temperature']
            else:
                print('Error in /minutely_measurement/ collection at {}'.format(datetime.now()))
                return

            if response_forecast != []:
                precipitation = response_forecast[0]['rain_precipitation'] if response_forecast[0]['rain_precipitation'] else 0
            else:
                print('Error in /forecast_measurement/ collection at {}'.format(datetime.now()))
                return

            measurement = ZoneMeasurement.objects.create(
                air_temperature=air_temperature,
                precipitation=precipitation,
                zone=zone
            )

            print('Measurement collection: {}'.format(measurement))
