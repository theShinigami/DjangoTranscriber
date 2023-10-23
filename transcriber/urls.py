# encoding=utf-8
from django.urls import re_path

# views
from transcriber.views.transcribe_view import TranscribeView, TranscribedFetch, TranscribeQueueView

urlpatterns = [
    re_path("^transcribe/$", TranscribeView.as_view()),
    re_path("^transcribe/queue/$", TranscribeQueueView.as_view()),
    re_path("^get/(?P<id>[0-9a-f-]+)$", TranscribedFetch.as_view()),
]
