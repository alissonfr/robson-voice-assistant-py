import unittest
from unittest.mock import patch
import speech_recognition as sr
from os import environ as env
from ..facades import SpeechRecognitionFacade

from os import path

ROOT_DIR = path.abspath(path.join(path.dirname(__file__), ".."))
AUDIO_FILE = path.join(ROOT_DIR, "chamando-robson.wav")

class TestSpeechRecognitionFacade(unittest.TestCase):
    @patch("speech_recognition.Recognizer.recognize_google")
    @patch("speech_recognition.Recognizer.listen")
    def test_transcribe_with_real_audio(self, mock_listen, mock_recognize_google):
        mock_recognize_google.return_value = "joana ligar a lampada"

        audio_path = AUDIO_FILE
        with open(audio_path, "rb") as audio_file:
            fake_audio = sr.AudioData(audio_file.read(), 16000, 1)

        mock_listen.return_value = fake_audio

        env['SPEECH_LANGUAGE'] = "pt-BR"

        facade = SpeechRecognitionFacade()

        speech = facade.listen()
        transcription = facade.transcribe(speech)

        mock_listen.assert_called_once()

        mock_recognize_google.assert_called_once_with(
            fake_audio,
            language="pt-BR"
        )

        self.assertEqual(transcription, "joana ligar a lampada")


# Execute os testes
if __name__ == '__main__':
    unittest.main()
