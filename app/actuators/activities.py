from actuators.base_actuator import BaseActuator

class Activities(BaseActuator):
    def __init__(self):
        return None

    def start(self, action, actuator_object, parameter):
        print("action: ", action)
        print("actuator_object: ", actuator_object)
        print("parameter: ", parameter)

        if action == "adicionar" and actuator_object == "atividade":
            self.__add_activitie()
        elif action == "remover" and actuator_object == "atividade":
            self.__remove_activitie()

    def __add_activitie():
        print("adicionando")

    def __remove_activitie():
        print("removendo")