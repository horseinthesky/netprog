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
	xmlDecoder := xml.NewDecoder(os.Stdin)

	var reInfo rpcReply
	err := xmlDecoder.Decode(&reInfo)
	if err != nil {
		panic(err)
	}

	for _, re := range reInfo.RouteEngineList {
		if re.MastershipState == "master" {
			fmt.Printf("%+v", re)
		}
	}

}
