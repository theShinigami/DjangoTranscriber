from django.test import TestCase
import logging

# service
from transcriber.services.model.file_service import FileService

# model
from transcriber.models.entities.File import File

# logging
logger = logging.getLogger(__name__)


class FileServiceTest(TestCase):
    FILE_ID = "01dfa145-4ddf-4fbb-8740-2465f40e2d70"

    def setUp(self) -> None:
        # create a sample file
        new_file = File(file_id=self.FILE_ID)
        new_file.save()

    def tearDown(self) -> None:
        File.objects.all().delete()

    def test_is_file_exists_by_uuid(self):
        file_service = FileService()
        exists = file_service.is_file_exists_by_uuid(file_id=self.FILE_ID)
        self.assertTrue(exists)

    def test_get_file_by_file_id(self):
        file_service = FileService()
        file = file_service.get_file_by_file_id(file_id=self.FILE_ID)

        self.assertIsNotNone(file)
        self.assertEqual(str(file.file_id), self.FILE_ID)

    def test_update_transcribe_status(self):
        file_service = FileService()

        is_updated_1 = file_service.update_transcribe_status(file_id=self.FILE_ID, marked=True)
        self.assertTrue(is_updated_1)

        # check
        updated_file_1 = File.objects.filter(file_id=self.FILE_ID).first()
        self.assertTrue(updated_file_1.is_transcribed)

        # update again
        is_updated_2 = file_service.update_transcribe_status(file_id=self.FILE_ID, marked=False)
        self.assertTrue(is_updated_2)

        # check again
        updated_file_2 = File.objects.filter(file_id=self.FILE_ID).first()
        self.assertFalse(updated_file_2.is_transcribed)

    def test_add_transcribed_text(self):
        sample_text = """
        this is a sample text to add
        """
        file_service = FileService()

        is_added = file_service.add_transcribed_text(file_id=self.FILE_ID, text=sample_text)
        self.assertTrue(is_added)

        # check
        added_text_file = File.objects.filter(file_id=self.FILE_ID).first()
        self.assertEqual(added_text_file.transcribed_text, sample_text)
