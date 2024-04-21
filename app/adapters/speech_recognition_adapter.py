import speech_recognition
from os import environ

class SpeechRecognitionAdapter:
    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()

    def listen(self):
        with speech_recognition.Microphone() as audio_source:
            self.recognizer.adjust_for_ambient_noise(audio_source)
            print("Listening...")
            speech = self.recognizer.listen(audio_source, timeout=int(environ.get("LISTENING_TIME")), phrase_time_limit=int(environ.get("LISTENING_TIME")))
        return speech

    def transcribe(self, fala):
        transcription = self.recognizer.recognize_google(fala, language=environ.get("SPEECH_LANGUAGE")).lower()
        return transcription