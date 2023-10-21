# encoding=utf-8
import logging
from django.conf import settings
import time

# service
from transcriber.services.whisper_service import WhisperService
from transcriber.services.model.file_service import FileService

# model
from transcriber.models.response.transcribed_response_model import Transcribed

# exception
from transcriber.exceptions.transcriber_service_exception import InstantTranscribeError

logger = logging.getLogger("service")


class TranscriberService:
    def __init__(self):
        self.whisper_service = WhisperService()
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
                    duration=(time.time() - start_time)
                )

        except Exception as e:
            logger.error("[transcribe_now]: %s", str(e))

        raise InstantTranscribeError("error while transcribing audio")
