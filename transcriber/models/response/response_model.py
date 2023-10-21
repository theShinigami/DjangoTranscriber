# encoding=utf-8

from datetime import datetime


class ResponseModel:
    def __init__(self, data: object, success: bool, time=None):
        """
        response model wrapper
        :param data: data obj
        :type data: object
        :param success: response status
        :type success: bool
        :param time: response time
        :type time: datetime
        """
        self.data = data
        self.success = success
        self.time = time or datetime.now()
