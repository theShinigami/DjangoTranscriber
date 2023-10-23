# encoding=utf-8
from transcriber.exceptions.base import TranscriberServiceBaseException


class InstantTranscribeError(TranscriberServiceBaseException):
    """throws if it encounters an error while transcribing"""
    pass


class QueueTranscribeError(TranscriberServiceBaseException):
    """throws if it encounters an error while queuing task"""
    pass


class TranscribeDataFetchError(TranscriberServiceBaseException):
    """throws if an error encounters while fetching transcribed file"""
    pass
