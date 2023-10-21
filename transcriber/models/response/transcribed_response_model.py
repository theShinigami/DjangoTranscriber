# encoding=utf-8


class Transcribed:
    def __init__(self, text: str, duration: float):
        """
        transcribed model
        :param text: transcribed model
        :type text: str
        :param duration: time taken
        :type duration: float
        """
        self.text = str(text)
        self.duration = duration

    def dict(self):
        """
        return obj dict
        :return: dict
        """
        return self.__dict__
