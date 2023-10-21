from django.test import TestCase
import logging

# service
from transcriber.services.transcriber_service import TranscriberService

# model
from transcriber.models.entities.File import File

# logging
logger = logging.getLogger(__name__)


class TranscriberServiceTest(TestCase):
    FILE_ID = "01dfa145-4ddf-4fbb-8740-2465f40e2d70"
    TEST_FILE_PATH = "transcriber/tests/services/test_files/test_file_001.mp3"

    def setUp(self) -> None:
        # create a sample file
        new_file = File(file_id=self.FILE_ID, file=self.TEST_FILE_PATH)
        new_file.save()

    def tearDown(self) -> None:
        File.objects.all().delete()

    def test_transcribe_now(self):
        transcriber_service = TranscriberService()
        transcribed = transcriber_service.transcribe_now(file_id=self.FILE_ID)

        self.assertIsNotNone(transcribed)
        self.assertTrue(len(transcribed.text) > 0)
