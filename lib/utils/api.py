import requests
from colorama import Fore, Style
from datetime import datetime


def get_date():
    now = datetime.now().strftime("%H:%M:%S")
    return now


class Api:
    def __init__(self, debug: bool = True) -> None:
        self.api = "https://desdobra-v2.herokuapp.com/api/v2/"
        self.debug = debug

    def _debug(self, url: str = None, status: int = None, methodRequest=str):
        """`Template das mensagens de debug. Desative o debug com`:
        >>> from lib.client import Client
        >>> client = Client()
        >>> client.debug = False
        """
        if status == 200:
            print(
                f"({get_date()}) "
                + Style.BRIGHT
                + Fore.LIGHTGREEN_EX
                + f"{methodRequest}: "
                + Fore.GREEN
                + url
                + Style.RESET_ALL
            )
        else:
            print(
                f"({get_date()}) "
                + Style.BRIGHT
                + Fore.LIGHTRED_EX
                + f"{methodRequest}: "
                + Fore.RED
                + url
                + Style.RESET_ALL
            )

    def sendGet(self, endpoint, params=None, headers=None):
        response = requests.get(self.api + endpoint, params=params, headers=headers)
        if self.debug:
            self._debug(
                url=self.api + endpoint,
                status=response.status_code,
                methodRequest="GET",
            )
        return response

    def sendPost(self, endpoint, data=None, json=None, headers: str = None):
        response = requests.post(
            self.api + endpoint, data=data, json=json, headers=headers
        )
        if self.debug:
            self._debug(
                url=self.api + endpoint,
                status=response.status_code,
                methodRequest="POST",
            )
        return response

    def sendDelete(self, endpoint, params=None, headers=None):
        response = requests.delete(self.api + endpoint, params=params, headers=headers)
        if self.debug:
            self._debug(
                url=self.api + endpoint,
                status=response.status_code,
                methodRequest="DELETE",
            )
        return response
