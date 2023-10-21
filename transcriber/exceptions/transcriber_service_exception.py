# encoding=utf-8
from transcriber.exceptions.base import TranscriberServiceBaseException


class InstantTranscribeError(TranscriberServiceBaseException):
    """throws if it encounters an error while transcribing"""
    pass
