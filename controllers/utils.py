import os
import requests
from .exceptions import ControllerTokenException
from controllers.models import Controller
from measurements.models import ActuatorsMeasurement
from measurements.models import ModulesMeasurement
from measurements.models import ZoneMeasurement


class ControllerCommunication():

    def make_decision(self):
        """
        Precisa de:
            - temperatura do ar (ZoneMeasurement)
            - precipitação (ZoneMeasurement)
            - temperatura do solo (ModulesMeasurement)
            - umidade do solo (ModulesMeasurement)
            - nível do reservatório (ActuatorsMeasurement)
        """

        controllers = Controller.objects.all()

        for controller in controllers:
            if controller.is_active:
                actuator_measurements = controller.actuatorsmeasurement_set.last()
                zone_measurements = controller.zonemeasurement_set.last()
                modules_measurements = controller.modulesmeasurement_set.objects.last()

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
                        controller.permit_irrigation = True
                    else:
                        if ground_humidity > 50:
                            if soil_temperature > 33.4 and air_temperature > 35:
                                if ground_humidity < 60:
                                    controller.permit_irrigation = True
                                else:
                                    pass
                            else:
                                pass
                        else:
                            controller.permit_irrigation = True
                else:
                    pass

    def allow_irrigation(self):
        pass
