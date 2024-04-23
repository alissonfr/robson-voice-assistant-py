import sys
import logging
from threading import Thread
from speech_recognition.exceptions import UnknownValueError
from os import path

ROOT_FOLDER = path.abspath(path.join(path.dirname(__file__), '..'))
sys.path.append(ROOT_FOLDER)

from app.config.env import *

from app.actuators.activities import Activities
from app.actuators.browser_manager import BrowserManager

from app.facades.nltk_facade import NltkFacade
from app.facades.speech_recognition_facade import SpeechRecognitionFacade

ACTUATORS = [
    {
        "name": "activities",
        "class": Activities,
    },
    {
        "name": "browser_manager",
        "class": BrowserManager,
    }
]

class Main:
    def __init__(self):
        self.isRunning = False
        self.actuators = ACTUATORS
        self.speech_recognition = None
        self.nltk = None

    def initialize(self):
        try:
            self.speech_recognition = SpeechRecognitionFacade()
            self.nltk = NltkFacade()
            
            for actuator in self.actuators:
                actuator_instance = actuator["class"]
                actuator_instance()

            self.isRunning = True
        except Exception as e:
            print(f"Erro ao iniciar o assistente: {str(e)}")
            logging.exception(str(e))

    def listen(self):
        if not self.isRunning:
            print("O assistente não foi iniciado corretamente.")
            return
        return self.speech_recognition.listen()
    
    def transcribe(self, speech):
        return self.speech_recognition.transcribe(speech)
    
    def get_tokens(self, transcription):
        return self.nltk.get_tokens(transcription)
    
    def is_tokens_valid(self, tokens):
        return self.nltk.is_tokens_valid(tokens)
    
    def act(self, tokens):
        action, main_param, secondary_params = app.nltk.get_action_and_params(tokens)
        app.__execute_action(app.actuators, action, main_param, secondary_params)
        
    def __execute_action(self, actuators, action, main_param, secondary_params):
        for actuator in actuators:
            actuator_instance = actuator["class"]
            process = Thread(target=actuator_instance.start, args=(actuator_instance, action, main_param, secondary_params))
            process.start()

if __name__ == "__main__":
    app = Main()
    app.initialize()

    while True:
        try:
            listen = app.listen()
            transcribe = app.transcribe(listen)
            tokens = app.get_tokens(transcribe)
            
            if app.is_tokens_valid(tokens) is False:
                print("Comando inválido. Por favor tente novamente.")
                continue
            
            app.act(tokens)
        except UnknownValueError:
            print("Erro ao processar a fala.")
        except KeyboardInterrupt:
            print("Desligando assistente virtual.")
            break
        except OSError as e:
            print(f"Erro de sistema operacional: {str(e)}.")
            break
        except LookupError as e:
            print(f"Erro de lookup: {str(e)}.")
            break
        except Exception as e:
            print(f"Erro ao processar comando: {str(e)}.")
            logging.exception(str(e))
