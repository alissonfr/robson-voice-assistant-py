from os import path, environ as env
from unittest import TestCase, TestLoader, TestSuite, TextTestRunner
from unittest.mock import patch
from speech_recognition import AudioFile
import sys

ROOT_FOLDER = path.abspath(path.join(path.dirname(__file__), '..'))
TESTS_FOLDER = path.join(ROOT_FOLDER, 'tests')
AUDIOS_FOLDER = path.join(TESTS_FOLDER, 'audios')

# Áudios pessimistas
SILENCE_AUDIO = path.join(AUDIOS_FOLDER, 'pessimistic\\silencio.wav') #
WRONG_ASSISTANT_AUDIO = path.join(AUDIOS_FOLDER, 'pessimistic\\joana-abrir-calendario.wav') #
SCHEDULE_MEETING_AUDIO = path.join(AUDIOS_FOLDER, 'pessimistic\\marcar-reuniao.wav')

# Áudios otimistas
OPEN_CALENDAR_AUDIO = path.join(AUDIOS_FOLDER, 'optimistic\\abrir-calendario.wav')#
OPEN_EMAIL_AUDIO = path.join(AUDIOS_FOLDER, 'optimistic\\abrir-email.wav')#
SEARCH_GOOGLE_AUDIO = path.join(AUDIOS_FOLDER, 'optimistic\\pesquisar-google.wav')
SEARCH_BING_AUDIO = path.join(AUDIOS_FOLDER, 'optimistic\\pesquisar-bing.wav')
ADD_ATICTIVITY_AUDIO = path.join(AUDIOS_FOLDER, 'optimistic\\adicionar-atividade-ler-livro.wav')
REMOVE_ATICTIVITY_AUDIO = path.join(AUDIOS_FOLDER, 'optimistic\\remover-atividade-ler-livro.wav')

sys.path.append(ROOT_FOLDER)

from app.main import Main

class TestBase(TestCase):
    def setUp(self):
        self.app = Main()
        self.app.initialize()

    def transcribe_and_tokenize(self, audio_file_path, expected_transcription):
        with AudioFile(audio_file_path) as source:
            recorded_audio = self.app.speech_recognition.recognizer.record(source)

        with patch('speech_recognition.Recognizer.recognize_google') as mock_recognize_google:
            mock_recognize_google.return_value = expected_transcription
            transcription = self.app.transcribe_and_validate(recorded_audio)
            is_valid, tokens = self.app.get_tokens_and_validate(transcription)
            
        return is_valid, tokens

class TestValidations(TestBase):
    @patch('speech_recognition.Recognizer.listen')
    def test_silence(self, mock_listen):
        mock_listen.return_value = self.app.speech_recognition.recognizer.record
        is_valid = self.transcribe_and_tokenize(SILENCE_AUDIO, "")

        self.assertFalse(is_valid)
        
    def test_invalid_action():
        SCHEDULE_MEETING_AUDIO
        pass
        
    @patch('speech_recognition.Recognizer.listen')
    def test_assistant_name(self, mock_listen):
        mock_listen.return_value = self.app.speech_recognition.recognizer.record
        tokens = self.transcribe_and_tokenize(OPEN_CALENDAR_AUDIO, "robson abrir calendário")

        self.assertEqual(tokens[0], env.get("ASSISTANT_NAME"))
        
    @patch('speech_recognition.Recognizer.listen')
    def test_not_assistant_name(self, mock_listen):
        mock_listen.return_value = self.app.speech_recognition.recognizer.record
        tokens = self.transcribe_and_tokenize(WRONG_ASSISTANT_AUDIO, "joana abrir calendario")

        self.assertNotEqual(tokens[0], env.get("ASSISTANT_NAME"))

class TestBrowserManager(TestBase):
    @patch('speech_recognition.Recognizer.listen')
    def test_calendar_audio(self, mock_listen):
        mock_listen.return_value = self.app.speech_recognition.recognizer.record
        tokens = self.transcribe_and_tokenize(OPEN_CALENDAR_AUDIO, "robson abrir calendário")

        self.assertEqual(" ".join(tokens), "robson abrir calendário")

    @patch('speech_recognition.Recognizer.listen')
    def test_email_audio(self, mock_listen):
        mock_listen.return_value = self.app.speech_recognition.recognizer.record
        tokens = self.transcribe_and_tokenize(OPEN_EMAIL_AUDIO, "robson abrir e-mail")

        self.assertEqual(" ".join(tokens), "robson abrir e-mail")

    def tearDown(self):
        # Limpeza após cada teste (se necessário)
        pass

if __name__ == '__main__':
    test_loader = TestLoader()
    tests = TestSuite()
    test_cases = [TestValidations, TestBrowserManager]
    test_runner = TextTestRunner()

    for test_case in test_cases:
        tests.addTests(test_loader.loadTestsFromTestCase(test_case))

    test_runner.run(tests)