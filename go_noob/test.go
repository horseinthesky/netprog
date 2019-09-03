package main

import (
	"encoding/xml"
	"fmt"
	"io/ioutil"
)

type RouteEngine struct {
	MastershipState string `xml:"rpc-reply>route-engine-information>route-engine>mastership-state"`
	Idle            string `xml:"rpc-reply>route-engine-information>route-engine>cpu-idle3"`
}

func main() {
	file, err := ioutil.ReadFile("test.xml")
	if err != nil {
		panic(err)
	}

	var re RouteEngine
	err = xml.Unmarshal([]byte(file), &re)
	if err != nil {
		panic(err)
	}
	fmt.Println(re)

}
