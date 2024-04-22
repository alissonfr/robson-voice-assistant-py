from abc import ABC, abstractmethod

class BaseActuator(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def start(self, action, main_param, secondary_params):
        pass