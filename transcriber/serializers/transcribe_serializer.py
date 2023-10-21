from rest_framework.serializers import ModelSerializer

# model
from transcriber.models.entities.File import File


class TranscribeSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = ['file']
