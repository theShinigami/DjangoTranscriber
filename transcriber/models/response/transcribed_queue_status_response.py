# encoding=utf-8


class TranscribedQueueResponse:
    def __init__(self, msg: str, file_id: str, duration: float):
        """
        transcribed queue status response model
        :param msg: message
        :type msg: str
        :param file_id: upload file id
        :type file_id: str
        :param duration: time taken
        :type duration: float
        """
        self.msg = str(msg)
        self.file_id = file_id
        self.duration = duration

    def dict(self):
        """
        return obj dict
        :return: dict
        """
        return self.__dict__
