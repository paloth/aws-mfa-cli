import configparser


def get(profile_path):
    config = configparser.ConfigParser()
    config.read(profile_path)
    return config


def write(path, profile, config, credentials):
    if profile + "-tmp" not in config:
        config[f"{profile}-tmp"] = {}
    config[f"{profile}-tmp"]["aws_access_key_id"] = credentials["Credentials"][
        "AccessKeyId"
    ]
    config[f"{profile}-tmp"]["aws_secret_access_key"] = credentials["Credentials"][
        "SecretAccessKey"
    ]
    config[f"{profile}-tmp"]["aws_session_token"] = credentials["Credentials"][
        "SessionToken"
    ]
    config[f"{profile}-tmp"]["aws_default_region"] = "eu-west-1"
    with open(path, "w") as configfile:
        config.write(configfile)


def update_profile(path, profile, config, key):
    config[profile]["aws_access_key_id"] = key["AccessKey"]["AccessKeyId"]
    config[profile]["aws_secret_access_key"] = key["AccessKey"]["SecretAccessKey"]
    config[profile]["aws_default_region"] = "eu-west-1"
    with open(path, "w") as configfile:
        config.write(configfile)
