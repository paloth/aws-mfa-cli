package main

import (
	"fmt"
	"os"

	"github.com/bigkevmcd/go-configparser"
)

const credentialFile string = "/.aws/credentials"

func main() {
	var home string
	fmt.Println("Auth cli with mfa project")
	home, err := os.UserHomeDir()
	if err != nil {
		fmt.Println("Error while get the home folder")
		os.Exit(2)
	}

	config, err := configparser.NewConfigParserFromFile(home + credentialFile)
	if err != nil {
		fmt.Println("Error while get the aws profiles")
		os.Exit(2)
	}
	fmt.Println(config.Sections())
}
