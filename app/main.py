

from threading import Thread

from config.env import *
from os import environ
import logging

from actuators.tocador import iniciar_tocador, atuar_sobre_tocador
from adapters.natural_language_adapter import NaturalLanguageAdapter
from adapters.speech_recognition_adapter import SpeechRecognitionAdapter
from helpers.json_helper import get_config_file
from helpers.token_helper import validate_token

ACTUATORS = [
    {
        "name": "tocador",
        "initActuator": iniciar_tocador,
        "actuatorParameter": None,
        "execute": atuar_sobre_tocador,
    },
]

class Main:
    def __init__(self):
        self.isRunning = False
        self.actuators = ACTUATORS

    def init(self):
        try:
            for atuador in self.actuators:
                atuador["actuatorParameter"] = atuador["initActuator"]()

            self.isRunning = True
        except Exception as e:
            logging.exception("Erro ao iniciar o assistente!")

    def execute(self):
        if not self.isRunning:
            print("O assistente não foi iniciado corretamente.")
            return

        while True:
            try:
                natural_language_client = NaturalLanguageAdapter()
                speech_recognition_client = SpeechRecognitionAdapter()

                speech = speech_recognition_client.listen()
                transcription = speech_recognition_client.transcribe(speech)
                tokens = natural_language_client.obter_tokens(transcription)
                filtered_tokens = natural_language_client.eliminar_palavras_de_parada(tokens)

                isTokenValid, action, actionObject = validate_token(
                    filtered_tokens, 
                    environ.get("ASSISTANT_NAME"), 
                    get_config_file(environ.get("CONFIG_FILE_PATH"))["actions"]
                )
                
                if isTokenValid is False:
                    return print("Comando inválido. Por favor tente novamente.")

                self._execute_action(self.actuators, action, actionObject)
            except Exception as e:
                logging.exception("Erro durante execução!")

    def _execute_action(actuators, action, actionObject):
        for actuator in actuators:
            actuatorParameter = actuator["actuatorParameter"]
            execute = actuator["execute"]
            process = Thread(target=execute, args=(action, actionObject, actuatorParameter))
            process.start()

if __name__ == "__main__":
    app = Main()
    app.init()
    app.execute()
