import re
from botocore.exceptions import ClientError


def token_valid(token):
    return True if re.match(r"\d{6}", token) else False


def get_sesion_token(sts, user_name, user_token):
    try:
        identity_response = sts.get_caller_identity()
    except ClientError as error:
        # logger.error(f"{error}")
        raise error
    try:
        response = sts.get_session_token(
            SerialNumber=f"arn:aws:iam::{identity_response['Account']}:mfa/{user_name}",
            TokenCode=user_token,
        )
    except ClientError as error:
        # logger.error(f"{error}")
        raise error
    return response
