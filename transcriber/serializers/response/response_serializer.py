# encoding=utf-8
from rest_framework import serializers

from transcriber.models.response.response_model import ResponseModel


class ResponseSerializer(serializers.Serializer):
    class Meta:
        model = ResponseModel

    data = serializers.SerializerMethodField()
    success = serializers.BooleanField()
    time = serializers.DateTimeField()

    def get_data(self, obj):
        return obj.data

