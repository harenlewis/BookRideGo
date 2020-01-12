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


### Solution

The solution to the this problem is divided into two parts

1: When the user sets a reminder (Ride scheduler API)
2: Actually sending out the reminder to the user. (Ride notifier cron)

1) When the user sets the reminder:
   a) We take the arrival time (arrival_ts) from the user.
   b) Find out the safest time to departure for the user, i.e
     safe_dept_ts = arrival_ts - (time_to_travel_ts + uber_ride_estimate_ts + deviation_ts)
     This is the time which is appropriate to send out a notification to the user.
     But this time is not optimal. Hence we write to the DB and store it for processing later. Now, we go to part 2 of the solution.

2) Ride notifier is a cron job which runs every minunte.
   a) It fetches all the ride schedules which have not been notfied yet an fall
      between the current time and current_time + 5 min
   b) It evalutes the schedule ride and validates the time to notify the user. It's working is as below:
        i) Calculate new_notify_time; based on the current map conditions and constant ride
           estimate.
        ii) Evaluation count is the number of times a ride schedule has been processed and notify_ts has been recalculated. If evalution count is 3 we notify the user directly without any checks.
        ii) If new_notfiy_time is less than the current time or the difference is only 20       min between them, then we notify the user and send a email
        iv) Else we save the new_notify_time in DB and increment the evalutaion coutner.

Note: In this entire solution we did not use the Uber API. Valid aussumptions have been made based on user behaviour.
