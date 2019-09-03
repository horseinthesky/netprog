package main

import (
	"encoding/xml"
	"flag"
	"fmt"
	"strconv"

	"github.com/Juniper/go-netconf/netconf"
)

var (
	user = flag.String("u", "root", "User name")
	pass = flag.String("ps", "", "Password")
	host = flag.String("h", "", "Host")
	port = flag.Int("p", 22, "Port")
)

type data struct {
	Master  bool
	CpuLoad int64
}

type RouteEngine struct {
	MastershipState string `xml:"route-engine-information>route-engine>mastership-state"`
	Idle            string `xml:"route-engine-information>route-engine>cpu-idle3"`
}

func (r *RouteEngine) transform() data {
	master := r.MastershipState == "master"

	idle, _ := strconv.ParseInt(r.Idle, 10, 64)
	cpuload := 100 - idle

	d := data{
		Master:  master,
		CpuLoad: cpuload,
	}

	return d
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
	result := re.transform()
	fmt.Println(result)
}
