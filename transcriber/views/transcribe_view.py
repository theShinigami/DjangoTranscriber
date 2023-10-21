# encoding=utf-8
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

# model
from transcriber.models.response.response_model import ResponseModel

# service
from transcriber.services.transcriber_service import TranscriberService

# serializer
from transcriber.serializers.response.response_serializer import ResponseSerializer
from transcriber.serializers.transcribe_serializer import TranscribeSerializer

logger = logging.getLogger(__name__)


class TranscribeView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = TranscribeSerializer
    transcriber_service = TranscriberService()
    whitelist_content_type = ["audio/mpeg"]

    def post(self, request, *args, **kwargs):
        errors = list()
        response_status = status.HTTP_200_OK

        # check if request data is not empty
        if request.data is None:
            logger.error("[TranscribeView]: invalid request body")

            errors.append("invalid request body")
            response_status = status.HTTP_400_BAD_REQUEST

        if len(errors) == 0:
            serialized = self.serializer_class(data=request.data)

            if serialized.is_valid():
                file = request.FILES.get("file")
                if file.content_type not in self.whitelist_content_type:
                    logger.error("[TranscribeView]: invalid content type: %s", file.content_type)
                    errors.append("invalid file type")
                    response_status = status.HTTP_400_BAD_REQUEST
                else:
                    result = serialized.save()
                    file_id = str(result.file_id)
                    transcribed = self.transcriber_service.transcribe_now(file_id)
                    res = ResponseModel(data=transcribed.dict(), success=True)
                    return Response(data=ResponseSerializer(res).data, status=response_status)
            else:
                logger.error("[TranscribeView]: invalid request data!")

                errors.append("bad request")
                response_status = status.HTTP_400_BAD_REQUEST

        if len(errors) > 0:
            response = ResponseModel(data={"error": errors}, success=False)
            return Response(data=ResponseSerializer(response).data, status=response_status)
