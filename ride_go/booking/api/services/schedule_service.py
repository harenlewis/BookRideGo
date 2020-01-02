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

# from .applications_detail_service import ApplicationsWebservice

from utils.constant import Constant


class RideScheduleService:
    """
    @Definition:
    This class is used for all ride scheduling realted services.
    """
    log = logging.getLogger(__name__)

    def schedule_ride_reminder(self, email, source, destination, time):
        """
        @Definition:
        This function is used for creating subtext data i.e what appears below a author i.e its comments, time posted

        @params:
        email: 
        source:
        destination:
        time:

        @return:
        subtext_dict: subtext_dict contains keys and values of subtext html
        """
        try:
            return True
        except ValidationError:
            pass
