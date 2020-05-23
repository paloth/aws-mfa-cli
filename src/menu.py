import subprocess


def filter_profile(config):
    return [
        profile
        for profile in config.sections()
        if not config.has_option(profile, "source_profile")
        and not profile.endswith("-tmp")
    ]


def prompt(config):
    flag = False
    profiles = filter_profile(config)
    while flag is False:
        for index, profile in enumerate(profiles):
            print(f"[{index + 1}] - {profile}\r")
        try:
            user_selection = input(
                "Please select a profile to use to get your temporary credentials:\n"
            )
            while int(user_selection) == 0 or int(user_selection) > len(profiles):
                raise ValueError
        except ValueError:
            subprocess.call("clear")
            print("Bad selection!\nPlease select a profile listed below")
            continue
        flag = True
    print(f"You selected the profile: {profiles[int(user_selection) - 1]}")
    return profiles[int(user_selection) - 1]
