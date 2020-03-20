import boto3
from botocore.exceptions import ClientError
from os import getenv, environ, name
import subprocess
import configparser


def environment_variables(config):
    if name == "posix":
        home = getenv("HOME")
    elif name == "nt":
        home = getenv("HOMEPATH")
    config.read(f"{home}/.aws/credentials")
    return config.sections()


def create_menu(profile_list):
    flag = False
    while flag is False:
        for index, profile in enumerate(profile_list):
            print(f"[{index + 1}] - {profile}\r")
        try:
            user_selection = input(
                "Please select a profile to use to get your temporary credentials:\n"
            )
            while int(user_selection) == 0 or int(user_selection) > len(profile_list):
                raise ValueError
        except ValueError:
            subprocess.call("clear")
            print(f"Bad selection!\nPlease select a profile listed below")
            continue
        flag = True
    print(f"You selected the profile: {profile_list[int(user_selection) - 1]}")
    environ["AWS_PROFILE"] = profile_list[int(user_selection) - 1]
    return True


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


def write_profile(id_profile, config, credentials):
    if id_profile + "-tmp" not in config:
        config[f"{id_profile}-tmp"] = {}
    config[f"{id_profile}-tmp"]["aws_access_key_id"] = credentials["Credentials"][
        "AccessKeyId"
    ]
    config[f"{id_profile}-tmp"]["aws_secret_access_key"] = credentials["Credentials"][
        "SecretAccessKey"
    ]
    config[f"{id_profile}-tmp"]["aws_session_token"] = credentials["Credentials"][
        "SessionToken"
    ]
    config[f"{id_profile}-tmp"]["aws_default_region"] = "eu-west-1"
    with open("/Users/paul/.aws/credentials2", "w") as configfile:
        config.write(configfile)
    return True


if __name__ == "__main__":
    id_profile = "edf"
    config = configparser.ConfigParser()
    profile_list = environment_variables(config)
    create_menu(profile_list)
    session = boto3.session.Session(profile_name=getenv("AWS_PROFILE"))
    sts = session.client("sts")
    user_name = input("Enter your AWS user name:\n")
    user_token = input("Token:\n")
    credentials = get_sesion_token(sts, user_name, user_token)
    write_profile(id_profile, config, credentials)
    print(
        f"Profile [{id_profile}-tmp] has been updated and will expire on {credentials['Credentials']['Expiration']}"
    )
