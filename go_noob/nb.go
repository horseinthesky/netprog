package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	// "os"
	"strings"
)

type device struct {
	name   string
	vendor string
	model  string
	role   string
	// tenant   string
	location string
	ip       string
}

type NetboxResponse struct {
	Results []*struct {
		Name       string `json:"name"`
		DeviceType *struct {
			Manufacturer struct {
				Slug string `json:"slug"`
			} `json:"manufacturer"`
			Slug string `json:"slug"`
		} `json:"device_type"`
		DeviceRole *struct {
			Slug string `json:"slug"`
		} `json:"device_role"`
		// Tenant *struct {
		// 	Slug string `json:"slug"`
		// } `json:"tenant"`
		Site *struct {
			Slug string `json:"slug"`
		} `json:"site"`
		PrimaryIp *struct {
			Address string `json:"address"`
		} `json:"primary_ip"`
	} `json:"results"`
}

func (r *NetboxResponse) getDevices() []device {
	devices := make([]device, 0, len(r.Results))
	for _, d := range r.Results {
		devices = append(devices, device{
			name:   d.Name,
			vendor: d.DeviceType.Manufacturer.Slug,
			model:  d.DeviceType.Slug,
			role:   d.DeviceRole.Slug,
			// tenant:   d.Tenant.Slug,
			location: d.Site.Slug,
			ip:       strings.Split(d.PrimaryIp.Address, "/")[0],
		})
	}

	return devices
}

func main() {
	response, err := http.Get("http://192.168.0.97:32770/api/dcim/devices/")
	if err != nil {
		log.Fatalln(err)
	}

	defer response.Body.Close()

	body, err := ioutil.ReadAll(response.Body)
	if err != nil {
		log.Fatalln(err)
	}

	log.Println(string(body))
	var results NetboxResponse
	if err := json.Unmarshal(body, &results); err != nil {
		panic(err)
	}

	devices := results.getDevices()
	fmt.Printf("%+v", devices)
}
