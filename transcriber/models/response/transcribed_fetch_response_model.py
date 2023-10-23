# encoding=utf-8


class TranscribedFetch:
    def __init__(self, text: str, file_id: str, in_progress: bool):
        """
        transcribe fetch response model
        :param text: transcribed text
        :type text: str
        :param file_id: transcribed file id
        :type file_id: str
        :param in_progress: indicator if file is transcribed or not
        :type in_progress: bool
        """
        self.text = str(text)
        self.file_id = file_id
        self.in_progress = in_progress

    def dict(self):
        """
        return obj dict
        :return: dict
        """
        return self.__dict__
