from django.db import models
from uuid import uuid4


class File(models.Model):
    """file field"""
    file = models.FileField()
    """alternate file id"""
    file_id = models.UUIDField()
    """flag to check if file is transcribed or not"""
    is_transcribed = models.BooleanField(default=False)
    # TODO: change this to a file
    """transcribed text"""
    transcribed_text = models.TextField(null=True)
    """tracks last update"""
    last_update = models.DateTimeField(auto_now=True)
    """created date"""
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "files"
        app_label = "transcriber"
