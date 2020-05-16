import boto3
from botocore.exceptions import ClientError
import configparser
from pathlib import Path
import menu
import configuration
import keyManagement

AWS_PROFILE_FILE = f"{str(Path.home())}/.aws/credentials"


def get_sesion_token(sts, user_name, user_token):
    try:
        identity_response = sts.get_caller_identity()
    except ClientError as error:
        print(f"{error}")
        raise error
    try:
        response = sts.get_session_token(
            SerialNumber=f"arn:aws:iam::{identity_response['Account']}:mfa/{user_name}",
            TokenCode=user_token,
        )
    except ClientError as error:
        print(f"{error}")
        raise error
    return response


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(AWS_PROFILE_FILE)
    profile = menu.start(config)
    session = boto3.session.Session(profile_name=profile)

    user_name = input("Enter your AWS user name:\n")
    user_token = input("Token:\n")

    sts = session.client("sts")
    credentials = get_sesion_token(sts, user_name, user_token)
    configuration.write(AWS_PROFILE_FILE, profile, config, credentials)
    print(
        f"Profile [{profile}-tmp] has been updated and will expire on {credentials['Credentials']['Expiration']}"
    )
    keyManagement.check(config, user_name, profile, AWS_PROFILE_FILE)
