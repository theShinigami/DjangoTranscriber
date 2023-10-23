from django.test import TestCase
import logging

# util
from transcriber.utils.whisper_util import WhisperUtil

# service
from transcriber.services.whisper_service import WhisperService

# logging
logger = logging.getLogger(__name__)


class WhisperUtilTest(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_get_whisper(self):
        whisper_util = WhisperUtil()
        whisper_service = whisper_util.get_whisper()

        self.assertIsNotNone(whisper_service)
        self.assertIsInstance(whisper_service, WhisperService)

