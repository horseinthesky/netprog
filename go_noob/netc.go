package main

import (
	"encoding/xml"
	"flag"
	"fmt"
	// "reflect"

	"github.com/Juniper/go-netconf/netconf"
)

var (
	user = flag.String("u", "root", "User name")
	pass = flag.String("ps", "", "Password")
	host = flag.String("h", "", "Host")
	port = flag.Int("p", 22, "Port")
)

type RouteEngine struct {
	MastershipState string `xml:"route-engine-information>route-engine>mastership-state"`
	Idle            string `xml:"route-engine-information>route-engine>cpu-idle3"`
}

func main() {
	flag.Parse()

	config := netconf.SSHConfigPassword(*user, *pass)

	addr := fmt.Sprintf("%s:%d", *host, *port)
	conn, err := netconf.DialSSH(addr, config)
	if err != nil {
		panic(err)
	}
	defer conn.Close()

	reply, err := conn.Exec(netconf.RawMethod("<get-route-engine-information/>"))
	if err != nil {
		panic(err)
	}

	var re RouteEngine

	err = xml.Unmarshal([]byte(reply.RawReply), &re)
	if err != nil {
		panic(err)
	}
	fmt.Println(re)
}
