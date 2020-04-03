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

func getHomeValue(h *string) {
	var err error
	*h, err = os.UserHomeDir()
	if err != nil {
		fmt.Println("Error: ", err)
		os.Exit(2)
	}
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

func main() {
	var (
		home        string
		profileList []string
		usrChoice   string
		username    string
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
	getProfileList(profileList, &usrChoice)
	getUserEntry(&username, &token)

	awsSession, err := session.NewSessionWithOptions(session.Options{
		Profile: usrChoice,
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
		SerialNumber:    aws.String("arn:aws:iam::" + *identity.Account + ":mfa/" + username),
		TokenCode:       aws.String(token),
	})
	if err != nil {
		if awsErr, ok := err.(awserr.Error); ok {
			fmt.Println(awsErr)
		}
	}

	if exists := config.HasSection(usrChoice + "-tmp"); exists {
		config.Set(usrChoice+"-tmp", "aws_access_key_id", *tmpSession.Credentials.AccessKeyId)
		config.Set(usrChoice+"-tmp", "aws_secret_access_key", *tmpSession.Credentials.SecretAccessKey)
		config.Set(usrChoice+"-tmp", "aws_session_token", *tmpSession.Credentials.SessionToken)
		config.Set(usrChoice+"-tmp", "aws_default_region", "eu-west-1")
	} else {
		fmt.Println("Profile " + usrChoice + "-tmp does not exists.")
		config.AddSection(usrChoice + "-tmp")
		fmt.Println("Profile " + usrChoice + "-tmp has been created.")
		config.Set(usrChoice+"-tmp", "aws_access_key_id", *tmpSession.Credentials.AccessKeyId)
		config.Set(usrChoice+"-tmp", "aws_secret_access_key", *tmpSession.Credentials.SecretAccessKey)
		config.Set(usrChoice+"-tmp", "aws_session_token", *tmpSession.Credentials.SessionToken)
		config.Set(usrChoice+"-tmp", "aws_default_region", "eu-west-1")
	}
	err = config.SaveWithDelimiter(home+credentialFile, "=")
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("The profile " + usrChoice + "-tmp has set up and will expire at " + tmpSession.Credentials.Expiration.Format("Mon Jan 2 15:04:05"))
}
