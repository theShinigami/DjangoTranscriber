# encoding=utf-8
from transcriber.exceptions.base import FileServiceBaseException


class UploadedFileNotFound(FileServiceBaseException):
    """throws if uploaded file is not found"""
    pass


class StatusUpdateError(FileServiceBaseException):
    """throws if it's unable to update status"""
    pass


class TextAddError(FileServiceBaseException):
    """throws if it's unable to add transcribed text"""
    pass


