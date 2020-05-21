# AWS authentication CLI

## Project

I know there is a planty tools to do the aws cli authentication with MFA that exist, but i wanted to try to code that.
The tools read the aws credentials file (if exist) and return a list of your differents profile available.

You can chose your profile and then enter your aws username and your token code.

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
