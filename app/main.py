import logging
from threading import Thread
from config.env import *
from speech_recognition.exceptions import UnknownValueError

from actuators.activities import Activities
from actuators.browser_manager import BrowserManager

from facades.nltk_facade import NltkFacade
from facades.speech_recognition_facade import SpeechRecognitionFacade



ACTUATORS = [
    {
        "name": "activities",
        "class": Activities,
        "parameter": None,
    },
    {
        "name": "browser_manager",
        "class": BrowserManager,
        "parameter": None,
    }
]

class Main:
    def __init__(self):
        self.isRunning = False
        self.actuators = ACTUATORS

    def initialize(self):
        try:
            for actuator in self.actuators:
                actuator_instance = actuator["class"]
                actuator["parameter"] = actuator_instance()

            self.isRunning = True
        except Exception as e:
            print(f"Erro ao iniciar o assistente: {str(e)}")
            logging.exception(str(e))

    def execute(self):
        if not self.isRunning:
            print("O assistente não foi iniciado corretamente.")
            return

        while True:
            try:
                nltk = NltkFacade()
                speech_recognition = SpeechRecognitionFacade()

                speech = speech_recognition.listen()
                transcription = speech_recognition.transcribe(speech) # ta sem tratamento de erro qnd nao fala nada
                nltk.generate_tokens(transcription)

                if nltk.is_tokens_valid() is False:
                    print("Comando inválido. Por favor tente novamente.")
                    continue
                
                action, actuator_object = nltk.get_action_and_object()

                self.__execute_action(self.actuators, action, actuator_object)
            except UnknownValueError:
                print("Erro ao processar a fala.")
            except KeyboardInterrupt:
                print("Desligando assistente virtual.")
                break
            except OSError as e:
                print(f"Erro de sistema operacional: {str(e)}.")
                break
            except Exception as e:
                print(f"Erro ao processar comando: {str(e)}.")
                logging.exception(str(e))

    def __execute_action(self, actuators, action, actuator_object):
        for actuator in actuators:
            actuator_instance = actuator["class"]
            parameter = actuator["parameter"]
            process = Thread(target=actuator_instance.start, args=(actuator_instance, action, actuator_object, parameter))
            process.start()

if __name__ == "__main__":
    app = Main()
    app.initialize()
    app.execute()
