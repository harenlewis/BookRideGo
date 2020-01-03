from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from booking.models import RideSchedules
from booking.api.serializers import RideScheduleRequestSerializer
from booking.api.services.schedule_service import RideScheduleService

from utils.constant import Constant


class RideScheduleAPIView(APIView):
    """
    @Definition:
    This class is used for ride schedule api's
    """
    def post(self, request, *args, **kwargs):
        """
        @Definition:
        Handles post request to this view

        @params:
        request: Django request object

        @return:
        status_code: hhtp custom status code.
        message: Appropriate message to the user
        result: {}
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
                arrival_time = ride_serializer.validated_data['arrival_time']

                user_id = kwargs.get('user_id', None)
                ride_id = kwargs.get('ride_id', None)

                RideScheduleService().schedule_ride_reminder(
                    user_id, ride_id, email, source,
                    destination, arrival_time
                )

                data[Constant.MESSAGE] = Constant.RIDE_SCHEDULE_SUCCESS_MESSAGE
                data[Constant.STATUS_CODE] = 200
            else:
                data[Constant.RESULT] = ride_serializer.errors
                data[Constant.MESSAGE] = "Improper request!"
        except Exception as error:
            self.log.error(traceback.format_exc().replace(
                Constant.ENTER, Constant.SPACE))
            data[Constant.MESSAGE] = str(error)
        finally:
            return Response(data, status=status.HTTP_200_OK, headers=None)
