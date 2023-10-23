# encoding=utf-8


class Transcribed:
    def __init__(self, text: str, transcribed: bool, duration: float):
        """
        transcribed model
        :param text: transcribed model
        :type text: str
        :param transcribed: transcribe indicator
        :type transcribed: bool
        :param duration: time taken
        :type duration: float
        """
        self.text = str(text)
        self.transcribed = transcribed
        self.duration = duration

    def dict(self):
        """
        return obj dict
        :return: dict
        """
        return self.__dict__
