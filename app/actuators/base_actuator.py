from abc import ABC, abstractmethod

class BaseActuator(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def start(self, action, actuator_object, parameter):
        pass

    def default_action():
        print("Ação não encontrada.")