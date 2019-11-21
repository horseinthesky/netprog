package main

import (
	"encoding/xml"
	"fmt"
	"os"
)

type routeEngine struct {
	Status          string `xml:"status"`
	MastershipState string `xml:"mastership-state"`
	CPUIdle         int    `xml:"cpu-idle"`
	CPUTemperature  struct {
		Celsius float32 `xml:"celsius,attr"`
		Textual string  `xml:",chardata"`
	} `xml:"cpu-temperature"`
	StartTime struct {
		Seconds int    `xml:"seconds,attr"`
		Textual string `xml:",chardata"`
	} `xml:"start-time"`
}

type rpcReply struct {
	RouteEngineList []routeEngine `xml:"route-engine-information>route-engine"`
}

func main() {
	file, err := os.Open("1re.xml")
	if err != nil {
		panic(err)
	}

	xmlDecoder := xml.NewDecoder(file)

	var reply rpcReply
	err = xmlDecoder.Decode(&reply)
	if err != nil {
		panic(err)
	}

	for _, re := range reply.RouteEngineList {
		if re.MastershipState == "master" {
			fmt.Printf("%+v", re)
		}
	}

}
