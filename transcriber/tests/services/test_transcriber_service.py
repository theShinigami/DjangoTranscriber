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
    TEST_FILE_PATH = "test_file_001.mp3"

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

    def test_transcribe_queue(self):
        transcriber_service = TranscriberService()
        queued_task = transcriber_service.transcribe_queue(file_id=self.FILE_ID)

        self.assertIsNotNone(queued_task)
        self.assertTrue(len(queued_task.msg) > 0)

    def test_get_transcribed_audio(self):
        transcriber_service = TranscriberService()
        file = transcriber_service.get_transcribed_audio(file_id=self.FILE_ID)

        self.assertIsNotNone(file)
        self.assertEqual(file.file_id, self.FILE_ID)
