from actuators.base_actuator import BaseActuator

ACTIVITIES_FILE = "activities.txt"

class Activities(BaseActuator):
    def __init__(self):
        return None

    def start(self, action, main_param, secondary_params):

        if main_param == "atividade":

            if len(secondary_params) == 0:
                print("O nome da atividade não foi informada.")
                return

            activity_name = " ".join(secondary_params).strip()
            activity_name = activity_name.lower()

            if action == "adicionar":
                self.__add_activitie(self, activity_name)
            elif action == "remover":
                self.__remove_activitie(self, activity_name)

    def __add_activitie(self, activity_name):
        activities = self.__load_activities(self)

        if activity_name in activities:
            print(f"A atividade '{activity_name}' já existe.")
        else:
            activities.add(activity_name)
            self.__save_activities(self, activities)
            print(f"Atividade '{activity_name}' adicionada.")

    def __remove_activitie(self, activity_name):
        activities = self.__load_activities(self)

        if activity_name not in activities:
            print(f"A atividade '{activity_name}' não foi encontrada.")
        else:
            activities.remove(activity_name)
            self.__save_activities(self, activities)
            print(f"Atividade '{activity_name}' removida.")

    def __load_activities(self):
        try:
            with open(ACTIVITIES_FILE, "r") as file:
                activities = set(file.read().splitlines())
            return activities
        except FileNotFoundError:
            return set()

    def __save_activities(self, activities):
        with open(ACTIVITIES_FILE, "w") as file:
            for activity in activities:
                file.write(activity + "\n")