import json
import requests
import re
from ip_and_mongo import MyMongodb

mongodb = MyMongodb("mongodb://admin:admin@localhost:27017/", "ip_blacklist", "ip_ver1")

def find_bad_ip():
    # open file feeds.json, lay truong feeds['url']
    filename = "feeds.json"
    with open(filename) as f:
        data = json.load(f)
    urls = []
    for feed in data["feeds"]:
        urls.append(feed["url"])

    for url in urls:
        try:
            response = requests.get(url)
            data = response.text

            # Use regular expressions to extract the IP addresses, for web that contains both ip address and text
            ip_pattern = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,3}")
            ips = ip_pattern.findall(data)

            # extracted IP addresses
            for ip in ips:
                ip = ip.split("\t")[0]
                mongodb.find_and_insert({"ip": ip})
            # print(len(ips))

            if len(ips) == 0:  # for web that contains only ip address
                # response = requests.get(url)
                # data = response.text
                ips = data.splitlines()
                for ip in ips:
                    ip = ip.split("\t")[0]
                    mongodb.find_and_insert({"ip": ip})

                # print(len(ips))

        except requests.exceptions.RequestException:
            pass

def find_tor_node(public_ip):
    tor = requests.get("https://check.torproject.org/exit-addresses")
    for ip_tor in tor.text.splitlines():
        ip_tor = ip_tor.replace("\n", "")
        if "ExitAddress" in ip_tor:
            ip_tor = ip_tor.split(" ")[1]
            #    print(ip_tor)
            if public_ip == ip_tor:
                success = 1  # success = 1 if find ip in tor list
                return success
                
            else:
                success = 0  # success = 0 if not
                return success