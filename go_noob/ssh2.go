package main

import (
	"flag"
	"fmt"

	"github.com/Juniper/go-netconf/netconf"
	"golang.org/x/crypto/ssh"
)

var (
	user = flag.String("u", "root", "User name")
	pass = flag.String("ps", "", "Password")
	host = flag.String("h", "", "Host")
	port = flag.Int("p", 22, "Port")
)

func main() {
	flag.Parse()

	config := &ssh.ClientConfig{
		User: *user,
		Auth: []ssh.AuthMethod{
			ssh.Password(*pass),
		},
		HostKeyCallback: ssh.InsecureIgnoreHostKey(),
	}

	addr := fmt.Sprintf("%s:%d", *host, *port)
	client, err := ssh.Dial("tcp", addr, config)
	if err != nil {
		panic(err)
	}

	session, err := client.NewSession()
	if err != nil {
		panic(err)
	}
	defer session.Close()

	b, err := session.CombinedOutput("uname -a")
	if err != nil {
		panic(err)
	}
	fmt.Print(string(b))
}
