import os
import requests
from .exceptions import ControllerTokenException
from controllers.models import Controller

class ControllerCommunication():

    @staticmethod
    def check_token(token, ip_address):
        response = requests.get(ip_address, params={"token": token})

        if response.status_code != 200:
            raise ControllerTokenException

    @staticmethod
    def get_controller_modules(token, ip_address):
        ip = ip_address + "modules/"

        response = requests.get(ip, params={"token": token})

        return response.json()

    @staticmethod
    def collect_all_measurements():
        controllers = Controller.objects.all()

        #TODO - put try except
        for controller in controllers:
            response = requests.get(
                os.getenv(
                    "MODULE_URL",
                    "http://localhost:3000/module_measurements"
                ),
                params={"token": controller.token}
            ).json()
