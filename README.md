# BookRideGo
-----

## Schedule and set reminders to get notifications for your next ride.

This is a RESTful webservice written in [Django REST framework](https://www.django-rest-framework.org/).

### About the Service

This service will send notifications to the user for him to book a uber to reach his destination according to his arrival time.

### Install dependencies
`pip install -r requirements.txt`

### Webservice Endpoint

| Method |                      Url                       |                            Description |
| ------ | :--------------------------------------------: | -------------------------------------: |
| POST   | api/v1/users/{user_id}/ride/{ride_id}/schedule | Accepts reminder request from the user |



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


### Steps to run the project

1. Clone the respository

    $ `git clone https://github.com/harenlewis/BookRideGo.git`
       `cd ride_go`

 1. Create a virtual envirnoment and activate it.

       `virtualenv -p python3 envname`
        `source envname/bin/active`

 2. Install requirements and dependencies.

       ` pip install -r ../requirements.txt`  

 3. Run server

       `python manage.py runserver`
 
 4. Hit the postman request on the above specified API endpoint with proper request data.
      `localhost:8000/api/v1/users/dd7e4280-e2d6-4de7-b94e-10f777678d78/ride/26546650-e557-4a7b-86e7-6a3942445247/schedule`
      OR
      Use the following curl command:

      `curl --location --request POST 'localhost:8000/api/v1/users/dd7e4280-e2d6-4de7-b94e-10f777678d78/ride/26546650-e557-4a7b-86e7-6a3942445247/schedule' \
--header 'Content-Type: application/json' \
--data-raw '{
    "source": {"lng": 12.927880, "lat": 77.627600},
    "destination": {"lng": 13.035542, "lat": 77.597100},
    "email": "abc@e.com",
    "arrival_time": 1578240000
}'`