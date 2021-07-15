import logging
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Shop

logger = logging.getLogger(__name__)


class AskConv(generics.GenericAPIView):

    queryset = Shop.objects.all()

    def get_actions(self, request, *args, **kwargs):
        super(AskConv, self).get_actions(request, args, kwargs)

        instance = self.get_object()

        serializer = self.get_serializer(instance)

        data = serializer.data

        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully retrieved",
                    "result": data}

        logger.info(data)

        return Response(response)
