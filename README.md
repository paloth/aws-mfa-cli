# AWS authentication CLI

## Project

I know there is a planty tools to do the aws cli authentication with MFA that exist, but i wanted to try to code that.
The tools read the aws credentials file (if exist) and return a list of your differents profile available.

You can chose your profile and then enter your aws username and your token code.

```text
[1] - profile 1
[2] - profile 2
[3] - profile 3
[4] - profile-tmp
Please select a profile to use to get your temporary credentials:
2
You selected the profile: profile 2
Enter your AWS user name:
MY_USERNAME
Token:
000000
```

It will return the temporary credential and will write it into the aws credentials configuration file as `profile-tmp`

## To do list

- [ ] Add more error handling
- [ ] Add test
