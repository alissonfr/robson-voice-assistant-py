import speech_recognition
from os import environ as env

class SpeechRecognitionFacade:
    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()

    def listen(self):
        with speech_recognition.Microphone() as audio_source:
            self.recognizer.adjust_for_ambient_noise(audio_source)
            print(f"{env.get('ASSISTANT_NAME')} está ouvindo...")
            listening_time = env.get("LISTENING_TIME")
            speech = self.recognizer.listen(audio_source, timeout=listening_time, phrase_time_limit=listening_time)
            
            return speech

    def transcribe(self, speech):
        transcription = self.recognizer.recognize_google(speech, language=env.get("SPEECH_LANGUAGE")).lower()
        return transcription