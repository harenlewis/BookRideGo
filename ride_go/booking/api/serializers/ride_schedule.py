from rest_framework import serializers



class GeoCordsSeriSerializer(serializers.Serializer):
    lng = serializers.FloatField()
    lat = serializers.FloatField()


class RideScheduleRequestSerializer(serializers.Serializer):
    source = GeoCordsSeriSerializer()
    destination = GeoCordsSeriSerializer()
    email = serializers.CharField(max_length=256)
    arrival_time = serializers.IntegerField()

    # def validate_time(self, value):
    #     """
    #     Check if time is greater than current or else raise error.
    #     """
    #     import pdb; pdb.set_trace()
    #     if value['not_valid']:
    #         raise serializers.ValidationError("Not valid")
    #     return value
