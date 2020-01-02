# -*- coding: utf-8 -*-
__author__ = "Haren Lewis"
__copyright__ = "Copyright (©) 2019. Athenas Owl. All rights reserved."
__credits__ = ["Quantiphi Analytics"]

# python dependencies
import uuid
import json
import logging
from bson.objectid import ObjectId

from django.utils import timezone
from django.core.exceptions import ValidationError

from booking.models import RideSchedules

from external_services.google_map_service import GoogleDistanceService

from utils.constant import Constant


class RideScheduleService:
    """
    @Definition:
    This class is used for all ride scheduling realted services.
    """
    log = logging.getLogger(__name__)

    def schedule_ride_reminder(self, user_id, ride_id, email, source, destination, time):
        """
        @Definition:
        This function is used for creating subtext data i.e what appears below a 
        author i.e its comments, time posted
        
        get temp time:
            - add safe 60mins to G_TIME
            - add 30mins Uber Time
            - Minus it from the arrival time to get Temp departuer time
            - Write it to DB for the cron to do its magic

        @params:
        user_id
        ride_id
        email: 
        source:
        destination:
        time:

        @return:
        subtext_dict: subtext_dict contains keys and values of subtext html

        arrival_time_ddtm = datetime.fromtimestamp(arrival_time)
        added_arrival_time_ddtm = arrival_time_ddtm + timedelta(seconds=60*30)
        added_arrival_time_ddtm.timestamp()
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

            return True
        except ValidationError:
            pass
