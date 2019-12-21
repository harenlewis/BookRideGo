import json
import time
import requests
import logging

from utils.constant import Constant


class UberRideDeatils:
    log = logging.getLogger(__name__)

    @staticmethod
    def get_ride_details(lng, lat):
        """
        """
        fetch_success = False
        ride_estimate = None

        try:
            uber_endpoint = Constant.UBER_API_ENDPOINT.format(lng, lat)
            res = requests.get(uber_endpoint)

            if res.status_code == 200:
                response = res.json()
                print("Response from UBER API: ", str(response))
                UberRideDeatils.log.info(str(response))

                ride_data = response['times']
                for ride in ride_data:
                    if Constant.RIDE_NAME == 'uberGO':
                        fetch_success = True
                        ride_estimate = ride.get('estimate', None)
                        break
        except Exception as e:
            print("Exception from UBER API: ", str(e))
            message = Constant.FAILED_RIDE_DETAIL_REQUEST_MESSAGE + '    ' + str(e)
            UberRideDeatils.log.error(message)

        return fetch_success, ride_estimate
