# AWS authentication CLI

## Project

The project will be completly refactored.
I will build a CLI with the click library.

I will add new option:

- generate
  - it will generate a temporary token for your user on aws
  - options:
    - user name
    - token
      - Must match regex: /d{6}
    - profile
      - Must be in the user aws credentials file
      - use default profile if it exists
- check
  - it will check the user current access key and warn if the access key is too old
  - options:
    - user name
    - profile
      - Must be in the user aws credentials file
      - use default profile if it exists
- rotate
  - to rotate the user current access key
  - options:
    - user name
    - profile
      - Must be in the user aws credentials file
      - use default profile if it exists

If the user did not set the profile option, the profile list  will be prompted and he will be able to chose his profile in the list

```text
[1] - profile 1
[2] - profile 2
Please select a profile to use to get your temporary credentials:
2
You selected the profile: profile 2
Enter your AWS user name:
MY_USERNAME
Token:
000000
```

You can use differents arguments like:

| argument  | shortcut | description                                      |
| --------- | -------- | ------------------------------------------------ |
| --help    | -h       | Show this help message and exit                  |
| --user    | -u       | A valid user name on aws                         |
| --token   | -t       | A valid token (Must be 6 digits)                 |
| --profile | -p       | A valid profile present in your .aws/credentials |
| --debug   |          | Activate logs debug mode                         |

Example: `aws-mfa-cli -p MyProfile -u UserName -t 000000`

If one value is not valide in arguments, you will be prompted to enter a valid value

At the end, it will return the temporary credential and will write it into the aws credentials configuration file as `profile-tmp`

## To do list

- [ ] Add more error handling
- [ ] Add a valid CI for test
- [ ] Add test
- [x] Add arguments management
- [ ] Add options
  - [ ] Generate temporary key
  - [ ] Check and renew access key
  - [ ] Show Profile available
