import json
import time
import requests
import logging

from django.conf import settings

# from utils.constant import Constant


class GoogleDistanceService:
    log = logging.getLogger(__name__)

    # Google MAP API
    MAX_DEVIATION = 3600 # 60mins in seconds
    G_DISTANCE_API_ENDPOINT = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={},{}&destinations={},{}&key={}'
    FAILED_GMAP_DETAIL_REQUEST_MESSAGE = 'EXCEPTION WHILE REQUESTING GMAP API'

    @staticmethod
    def get_distance_matrix_details(origin_lng, origin_lat, dest_lng, dest_lat, arrival_time=None):
        """
        @Definition:
        This function is used for creating subtext data i.e what appears below a 
        author i.e its comments, time posted

        @params:
        origin_lng:
        origin_lat:
        dest_lng:
        dest_lat:
        arrival_time:

        @return:
        fetch_distance_success: 
        distance_time_estimate: 
        """
        fetch_distance_success = False
        distance_time_estimate = None

        try:
            g_distance_endpoint = GoogleDistanceService.G_DISTANCE_API_ENDPOINT.format(
                origin_lng, origin_lat, dest_lng, dest_lat, settings.G_MAP_API_KEY)

            if arrival_time is not None:
                g_distance_endpoint = '{}&arrival_time={}'.format(g_distance_endpoint, arrival_time)

            res = requests.get(g_distance_endpoint)

            if res.status_code == 200:
                response = res.json()
                print("Response from Google Maps API: ", str(response))
                GoogleDistanceService.log.info(str(response))

                distance_time_estimate = response['rows'][0]['elements'][0]['duration']['value']
                fetch_distance_success = True

        except Exception as e:
            print("Exception from Google Maps API: ", str(e))
            message = GoogleDistanceService.FAILED_GMAP_DETAIL_REQUEST_MESSAGE + '    ' + str(e)
            GoogleDistanceService.log.error(message)

        return fetch_distance_success, distance_time_estimate
