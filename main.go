package main

import (
	"fmt"
	"os"

	"github.com/bigkevmcd/go-configparser"
	"github.com/manifoldco/promptui"
)

const credentialFile string = "/.aws/credentials"

func main() {
	var home string
	fmt.Println("Auth cli with mfa project")
	home, err := os.UserHomeDir()
	if err != nil {
		fmt.Println("Error: ", err)
		os.Exit(2)
	}

	config, err := configparser.NewConfigParserFromFile(home + credentialFile)
	if err != nil {
		fmt.Println("Error: ", err)
		os.Exit(2)
	}

	prompt := promptui.Select{
		Label: "Select profile",
		Items: config.Sections(),
	}

	_, result, err := prompt.Run()

	if err != nil {
		fmt.Printf("Prompt failed %v\n", err)
		return
	}

	fmt.Printf("You choose %q\n", result)

}
