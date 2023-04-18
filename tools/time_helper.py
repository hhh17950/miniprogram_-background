import datetime
import time

import pytz


def utc_now():
    return datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)


def utc_now_timestamp():
    return int(utc_now().timestamp())


def timestamp_to_datetime(utc_timestamp):
    return datetime.datetime.utcfromtimestamp(utc_timestamp).replace(tzinfo=pytz.UTC)


def time_str_to_timestamp(time_str: str, time_format: str = "%Y-%m-%dT%H:%M:%SZ"):
    datetime_obj = datetime.datetime.strptime(time_str, time_format).replace(tzinfo=pytz.UTC)
    utc_time = datetime_obj.replace(tzinfo=datetime.timezone.utc)
    timestamp = utc_time.timestamp()
    return timestamp
