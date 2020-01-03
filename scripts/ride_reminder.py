import json
import boto3
import logging
import datetime
import configparser
from mongoengine import *
import logging.handlers as handlers

from django.conf import settings

from utils.constant import Constant

from booking.models import RideSchedules, GeoCords


class RideReminderCronJob:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # create a file handler
    handler = logging.FileHandler(Constant.LOCAL_LOCATION_OF_LOG)
    handler = handlers.TimedRotatingFileHandler(Constant.LOCAL_LOCATION_OF_LOG, when='midnight', interval=1, backupCount=10)
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
    mongoengine.connect(host=MONGO_HOST)

    ACCESS_KEY = config.get(stage, 'AWS_ACCESS_KEY')
    SECRET_KEY = config.get(stage, 'AWS_SECRET_KEY')

    self.aws_client = boto3.client(
        'lambda',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )

    def invoke_cron(self):
        try:
            msg_bytes = json.dumps({ 
                "receiver": "harenlewis@gmail.com", 
                "subject": "Reminder - To book an Uber", 
                "message": "" 
            }).encode('utf-8')

            lambda_resp = (client
                            .invoke(
                                FunctionName='ride_reminder_mailer', 
                                InvocationType='Event', 
                                Payload=msg_bytes
                            )
                           )
        except Exception as e:
            RideReminderCronJob.logger.error(e)
            print(e)

if __name__ == '__main__':
    RideReminderCronJob().invoke_cron()
