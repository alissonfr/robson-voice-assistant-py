from nltk import word_tokenize, corpus
from os import environ as env
from helpers.json_helper import get_config_file

class NltkFacade:
    def __init__(self):
        self.stop_words = set(corpus.stopwords.words(env.get("WORDS_LANGUAGE")))
        self.tokens = None

    def generate_tokens(self, transcription):
        tokens = word_tokenize(transcription)
        self.tokens = [token for token in tokens if token not in self.stop_words]
        print(self.tokens)
    
    def is_tokens_valid(self):
        return len(self.tokens) >= 3 and self.tokens[0] == env.get("ASSISTANT_NAME")

    def get_action_and_object(self):
        actuator_actions = get_config_file(env.get("CONFIG_FILE_PATH"))["actions"]

        action = self.tokens[1]
        actuator_object = self.tokens[2]

        for actuator_action in actuator_actions:
            if action == actuator_action["name"] and actuator_object in actuator_action["objects"]:
                return action, actuator_object
        
        raise Exception("Nome ou objeto autuador incorreto.")