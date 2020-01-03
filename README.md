# BookRideGo
## Schedule and set reminders to get notifications for your next ride.

This is a RESTful webservice written in [Django REST framework](https://www.django-rest-framework.org/).

### About the Service

This service will send notifications to the user for him to book a uber to reach his destination according to his arrival time.

### Install dependencies
`pip install -r requirements.txt`

### Webservice Endpoint

| Method |                                Url                                 |                        Description |
| ------ | :----------------------------------------------------------------: | ---------------------------------: |
| POST   |                 api/v1/users/{user_id}/ride/{ride_id}/schedule                |                  Accepts reminder request from the user|



Input:
```sh
{
    "source": {"lng": 12.927880, "lat": 77.627600},
    "destination": {"lng": 13.035542, "lat": 77.597100},
    "email": "abc@e.com",
    "arrival_time": 1576958400
}
```

Output:
```sh
{
    "status_code": 200,
    "message": "Remider set successfully!",
    "result": {}
}
```

### Log File Configuration

- All Log Configuration are set in settings.py file
- Location of log files: `/tmp/log_files/ride_go.log`

### System Architecture

![Ride Go V1 System](https://github.com/harenlewis/BookRideGo/blob/development/Ride_GO-Architecture.png?raw=true)