# encoding=utf-8
from celery.utils.log import get_logger
from celery import shared_task
from pathlib import Path
import time

# util
from transcriber.utils.whisper_util import WhisperUtil

# service
from transcriber.services.model.file_service import FileService

logger = get_logger(__name__)


@shared_task(
    retry_kwargs={'max_retries': 5, 'countdown': 3},
    time_limit=300,
    soft_time_limit=300)
def transcribe_task(file_path: str, file_id: str) -> bool:
    """
    transcribe audio task
    :param file_path: path of the file
    :type file_path: str
    :param file_id: file id of the audio file
    :type file_id: str
    :return: True if transcribe was a success else False
    :rtype: bool
    """
    try:
        # check if file exist
        if Path(file_path).is_file():

            file_service = FileService()
            whisper_service = WhisperUtil().get_whisper()
            logger.info("[transcribe_task]: is model initialized: %s", str(whisper_service is not None))

            # TODO: for testing, remove after
            time.sleep(15)
            result = whisper_service.transcribe(file_path=file_path)

            if result is not None:
                # mark transcribe status and set the text
                marked = file_service.update_transcribe_status(file_id=file_id, marked=True)
                if marked:
                    text_set = file_service.add_transcribed_text(file_id=file_id, text=result['text'])
                    if text_set:
                        return True
                    else:
                        logger.error("[transcribe_task]: error while setting text")
                        logger.error("[transcribe_task]: marking transcribe status to 'False' for file id '%s'",
                                     file_id)
                        file_service.update_transcribe_status(file_id=file_id, marked=False)
                else:
                    logger.error("[transcribe_task]: an error occurred while marking transcribe status")
            else:
                logger.error("[transcribe_task]: an error occurred while transcribing audio")

        else:
            logger.error("[transcribe_task]: the file '%s' does not exists", file_path)

    except Exception as e:
        logger.error("[transcribe_task]: %s", str(e))

    return False
