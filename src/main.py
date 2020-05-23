import os
from pathlib import Path

import click
from src.cmd.generate import execute

AWS_PROFILE_FILE = f"{str(Path.home())}/.aws/credentials"


@click.group()
# @click.option("--debug", is_flag=True)
def run():
    pass
    # if debug:
    #     os.environ["LOGS_LVL"] = "10"
    # logger = logs.get_logger(__name__, os.getenv("LOGS_LVL", "20"))
    # if os.environ.get("LOGS_LVL") is not None:
    #     logger.warning("Be careful !! Logs have been set to DEBUG. Sensitive information may be displayed.")


@run.command(help="Generate temporary token")
@click.option(
    "-p",
    "--profile",
    default=lambda: os.environ.get("AWS_PROFILE"),
    required=True,
    help="AWS profile to use",
)
@click.option("-u", "--user", required=True, help="AWS user name")
@click.option("-t", "--token", required=True, help="MFA Token")
def generate(profile, user, token):
    execute(AWS_PROFILE_FILE, profile, user, token)


@run.command(help="Check access key age")
@click.option("--test", help="This is a test")
def check(test):
    pass


@run.command(help="Perform access key rotation")
def rotate():
    pass
