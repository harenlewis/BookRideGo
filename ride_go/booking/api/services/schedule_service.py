# -*- coding: utf-8 -*-
__author__ = "Haren Lewis"
__copyright__ = "Copyright (©) 2019. Athenas Owl. All rights reserved."
__credits__ = ["Quantiphi Analytics"]

# python dependencies
import uuid
import json
import logging
from bson.objectid import ObjectId
from datetime import datetime, timedelta

from django.utils import timezone
from django.core.exceptions import ValidationError

from booking.models import RideSchedules, GeoCords

from external_services.google_map_service import GoogleDistanceService

from utils.constant import Constant


class RideScheduleService:
    """
    @Definition:
    This class is used for all ride scheduling realted services.
    """
    log = logging.getLogger(__name__)

    def schedule_ride_reminder(self, user_id, ride_id, email, source, destination, arrival_time):
        """
        @Definition:
        This function is used for calculating worst case time for the reminder to 
        be sent to the user and writes it to the DB.
        
        get temp time:
          - add safe 60mins to G_TIME
          - add 30mins Uber Time
          - Minus it from the arrival time to get Temp departure time
          - Write it to DB for the cron to calculate approximate time.

        @params:
        user_id: UUID of requesting user
        ride_id: UUID of ride
        email: User's email
        source: Source location co-ordinates
        destination: Destination location co-ordinates
        time: Arrival time

        @return:
        bool: validates all the dependent services have run successfully.
        """
        try:
            source_lng = source.get('lng', None)
            source_lat = source.get('lat', None)

            destination_lng = destination.get('lng', None)
            destination_lat = destination.get('lat', None)

            fetch_distance_success, distance_time_estimate = (
                GoogleDistanceService
                .get_distance_matrix_details(
                    source_lng, source_lat,
                    destination_lng, destination_lat
                )
            )

            if not fetch_distance_success:
                return fetch_distance_success

            arrival_time_obj = datetime.fromtimestamp(arrival_time)
            total_time_deviation_seconds = distance_time_estimate + Constant.MAX_DEVIATION + Constant.MAX_RIDE_ESTIMATE

            safe_departure_ddtm = arrival_time_obj + timedelta(seconds=total_time_deviation_seconds)

            to_notify_ts = safe_departure_ddtm

            source_cords = GeoCords(
                lng=source_lng,
                lat=source_lat
            )

            destination_cords = GeoCords(
                lng=destination_lng,
                lat=destination_lat
            )

            scheduled_ride_reminder = RideSchedules(
                uuid=ride_id,
                email=email,
                source=source_cords,
                destination=destination_cords,
                to_notify_ts=to_notify_ts,
                created_by_id=user_id
            )

            scheduled_ride_reminder.save()
            return True
        except ValidationError:
            pass
