import webbrowser
from os import environ as env
from actuators.base_actuator import BaseActuator

GOOGLE_URL = "www.google.com.br"
BING_URL = "www.bing.com"

class BrowserManager(BaseActuator):
    def __init__(self):
        return None

    def start(self, action, actuator_object, _):
        if action == "abrir" and actuator_object == "calendário":
            self.__open_browser_tab(env.get("CALENDAR_SERVICE_URL"))
        elif action == "abrir" and actuator_object == "e-mail":
            self.__open_browser_tab(env.get("EMAIL_SERVICE_URL"))
        elif action == "pesquisar" and actuator_object == "google":
            self.__open_browser_tab(GOOGLE_URL)
        elif action == "pesquisar" and actuator_object == "bing":
            self.__open_browser_tab(BING_URL)

    def __open_browser_tab(url):
        webbrowser.open(url)

