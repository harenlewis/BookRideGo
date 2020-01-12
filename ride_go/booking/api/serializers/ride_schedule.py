from datetime import datetime, timezone, timedelta
from rest_framework import serializers


class GeoCordsSeriSerializer(serializers.Serializer):
    lng = serializers.FloatField()
    lat = serializers.FloatField()


class RideScheduleRequestSerializer(serializers.Serializer):
    source = GeoCordsSeriSerializer()
    destination = GeoCordsSeriSerializer()
    email = serializers.CharField(max_length=256)
    arrival_time = serializers.IntegerField()

    def validate_arrival_time(self, value):
        """
        Check if time is greater than current or else raise error.
        """
        arrival_time_dttm = datetime.fromtimestamp(value, tz=timezone.utc)
        current_dttm = datetime.now(tz=timezone.utc)

        # print("arrival_time_dttm: ", arrival_time_dttm)
        # print("current_dttm: ", current_dttm)

        if arrival_time_dttm < current_dttm:
            raise serializers.ValidationError("Not valid datetime")
        return value
