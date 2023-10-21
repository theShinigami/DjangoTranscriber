from django.test import TestCase
import logging
import time

# service
from transcriber.services.whisper_service import WhisperService

# exception
from transcriber.exceptions.whisper_service_exception import FileNotFound

# logging
logger = logging.getLogger(__name__)


class WhisperServiceTest(TestCase):
    TEST_FILE_PATH = "transcriber/tests/services/test_files/test_file_001.mp3"

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_transcribe_method_when_file_does_not_exists(self):
        whisper_service = WhisperService()

        def raises_file_not_found():
            whisper_service.transcribe(file_path=self.TEST_FILE_PATH + str(int(time.time())))

        self.assertRaises(FileNotFound, raises_file_not_found)

    def test_transcribe_method_to_transcribe_test_audio_file(self):
        whisper_service = WhisperService()

        result = whisper_service.transcribe(file_path=self.TEST_FILE_PATH)
        self.assertIsNotNone(result)
        self.assertTrue(len(result['text']) > 0)
