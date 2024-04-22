import unittest
from unittest.mock import patch, MagicMock
from app.main import Main
from speech_recognition.exceptions import UnknownValueError
import threading


class TestMain(unittest.TestCase):
    def setUp(self):
        # Criar uma instância de Main para cada teste
        self.main_instance = Main()

    @patch('src.main.Activities')
    @patch('src.main.BrowserManager')
    def test_initialize(self, mock_browser_manager, mock_activities):
        # Chamar a função de inicialização
        self.main_instance.initialize()

        # Verificar se os atuadores foram instanciados corretamente
        mock_activities.assert_called_once()
        mock_browser_manager.assert_called_once()

        # Verificar se o assistente está rodando
        self.assertTrue(self.main_instance.isRunning)

    @patch('src.main.NltkFacade')
    @patch('src.main.SpeechRecognitionFacade')
    def test_execute(self, mock_speech_recognition, mock_nltk):
        # Mock para simular reconhecimento de fala
        mock_speech_recognition_instance = mock_speech_recognition.return_value
        mock_speech_recognition_instance.listen.return_value = "audio_data"
        mock_speech_recognition_instance.transcribe.return_value = "example command"

        # Mock para simular processamento do comando
        mock_nltk_instance = mock_nltk.return_value
        mock_nltk_instance.is_tokens_valid.return_value = True
        mock_nltk_instance.get_action_and_params.return_value = ("action", "main_param", ["param1", "param2"])

        # Iniciar o assistente
        self.main_instance.initialize()

        # Para testar a execução do loop, vamos executar em uma thread separada
        execute_thread = threading.Thread(target=self.main_instance.execute)
        execute_thread.start()

        # Certificar de que o loop iniciou
        import time
        time.sleep(1)  # Aguarde um pouco para o loop rodar

        # Verificar se o reconhecimento de fala foi chamado
        mock_speech_recognition_instance.listen.assert_called_once()
        mock_speech_recognition_instance.transcribe.assert_called_once_with("audio_data")

        # Terminar o loop
        self.main_instance.execute = lambda: None  # Interromper o loop forçando
        execute_thread.join()  # Aguarde a thread terminar

    @patch('src.main.NltkFacade')
    @patch('src.main.SpeechRecognitionFacade')
    def test_execute_unknown_value_error(self, mock_speech_recognition, mock_nltk):
        # Simular um erro de UnknownValueError
        mock_speech_recognition_instance = mock_speech_recognition.return_value
        mock_speech_recognition_instance.transcribe.side_effect = UnknownValueError()

        # Iniciar o assistente
        self.main_instance.initialize()

        # Para testar a execução do loop, vamos executar em uma thread separada
        execute_thread = threading.Thread(target=self.main_instance.execute)
        execute_thread.start()

        import time
        time.sleep(1)  # Aguarde um pouco para o loop rodar

        # Verificar se o erro foi capturado
        self.assertTrue(mock_speech_recognition_instance.transcribe.called)

        # Terminar o loop
        self.main_instance.execute = lambda: None  # Interromper o loop forçando
        execute_thread.join()  # Aguarde a thread terminar


if __name__ == "__main__":
    unittest.main()
