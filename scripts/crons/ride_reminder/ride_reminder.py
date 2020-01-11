
import json
import boto3
import logging
from datetime import datetime, timedelta

import configparser
from mongoengine import *
import logging.handlers as handlers

from ride_go.utils.constant import Constant

from ride_go.booking.models import RideSchedules, GeoCords

from ride_go.external_services.google_map_service import GoogleDistanceService
from ride_go.external_services.uber_ride_service import UberRideDeatils


class RideReminderCronJob:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # create a file handler
    ini_file_name = Constant.LOCAL_LOCATION_OF_LOG + 'reminder_cron.log'
    handler = logging.FileHandler(ini_file_name)
    handler = handlers.TimedRotatingFileHandler(ini_file_name, when='midnight', interval=1, backupCount=10)
    handler.setLevel(logging.INFO)
    # create a logging format
    formatter = logging.Formatter('%(levelname)-8s %(asctime)s,%(msecs)d  [%(filename)s:%(lineno)d] %(message)s', "%d-%m-%Y %H:%M:%S")

    handler.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(handler)

    config = configparser.ConfigParser()
    config.read(Constant.INI_FILE_PATH)
    stage = config.get(Constant.DEFINITION, Constant.STAGE)

    MONGO_HOST = config.get(stage, 'MONGO_HOST_URI')
    connect(host=MONGO_HOST)

    ACCESS_KEY = config.get(stage, 'AWS_ACCESS_KEY')
    SECRET_KEY = config.get(stage, 'AWS_SECRET_KEY')
    REGION_NAME = config.get(stage, 'REGION_NAME')

    aws_client = boto3.client(
        'lambda',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION_NAME
    )

    def invoke_cron(self):
        #TODO: This cron is WIP.
        """
        @Definition:
        1) Fetch all the reminders that are current time + 5 mins and which are not yet
           notifed yet
        2) Using this the previous calculated information, query the google map service with
           this departure time.
        3) Evaluate and validate the estimated time from the goole map api and query the
           uber ride api to fetch the ride estimate.
        4) Check for evaluation_count and notify the user.
        4) Irrespective of time left or not trigger the Mailer lambda function.
        """
        try:
            self.current_utc_ts = datetime.now()
            upper_limit_ts = current_utc_ts + timedelta(seconds=3600)

            to_process_reminders = (RideSchedules
                                        .objects(
                                            Q(notified=False)
                                            # & Q(to_notify_ts__gte=current_utc_ts) & 
                                            # Q(to_notify_ts__lte=upper_limit_ts)
                                        )
                                    )

            for reminder in to_process_reminders:
                print("DOC UUID: ", reminder.uuid)
                to_remind = self.evaluate_reminder(reminder)

        except Exception as e:
            RideReminderCronJob.logger.error(e)
            print(e)

    def evaluate_reminder(self, ride_remind_doc):
        start_lng = ride_remind_doc.source['lng']
        start_lat = ride_remind_doc.source['lat']

        dest_lng = ride_remind_doc.destination['lng']
        dest_lat = ride_remind_doc.destination['lat']

        eval_cnt = ride_remind_doc.evaluation_count
        arrival_time_obj = ride_remind_doc.arrival_ts

        if eval_cnt == 2:
            ride_remind_doc.notifed = True
            ride_remind_doc.save()
            self.send_email(self, user_email_id)
            return

        to_notify, notif_ts = (self.validate_time_acc_gmap(
            start_lng, start_lat, dest_lng, dest_lat, arrival_time_obj)
        )

        if not to_notify:
            ride_remind_doc.to_notify_ts = notif_ts
            ride_remind_doc.evaluation_count = eval_cnt + 1
            ride_remind_doc.save()
            return

        fetch_success, ride_estimate = (UberRideDeatils
                                        .get_ride_details(
                                            start_lng, start_lat
                                        )
                                       )

        if to_remind:
            ride_remind_doc.notifed = True
            ride_remind_doc.save()
            self.send_email(self, user_email_id)
    
    def validate_time_acc_gmap(self, source_lng, source_lat, destination_lng, destination_lat, arrival_time):
        to_notify = False
        notif_ts = ''

        arrival_time_ts = arrival_time.timestamp()

        fetch_distance_success, distance_time_estimate = (
                GoogleDistanceService
                .get_distance_matrix_details(
                    source_lng, source_lat,
                    destination_lng, destination_lat,
                    arrival_time_ts
                )
            )

        if not fetch_distance_success:
            to_notify = True

        # new_dept_time = arr time - cur map time
        # if new_dept_time is < currnet time or new_dept_time - current_time is less than 20 min 
        # send notif
        # else
        # update to_notify_ts with new_dept_time and eval count + 1

        new_to_notify_ts = arrival_time_ts - distance_time_estimate
        new_to_notify_ts_obj = datetime.fromtimestamp(new_to_notify_ts)

        safe_departure_ddtm = arrival_time_obj + timedelta(seconds=total_time_deviation_seconds)

        time_diff = new_to_notify_ts_obj - self.current_utc_ts
        if new_to_notify_ts_obj < self.current_utc_ts or time_diff < 20:
            to_notify = True

        to_notify_ts = safe_departure_ddtm

        return to_notify, notif_ts

    def send_email(self, user_email_id):
        if to_remind:
            print("Triggering Lambda mailer!")
            # send an email to the user to book a cab
            msg_json = json.dumps({ 
                "receiver": user_email_id, 
                "subject": "Reminder - To book an Uber", 
                "message": "" 
            })
            msg_bytes = msg_json.encode('utf-8')

            lambda_resp = (self.aws_client
                            .invoke(
                                FunctionName='ride_reminder_mailer',
                                InvocationType='Event',
                                Payload=msg_bytes
                            )
                           )


if __name__ == '__main__':
    RideReminderCronJob().invoke_cron()
