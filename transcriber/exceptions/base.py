# encoding=utf-8

class Error(Exception):
    """base class for sub exceptions"""


class WhisperServiceBaseException(Error):
    """WhisperService base exception"""
    pass


class TranscriberServiceBaseException(Error):
    """Transcriber base exception"""
    pass


class FileServiceBaseException(Error):
    """File service base exception"""
    pass

