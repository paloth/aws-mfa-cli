import argparse


def get_args():
    parser = argparse.ArgumentParser(
        prog="aws-mfa-cli", description="Manage cli access for aws"
    )

    parser.add_argument("--debug", help="Activate logs debug mode", action="store_true")
    subparser = parser.add_subparsers()
    set_generate_command(subparser)
    set_check_command(subparser)
    return parser.parse_args()


def set_generate_command(subparser):
    generate = subparser.add_parser("generate")
    generate.add_argument("-u", "--user", help="User Name")
    generate.add_argument("-t", "--token", help="User's token")
    generate.add_argument("-p", "--profile", help="Profile to use")


def set_check_command(subparser):
    validate = subparser.add_parser("validate")
    validate.add_argument("--test")
