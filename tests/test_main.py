from os import path, environ as env
from unittest import TestCase, TestLoader, TestSuite, TextTestRunner
from speech_recognition import AudioFile
import sys

ROOT_FOLDER = path.abspath(path.join(path.dirname(__file__), '..'))
TESTS_FOLDER = path.join(ROOT_FOLDER, 'tests')
AUDIOS_FOLDER = path.join(TESTS_FOLDER, 'audios')

# Áudios pessimistas
SILENCE_AUDIO = path.join(AUDIOS_FOLDER, 'invalid_commands\\silencio.wav')
WRONG_ASSISTANT_AUDIO = path.join(AUDIOS_FOLDER, 'invalid_commands\\joana-abrir-calendario.wav')
SCHEDULE_MEETING_AUDIO = path.join(AUDIOS_FOLDER, 'invalid_commands\\marcar-reuniao.wav')

# Áudios otimistas
OPEN_CALENDAR_AUDIO = path.join(AUDIOS_FOLDER, 'command\\abrir-calendario.wav')
OPEN_EMAIL_AUDIO = path.join(AUDIOS_FOLDER, 'command\\abrir-email.wav')
SEARCH_GOOGLE_AUDIO = path.join(AUDIOS_FOLDER, 'command\\pesquisar-google.wav')
SEARCH_BING_AUDIO = path.join(AUDIOS_FOLDER, 'command\\pesquisar-bing.wav')
ADD_ATICTIVITY_AUDIO = path.join(AUDIOS_FOLDER, 'command\\adicionar-atividade-ler-livro.wav')
REMOVE_ATICTIVITY_AUDIO = path.join(AUDIOS_FOLDER, 'command\\remover-atividade-ler-livro.wav')

sys.path.append(ROOT_FOLDER)

from app.main import Main

class TestBase(TestCase):
    def setUp(self):
        self.app = Main()
        self.app.initialize()

    def speech_from_audio_file(self, audio_path):
        with AudioFile(audio_path) as audio_source:
            return self.app.speech_recognition.recognizer.listen(audio_source)

    def transcribe_and_tokenize(self, audio_file_path):
        transcription = self.app.transcribe(self.speech_from_audio_file(audio_file_path))
        return self.app.get_tokens(transcription)

class TestValidations(TestBase):
    def test_silence(self):
        is_valid = False
        try:
            tokens = self.transcribe_and_tokenize(SILENCE_AUDIO)
            self.app.is_tokens_valid(tokens)
            is_valid = True
        except Exception:
            pass

        self.assertFalse(is_valid)
    
    def test_invalid_action(self):
        is_valid = False
        try:
            tokens = self.transcribe_and_tokenize(SCHEDULE_MEETING_AUDIO)
            self.app.act(tokens)
            is_valid = True
        except Exception:
            pass

        self.assertFalse(is_valid)
        
    def test_assistant_name(self):
        tokens = self.transcribe_and_tokenize(OPEN_CALENDAR_AUDIO)

        self.assertEqual(tokens[0], env.get("ASSISTANT_NAME"))
        
    def test_wrong_assistant_name(self):
        tokens = self.transcribe_and_tokenize(WRONG_ASSISTANT_AUDIO)

        self.assertNotEqual(tokens[0], env.get("ASSISTANT_NAME"))

class TestBrowserManager(TestBase):
    def test_calendar_audio(self):
        tokens = self.transcribe_and_tokenize(OPEN_CALENDAR_AUDIO)

        self.assertTrue(self.app.is_tokens_valid(tokens))
        self.assertEqual(" ".join(tokens), "robson abrir calendário")

    def test_email_audio(self):
        tokens = self.transcribe_and_tokenize(OPEN_EMAIL_AUDIO)

        self.assertTrue(self.app.is_tokens_valid(tokens))
        self.assertEqual(" ".join(tokens), "robson abrir e-mail")

    def test_google_search(self):
        tokens = self.transcribe_and_tokenize(SEARCH_GOOGLE_AUDIO)

        self.assertTrue(self.app.is_tokens_valid(tokens))
        self.assertEqual(" ".join(tokens), "robson pesquisar google")

    def test_bing_search(self):
        tokens = self.transcribe_and_tokenize(SEARCH_BING_AUDIO)

        self.assertTrue(self.app.is_tokens_valid(tokens))
        self.assertEqual(" ".join(tokens), "robson pesquisar bing")

class TestActivities(TestBase):
    def test_add_activity(self):
        tokens = self.transcribe_and_tokenize(ADD_ATICTIVITY_AUDIO)

        self.assertTrue(self.app.is_tokens_valid(tokens))
        self.assertEqual(" ".join(tokens), "robson adicionar atividade ler livro")

    def test_remove_activity(self):
        tokens = self.transcribe_and_tokenize(REMOVE_ATICTIVITY_AUDIO)

        self.assertTrue(self.app.is_tokens_valid(tokens))
        self.assertEqual(" ".join(tokens), "robson remover atividade ler livro")

if __name__ == '__main__':
    test_loader = TestLoader()
    tests = TestSuite()
    test_cases = [TestValidations, TestBrowserManager, TestActivities]
    test_runner = TextTestRunner()

    for test_case in test_cases:
        tests.addTests(test_loader.loadTestsFromTestCase(test_case))

    test_runner.run(tests)