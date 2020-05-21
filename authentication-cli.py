import configparser
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

import profileMgt
import accessMgt
import menu
from config import logs, args
import re
import os

AWS_PROFILE_FILE = f"{str(Path.home())}/.aws/credentials"

args = args.get_args()

if args.debug:
    os.environ["LOGS_LVL"] = "10"

logger = logs.get_logger(__name__, os.getenv("LOGS_LVL", "20"))
if os.environ.get("LOGS_LVL") is not None:
    logger.warning(
        "Be careful !! Logs have been set to DEBUG. Sensitive information may be displayed."
    )


def get_sesion_token(sts, user_name, user_token):
    try:
        identity_response = sts.get_caller_identity()
    except ClientError as error:
        logger.error(f"{error}")
        raise error
    try:
        response = sts.get_session_token(
            SerialNumber=f"arn:aws:iam::{identity_response['Account']}:mfa/{user_name}",
            TokenCode=user_token,
        )
    except ClientError as error:
        logger.error(f"{error}")
        raise error
    return response


if __name__ == "__main__":
    logger.debug(f"AWS credentials file set to: {AWS_PROFILE_FILE}")
    logger.debug("Creating config parser")
    config = configparser.ConfigParser()
    config.read(AWS_PROFILE_FILE)

    if args.profile is not None and config.has_section(args.profile):
        logger.debug(f"Profile args: {args.profile}")
        profile = args.profile
        print(f"Profile selected: {profile}")
    else:
        profile = menu.start(config)
    logger.debug("Creating AWS session")
    session = boto3.session.Session(profile_name=profile)

    if args.user is None:
        user_name = input("Enter your AWS user name:\n")
    else:
        user_name = args.user
        print(f"User name:{user_name}")
    logger.debug(f"UserName: {user_name}")

    if args.token is not None and re.match(args.token, r"\d{6}"):
        user_token = args.token
    else:
        user_token = input("Token:\n")

    logger.debug("Getting sts client")
    sts = session.client("sts")
    credentials = get_sesion_token(sts, user_name, user_token)
    logger.debug(f"Credentials response: {credentials}")
    profileMgt.write(AWS_PROFILE_FILE, profile, config, credentials)
    print(
        f"Profile [{profile}-tmp] has been updated and will expire on {credentials['Credentials']['Expiration']}"
    )
    accessMgt.check(config, user_name, profile, AWS_PROFILE_FILE)
