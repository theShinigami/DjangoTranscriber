# encoding=utf-8
import whisper
import logging
from pathlib import Path

# exception
from transcriber.exceptions.whisper_service_exception import FileNotFound


logger = logging.getLogger("service")


class WhisperService:
    def __init__(self, model: str = "base"):
        self.model = whisper.load_model(str(model))

    def transcribe(self, file_path: str) -> dict:
        """
        transcribe audio
        :param file_path: file to transcribe
        :type file_path str
        :return: transcribed text
        :rtype: dict
        :exception FileNotFound: throws if file does not exist
        """
        # check if file exists
        if not Path(file_path).is_file():
            raise FileNotFound("file does not exist!")

        result = self.model.transcribe(file_path)
        return result
