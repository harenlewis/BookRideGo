from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.db.transaction import atomic
from django.shortcuts import get_object_or_404

from booking.models import RideSchedules
from booking.api.serializers import RideScheduleRequestSerializer

from utils.constant import Constant


class RideScheduleAPIView(APIView):

    @atomic
    def post(self, request, *args, **kwargs):
        """

        """

        try:
            data = {
                Constant.STATUS_CODE: 10000,
                Constant.MESSAGE: Constant.DEFAULT_RESPONSE_MESSAGE,
                Constant.RESULT: {}
            }


            ride_serializer = RideScheduleRequestSerializer(data=request.data)

            if ride_serializer.is_valid():
                email = ride_serializer.validated_data['email']
                source = ride_serializer.validated_data['source']
                destination = ride_serializer.validated_data['destination']
                time = ride_serializer.validated_data['time']

        except Exception as error:
            self.log.error(traceback.format_exc().replace(
                Constant.ENTER, Constant.SPACE))

        finally:
            return Response(data, status=status.HTTP_200_OK, headers=None)
