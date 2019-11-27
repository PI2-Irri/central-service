import os
import requests
from controllers.models import Controller
from measurements.models import ActuatorsMeasurement
from measurements.models import ModulesMeasurement
from measurements.models import ZoneMeasurement
from django_cron import CronJobBase, Schedule
from zones.models import Zone
from schedules.models import Notification
from django.utils.timezone import datetime


class MinutelyVerificationCronJob(CronJobBase):
    RUN_EVERY_MINS = 0
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'schedules.cronjob.MinutelyVerificationCronJob'

    def do(self):

        time = datetime.now().strftime('%Y-%m-%d %H:%M')
    
        controllers = Controller.objects.all()
       
        for controller in controllers:

            zones = controller.zone_set.all()
            active_zone = None

            for zone in zones:
                schedule = zone.schedule_set.filter(schedule=datetime.strptime(time, '%Y-%m-%d %H:%M'))
                if schedule:
                    irrigate = self.make_decision(zone)
                    
                    if irrigate:
                        active_zone = zone
                    else:
                        users = controller.user_set.all()
                        for user in users:
                            Notification.objects.create(
                                time=datetime.strptime(time, '%Y-%m-%d %H:%M'),
                                message="Schedule {}: Zone {} in proper condition. No need to irrigate".format(time,zone.name),
                                user=user
                            )


            if active_zone:
                for zone in zones:
                    if zone.name == active_zone.name:
                        zone.is_active = True
                    else:
                        zone.is_active = False

    
    def make_decision(self, zone):
        """
        Precisa de:
            - temperatura do ar (ZoneMeasurement)
            - precipitação (ZoneMeasurement)
            - temperatura do solo (ModulesMeasurement)
            - umidade do solo (ModulesMeasurement)
            - nível do reservatório (ActuatorsMeasurement)
        """
            
        actuator_measurements = zone.actuatorsmeasurement_set.last()
        zone_measurements = zone.zonemeasurement_set.last()
        modules_measurements = zone.modulesmeasurement_set.objects.last()
        controller = zone.controller_set.get(controller=zone.controller)

        if actuator_measurements:
            reservoir_level = reservoir_level['precipitation']

        if zone_measurements:
            precipitation = zone_measurements['precipitation']
            air_temperature = zone_measurements['air_temperature']

        if modules_measurements:
            ground_humidity = modules_measurements['ground_humidity']
            soil_temperature = modules_measurements['temperature']

        if reservoir_level:
            if precipitation:
                controller.status = False
            else:
                if ground_humidity > 50:
                    if soil_temperature > 33.4 and air_temperature > 35:
                        if ground_humidity < 60:
                            controller.status = True
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    controller.status = True
                    return True
        else:
            return False