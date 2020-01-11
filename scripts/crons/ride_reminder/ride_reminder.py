
import json
import boto3
import logging
from datetime import datetime, timedelta

import configparser
from mongoengine import *
import logging.handlers as handlers

from ride_go.utils.constant import Constant

from ride_go.booking.models import RideSchedules, GeoCords


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
            
            current_utc_ts = datetime.utcnow()
            upper_limit_ts = current_utc_ts + timedelta(seconds=3600)

            to_process_reminders = (RideSchedules
                                        .objects(
                                            Q(notified=False) & 
                                            Q(to_notify_ts__gte=current_utc_ts) & 
                                            Q(to_notify_ts__lte=upper_limit_ts)
                                        )
                                    )

            for reminder in to_process_reminders:
                print("DOC UUID: ", reminder.uuid)
                to_remind = self.evaluate_reminder(reminder)
                if to_remind:
                    # send an email to the user to book a cab
                    msg_bytes = json.dumps({ 
                        "receiver": "user1@gmail.com", 
                        "subject": "Reminder - To book an Uber", 
                        "message": "" 
                    }).encode('utf-8')

                    lambda_resp = (self.aws_client.client
                                    .invoke(
                                        FunctionName='ride_reminder_mailer',
                                        InvocationType='Event',
                                        Payload=msg_bytes
                                    )
                                )

        except Exception as e:
            RideReminderCronJob.logger.error(e)
            print(e)

    def evaluate_reminder(self, ride_reminf_doc):
        print(ride_reminf_doc.id)
        pass


if __name__ == '__main__':
    RideReminderCronJob().invoke_cron()
