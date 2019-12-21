import json
import time
import requests
import logging

from utils.constant import Constant


class GoogleDistanceService:
    log = logging.getLogger(__name__)

    @staticmethod
    def get_distance_matrix_details(origin_lng, origin_lat, dest_lng, dest_lat, departure=None):
        """
        """
        fetch_distance_success = False
        ride_estimate = None

        try:
            g_distance_endpoint = Constant.G_DISTANCE_API_ENDPOINT.format(
                origin_lng, origin_lat, dest_lng, dest_lat, settings.G_MAP_API_KEY)

            if departure is not None:
                g_distance_endpoint = '{}&departure_time={}'.format(g_distance_endpoint, departure)
                

            res = requests.get(g_distance_endpoint)

            if res.status_code == 200:
                response = res.json()
                print("Response from Google Maps API: ", str(response))
                GoogleDistanceService.log.info(str(response))

                ride_data = response['times']

        except Exception as e:
            print("Exception from Google Maps API: ", str(e))
            message = Constant.FAILED_RIDE_DETAIL_REQUEST_MESSAGE + '    ' + str(e)
            GoogleDistanceService.log.error(message)

        return fetch_success, ride_estimate
