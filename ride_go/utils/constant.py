

class Constant:
    '''
    Constant is class used to store all string literals
    '''
    INI_FILE_PATH = '/var/.ao/config_parameters.ini'
    DEFINITION = 'DEFINITION'
    SECTION = 'SECTION'
    STAGE = 'STAGE'
    LOCAL_LOCATION_OF_LOG = '/tmp/log_files/'

    # Uber API 
    UBER_API_ENDPOINT = 'https://rr1iky5f5f.execute-api.us-east-1.amazonaws.com/api/estimate/time?start_longitude={}&start_latitude={}'
    RIDE_NAME = 'uberGO'

    FAILED_RIDE_DETAIL_REQUEST_MESSAGE = 'EXCEPTION WHILE REQUESTING UBER API'

    # Google MAP API
    G_DISTANCE_API_ENDPOINT = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={},{}&destinations={},{}&key={}/'

    # request constants
    STATUS_CODE = 'status_code'
    MESSAGE = 'message'
    RESULT = 'result'
    DEFAULT_RESPONSE_MESSAGE = 'Something went wrong!'
    RIDE_SCHEDULE_SUCCESS_MESSAGE = 'Remider set successfully!'
    DB_DOWN_MESSAGE = 'Could not connect to the database!'
    API_SUCCESS_MESSAGE = 'API successfully worked'
