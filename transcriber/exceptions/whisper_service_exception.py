# encoding=utf-8
from transcriber.exceptions.base import WhisperServiceBaseException


class FileNotFound(WhisperServiceBaseException):
    """file not found"""
    pass

