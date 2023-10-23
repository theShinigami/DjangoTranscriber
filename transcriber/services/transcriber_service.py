# encoding=utf-8
import logging
from django.conf import settings
import time

# service
from transcriber.services.model.file_service import FileService

# util
from transcriber.utils.whisper_util import WhisperUtil

# model
from transcriber.models.response.transcribed_response_model import Transcribed
from transcriber.models.response.transcribed_fetch_response_model import TranscribedFetch
from transcriber.models.response.transcribed_queue_status_response import TranscribedQueueResponse

# exception
from transcriber.exceptions.transcriber_service_exception import InstantTranscribeError
from transcriber.exceptions.transcriber_service_exception import TranscribeDataFetchError
from transcriber.exceptions.transcriber_service_exception import QueueTranscribeError

# celery app
from config.celery_app import app

logger = logging.getLogger("service")


class TranscriberService:
    def __init__(self):
        self.whisper_service = WhisperUtil().get_whisper()
        self.file_service = FileService()

    def transcribe_now(self, file_id: str) -> Transcribed:
        """
        transcribe audio instantly
        :param file_id: unique file id
        :type file_id: str
        :return: Transcribed model
        :rtype: Transcribed
        :exception InstantTranscribeError: raises if it encounters any error while transcribing audio
        """
        try:
            # to calculate duration
            start_time = time.time()

            logger.info("[transcribe_now]: fetching file with id '%s'", file_id)
            file = self.file_service.get_file_by_file_id(file_id=file_id)
            # construct file path
            file_path = "{}/media/{}".format(str(settings.BASE_DIR), str(file.file))

            logger.info("[transcribe_now]: transcribing: %s", file_path)

            result = self.whisper_service.transcribe(file_path=file_path)

            if result is not None:
                marked = self.file_service.update_transcribe_status(file_id=file_id, marked=True)
                if marked:
                    logger.info("[transcribe_now]: file id %s marked to %s", str(file_id), str(marked))
                    text_added = self.file_service.add_transcribed_text(file_id=file_id, text=result['text'])
                    if text_added:
                        logger.info("[transcribe_now]: file %s transcribed text added", str(file_id))
                    else:
                        raise InstantTranscribeError("unable to save transcribed text")
                else:
                    raise InstantTranscribeError("unable to mark transcribed text")

                return Transcribed(
                    text=result['text'],
                    transcribed=marked,
                    duration=(time.time() - start_time)
                )

        except Exception as e:
            logger.error("[transcribe_now]: %s", str(e))

        raise InstantTranscribeError("error while transcribing audio")

    def transcribe_queue(self, file_id: str) -> TranscribedQueueResponse:
        """
        transcribe task with queue
        :param file_id: id of the upload file
        :type file_id: str
        :return: transcribe queue response model
        :rtype: TranscribedQueueResponse
        :exception QueueTranscribeError: raises if it encounters error while queuing transcribe task
        """
        try:

            # to calculate duration
            start_time = time.time()

            logger.error("[transcribe_queue]: checking if file exists")
            if not self.file_service.is_file_exists_by_uuid(file_id=file_id):
                logger.error("[transcribe_queue]: the file with an id '%s' does not exists", str(file_id))
                raise QueueTranscribeError("file not found!")

            logger.info("[transcribe_queue]: fetching file with id '%s'", file_id)
            file = self.file_service.get_file_by_file_id(file_id=file_id)
            # construct file path
            file_path = "{}/media/{}".format(str(settings.BASE_DIR), str(file.file))

            logger.error("[transcribe_queue]: queuing task...")
            transcribe_task_status = app.send_task(
                name="transcriber.tasks.transcriber_tasks.transcribe_task", args=(file_path, file_id,))

            if transcribe_task_status is not None:
                logger.info("[transcribe_queue]: transcribe task id: %s", str(transcribe_task_status.id))
                return TranscribedQueueResponse(
                    msg="transcribe in progress",
                    file_id=file_id,
                    duration=time.time() - start_time
                )

            raise QueueTranscribeError("error while queuing tasking")

        except Exception as e:
            logger.error("[transcribe_queue]: %s", str(e))

        raise QueueTranscribeError("error while queuing task")

    def get_transcribed_audio(self, file_id: str) -> TranscribedFetch:
        """
        fetch transcribed file
        :param file_id: transcribed audio file id
        :type file_id: str
        :return: transcribed fetch response model
        :rtype: TranscribedFetch
        :exception TranscribeDataFetchError: raises if it encounters an error while fetching transcribed file
        """
        try:

            # check if file exists or not
            if self.file_service.is_file_exists_by_uuid(file_id=file_id):
                file = self.file_service.get_file_by_file_id(file_id=file_id)
                return TranscribedFetch(
                    text=file.transcribed_text,
                    file_id=str(file.file_id),
                    in_progress=not file.is_transcribed
                )
            else:
                logger.error("[get_transcribed_audio]: file by the id '%s' is not found", file_id)
                raise TranscribeDataFetchError("file not found")

        except Exception as e:
            logger.error("[get_transcribed_audio]: %s", str(e))

        raise TranscribeDataFetchError("an error has occurred while fetching transcribed file")
