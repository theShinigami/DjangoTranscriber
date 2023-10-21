from django.contrib import admin

# model
from transcriber.models.entities.File import File


@admin.register(File)
class FilesAdmin(admin.ModelAdmin):
    list_display = ("file_id", "file", "is_transcribed", "last_update", "created_at",)



