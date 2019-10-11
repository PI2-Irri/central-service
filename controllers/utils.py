import requests
from .exceptions import ControllerTokenException

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