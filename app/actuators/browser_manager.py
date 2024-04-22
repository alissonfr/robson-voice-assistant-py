import webbrowser
from os import environ as env
from .base_actuator import BaseActuator

GOOGLE_URL = "www.google.com.br"
BING_URL = "www.bing.com"

class BrowserManager(BaseActuator):
    def __init__(self):
        return None

    def start(self, action, main_param, _):

        if action == "abrir" and main_param == "calendário":
            self.__open_browser_tab(env.get("CALENDAR_SERVICE_URL"))
        elif action == "abrir" and main_param == "e-mail":
            self.__open_browser_tab(env.get("EMAIL_SERVICE_URL"))
        elif action == "pesquisar" and main_param == "google":
            self.__open_browser_tab(GOOGLE_URL)
        elif action == "pesquisar" and main_param == "bing":
            self.__open_browser_tab(BING_URL)

    def __open_browser_tab(url):
        webbrowser.open(url)

