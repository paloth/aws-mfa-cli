from datetime import datetime, timedelta

import boto3
from botocore.exceptions import ClientError
from dateutil.tz import tzutc

import profileMgt
from config import logs

logger = logs.get_logger(__name__)
"""Access Key management"""


def convert_to_date(date_to_convert):
    """Convert the date format """
    try:
        return datetime.strptime(date_to_convert, "%Y-%m-%dT%H:%M:%S")
    except ValueError as error:
        raise error


def is_delta_greater_than_ninety_days(date):
    """
    Check if the delta between the current date and the data date is greater than 90 days
    datetime.datetime(2020, 3, 20, 22, 6, 14, tzinfo=tzutc())}]
    """
    if (
        datetime.now().replace(tzinfo=tzutc(), microsecond=0)
        - date.replace(microsecond=0)
    ) >= timedelta(days=90):
        return True
    else:
        return False


def check(config, user_name, profile, path):
    session = boto3.session.Session(profile_name=f"{profile}-tmp")
    iam = session.client("iam")
    try:
        current_keys = iam.list_access_keys(UserName=user_name)
        logger.debug(
            current_keys["AccessKeyMetadata"][0]["CreateDate"].replace(
                tzinfo=None, microsecond=0
            )
        )
    except ClientError as error:
        logger.error(error)
    for key in current_keys["AccessKeyMetadata"]:
        if is_delta_greater_than_ninety_days(key["CreateDate"]):
            new_key = iam.create_access_key(UserName=user_name)
            logger.debug(f"NewKey {new_key}")
            if profileMgt.update_profile(path, profile, config, new_key):
                try:
                    iam.update_access_key(
                        UserName=user_name,
                        AccessKeyId=key["AccessKeyId"],
                        Status="Inactive",
                    )
                except ClientError as error:
                    logger.error(error)
                logger.info("Your access key is expired and has been updated")
            else:
                return False
        else:
            remaining_days = (
                key["CreateDate"] + timedelta(days=90)
            ) - datetime.now().replace(tzinfo=tzutc())
            logger.debug(f"Remaining days {remaining_days.days}")
            logger.info(f"Your access key will expire in {remaining_days.days} days ")
    return True
