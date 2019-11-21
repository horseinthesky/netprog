package main

import (
	"encoding/xml"
	"fmt"
	"os"
)

func main() {
	file, err := os.Open("2re.xml")
	if err != nil {
		panic(err)
	}

	xmlDecoder := xml.NewDecoder(file)

	//xmlDecoder := xml.NewDecoder(os.Stdin)

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
		// ...
	}

	type rpcReply struct {
		RouteEngine []routeEngine `xml:"route-engine-information>route-engine"`
	}

	var reInfo rpcReply
	err = xmlDecoder.Decode(&reInfo)
	if err != nil {
		panic(err)
	}

	for _, re := range reInfo.RouteEngine {
		if re.MastershipState == "master" {
			fmt.Printf("%+v", re)
		}
	}

}
