# encoding=utf-8
from django.urls import re_path

# views
from transcriber.views.transcribe_view import TranscribeView

urlpatterns = [
    re_path("^transcribe/$", TranscribeView.as_view()),
]
