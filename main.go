package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/awserr"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/sts"
	"github.com/bigkevmcd/go-configparser"
	"github.com/manifoldco/promptui"
)

const (
	credentialFile string = "/.aws/credentials"
)

func main() {
	var (
		home        string
		profileList []string
		userChoice  string
		userName    string
		token       string
	)

	fmt.Println("Auth cli with mfa project")

	getHomeValue(&home)

	config, err := configparser.NewConfigParserFromFile(home + credentialFile)
	if err != nil {
		fmt.Println("Error: ", err)
		os.Exit(2)
	}

	profileList = removeBadProfile(config)
	getProfileList(profileList, &userChoice)
	getUserEntry(&userName, &token)

	session := callAwsSession(userChoice, userName, token)

	writeConfigFile(config, userName, home, &session)

	fmt.Println("The profile " + userChoice + "-tmp has set up and will expire on " + session.Credentials.Expiration.Format("Mon Jan 2") + " at " + session.Credentials.Expiration.Format("15:04:05"))
}

func getHomeValue(h *string) {
	var err error
	*h, err = os.UserHomeDir()
	if err != nil {
		fmt.Println("Error: ", err)
		os.Exit(2)
	}
}

func removeBadProfile(list *configparser.ConfigParser) []string {
	var listProfile []string
	for i := 0; i < len(list.Sections()); i++ {
		flag, err := list.HasOption(list.Sections()[i], "aws_access_key_id")
		if flag == true && !strings.HasSuffix(list.Sections()[i], "-tmp") {
			listProfile = append(listProfile, list.Sections()[i])
		}
		if err != nil {
			fmt.Println(err)
		}
	}
	return listProfile
}

func getProfileList(list []string, choice *string) {
	var err error
	prompt := promptui.Select{
		Label: "Select profile",
		Items: list,
	}

	_, *choice, err = prompt.Run()
	if err != nil {
		fmt.Printf("Prompt failed %v\n", err)
		os.Exit(2)
	}

	fmt.Printf("You choose %q\n", *choice)
}

func getUserEntry(usrname *string, token *string) {
	scanner := bufio.NewScanner(os.Stdin)
	for *usrname == "" {
		fmt.Println("Enter your aws username: ")
		scanner.Scan()
		*usrname = scanner.Text()
	}
	for *token == "" {
		fmt.Println("Enter your token: ")
		scanner.Scan()
		*token = scanner.Text()
	}
}

func callAwsSession(choice string, user string, token string) sts.GetSessionTokenOutput {
	var err error
	awsSession, err := session.NewSessionWithOptions(session.Options{
		Profile: choice,
	})
	if err != nil {
		if awsErr, ok := err.(awserr.Error); ok {
			fmt.Println(awsErr)
		}
	}
	svcSts := sts.New(awsSession)

	identity, err := svcSts.GetCallerIdentity(&sts.GetCallerIdentityInput{})
	if err != nil {
		if awsErr, ok := err.(awserr.Error); ok {
			fmt.Println(awsErr)
		}
	}

	tmpSession, err := svcSts.GetSessionToken(&sts.GetSessionTokenInput{
		DurationSeconds: aws.Int64(43200),
		SerialNumber:    aws.String("arn:aws:iam::" + *identity.Account + ":mfa/" + user),
		TokenCode:       aws.String(token),
	})
	if err != nil {
		if awsErr, ok := err.(awserr.Error); ok {
			fmt.Println(awsErr)
		}
	}
	return *tmpSession
}

func writeConfigFile(file *configparser.ConfigParser, profileName string, homePath string, session *sts.GetSessionTokenOutput) {
	var err error

	if exists := file.HasSection(profileName + "-tmp"); exists {
		file.Set(profileName+"-tmp", "aws_access_key_id", *session.Credentials.AccessKeyId)
		file.Set(profileName+"-tmp", "aws_secret_access_key", *session.Credentials.SecretAccessKey)
		file.Set(profileName+"-tmp", "aws_session_token", *session.Credentials.SessionToken)
		file.Set(profileName+"-tmp", "aws_default_region", "eu-west-1")
	} else {
		fmt.Println("Profile " + profileName + "-tmp does not exists.")
		file.AddSection(profileName + "-tmp")
		fmt.Println("Profile " + profileName + "-tmp has been created.")
		file.Set(profileName+"-tmp", "aws_access_key_id", *session.Credentials.AccessKeyId)
		file.Set(profileName+"-tmp", "aws_secret_access_key", *session.Credentials.SecretAccessKey)
		file.Set(profileName+"-tmp", "aws_session_token", *session.Credentials.SessionToken)
		file.Set(profileName+"-tmp", "aws_default_region", "eu-west-1")
	}

	err = file.SaveWithDelimiter(homePath+credentialFile, "=")
	if err != nil {
		fmt.Println(err)
	}
}
