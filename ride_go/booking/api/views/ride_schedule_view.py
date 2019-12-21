from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.db.transaction import atomic
from django.shortcuts import get_object_or_404

# from booking.models import RideSchedule
from booking.api.serializers import RideScheduleRequestSerializer


class RideScheduleAPIView(APIView):

    @atomic
    def post(self, request, *args, **kwargs):
        """
        """
        ride_serializer = RideScheduleRequestSerializer(data=request.data)
        import pdb; pdb.set_trace()
        if ride_serializer.is_valid():
            return Response("serializer.data", status=status.HTTP_201_CREATED)
