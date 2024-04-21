from nltk import word_tokenize, corpus
from os import environ

class NaturalLanguageAdapter:
    def __init__(self):
        self.palavras_de_parada = set(corpus.stopwords.words(environ.get("WORDS_LANGUAGE")))

    def obter_tokens(self, transcricao):
        return word_tokenize(transcricao)

    def eliminar_palavras_de_parada(self, tokens):
        tokens_filtrados = []

        for token in tokens:
            if token not in self.palavras_de_parada:
                tokens_filtrados.append(token)

        return tokens_filtrados