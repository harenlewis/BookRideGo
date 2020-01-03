import uuid
from mongoengine import *
import datetime


class GeoCords(EmbeddedDocument):
    lat = FloatField(required=True)
    lng = FloatField(required=True)


class RideSchedules(Document):
    uuid = UUIDField(binary=False)

    email = EmailField(required=True)
    source = EmbeddedDocumentField(GeoCords)
    destination = EmbeddedDocumentField(GeoCords)

    notified = BooleanField(default=False)

    to_notify_ts = DateTimeField(required=True)

    evalutaion_count = IntField(default=1)

    created_by_id = UUIDField(binary=False)
    created_dttm = DateTimeField(default=datetime.datetime.utcnow)
    updated_dttm = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        "strict": False
    }
