import json
from nltk import word_tokenize, corpus
from os import environ as env

class NltkFacade:
    def __init__(self):
        self.stop_words = set(corpus.stopwords.words(env.get("WORDS_LANGUAGE")))

    def get_tokens(self, transcription):
        tokens = word_tokenize(transcription)
        tokens = [token for token in tokens if token not in self.stop_words]
        return tokens
    
    def is_tokens_valid(self, tokens):
        return len(tokens) >= 3 and tokens[0] == env.get("ASSISTANT_NAME")

    def get_action_and_params(self, tokens):
        actuator_actions = self.__get_config_file(env.get("CONFIG_FILE_PATH"))["actions"]

        action = tokens[1]
        main_param = tokens[2]
        secondary_params = tokens[3:]

        for actuator_action in actuator_actions:
            if action == actuator_action["name"] and main_param in actuator_action["params"]:
                return action, main_param, secondary_params
        
        raise Exception("Nome ou objeto autuador incorreto.")
    
    def __get_config_file(self, path):
        with open(path, "r", encoding="utf-8") as file:
            config_file = json.load(file)
            return config_file