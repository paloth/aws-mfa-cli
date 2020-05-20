import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", help="User Name")
    parser.add_argument("-t", "--token", help="User's token")
    parser.add_argument("-p", "--profile", help="Profile to use")
    parser.add_argument("--debug", help="Activate logs debug mode", action="store_true")
    return parser.parse_args()
