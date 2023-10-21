# encoding=utf-8
import logging

# model
from transcriber.models.entities.File import File

# exception
from transcriber.exceptions.file_service_exception import UploadedFileNotFound
from transcriber.exceptions.file_service_exception import StatusUpdateError
from transcriber.exceptions.file_service_exception import TextAddError

logger = logging.getLogger("service")


class FileService:
    def __init__(self):
        pass

    @staticmethod
    def is_file_exists_by_uuid(file_id: str) -> bool:
        """
        check if file exists by file id (UUID)
        :param file_id: uuid file id
        :type file_id: uuid str
        :return: bool
        :rtype: bool
        """
        return File.objects.filter(file_id=file_id).exists()

    @staticmethod
    def get_file_by_file_id(file_id: str) -> File:
        """
        get file by file id
        :param file_id: uuid file id
        :type file_id: uuid str
        :return: file model
        :rtype: File
        :exception UploadedFileNotFound: raises if uploaded file is not found
        """
        try:
            return File.objects.filter(file_id=file_id).first()
        except Exception as e:
            logger.error("[get_file_by_file_id]: %s", str(e))

        raise UploadedFileNotFound("unable to find file")

    @staticmethod
    def update_transcribe_status(file_id: str, marked: bool) -> bool:
        """
        update transcribe status by file id
        :param file_id: uuid file id
        :type file_id: uuid str
        :param marked: status
        :type marked: bool
        :return: bool
        :rtype: bool
        :exception StatusUpdateError: raises if it's unable to update the status
        """
        try:
            file_to_update = File.objects.filter(file_id=file_id).first()
            file_to_update.is_transcribed = marked
            file_to_update.save()
            return True
        except Exception as e:
            logger.error("[update_transcribe_status]: %s", str(e))

        raise StatusUpdateError("unable to update status")

    @staticmethod
    def add_transcribed_text(file_id: str, text: str) -> bool:
        """
        add transcribed text
        :param file_id: unique uuid file id
        :type file_id: str
        :param text: transcribed text
        :type text: str
        :return: returns True if the update is a success
        :rtype: bool
        :exception TextAddError: raises if it's unable to add transcribed text
        """
        try:
            file_to_update = File.objects.filter(file_id=file_id).first()
            file_to_update.transcribed_text = text
            file_to_update.save()
            return True
        except Exception as e:
            logger.error("[add_transcribed_text]: %s", str(e))

        raise TextAddError("unable to add transcribed text")
