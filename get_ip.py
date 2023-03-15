import requests
import re
from pymongo import MongoClient
from flask import Flask, jsonify, request
import json

app = Flask(__name__)


class MyMongodb:
    def __init__(self, url, mongodatabase, mongocollection):
        self.client = MongoClient(url)
        self.mongodatabase = self.client[mongodatabase]
        self.mongocollection = self.mongodatabase[mongocollection]

    def insertone(self, document):
        return self.mongocollection.insert_one(document)

    def find_and_insert(self, document):
        f = self.mongocollection.find_one(document)
        if f is None:
            self.mongocollection.insert_one(document)
        else:
            pass

    def findone(self, document):
        f = self.mongocollection.find_one(document)
        if f is not None:
            return 1  # return 1 if find f
        else:
            return 0  # return 0 if not find f


mongodb = MyMongodb("mongodb://admin:admin@localhost:27017/", "ip_blacklist", "ip_ver1")

# open feeds.json to get urls
filename = "feeds.json"
with open(filename) as f:
    data = json.load(f)
urls = []
for feed in data["feeds"]:
    urls.append(feed["url"])
# urls = [
#     "https://www.spamhaus.org/drop/drop.txt",
#     "http://rules.emergingthreats.net/blockrules/compromised-ips.txt",
#     "https://www.spamhaus.org/drop/edrop.txt",
#     "http://www.blocklist.de/lists/bruteforcelogin.txt",
#     "http://dragonresearchgroup.org/insight/sshpwauth.txt", # url not found
# ]
# print(urls)


@app.route("/insert_ip", methods=["post"])
def insert_ip():
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

    return jsonify("inserted successful")


@app.route("/check_ip", methods=["post"])
def check_ip():
    ip = request.json.get("ip")
    f = mongodb.findone({"ip": ip})
    if f ==0:
        res = jsonify("Do not in blacklist")
        res.status_code = 200
    else:
        res = jsonify("blacklist")
        res.status_code = 200

    return res


@app.route("/check_my_ip", methods=["post"])
def check_my_ip():
    PROXY_CHECK_URL = "https://branchup.pro/whatsmyip.php"
    data = requests.get(PROXY_CHECK_URL)
    myip = data.text.splitlines()
    myip = myip[0].split(":")[1].strip('"{}')

    # find in mongodb blacklist
    f = mongodb.findone({"ip": myip})

    # find in tor
    tor = requests.get("https://check.torproject.org/exit-addresses")
    for ip_tor in tor.text.splitlines():
        ip_tor = ip_tor.replace("\n", "")
        if "ExitAddress" in ip_tor:
            ip_tor = ip_tor.split(" ")[1]
            #    print(ip_tor)
            if myip == ip_tor:
                success = 1  # success = 1 if find ip in tor list
                break
            else:
                success = 0  # success = 0 if not

    # condition for your ip, f is blacklist condition  and success is tor condition
    if f == 0 and success == 0:
        res = "==> It's NOT a TOR exit node and NOT in blacklist"

    elif f == 1 and success == 0:
        res = "==> It's NOT a TOR exit node and in blacklist"

    elif f == 0 and success == 1:
        res = "==> It's a TOR exit node and NOT in blacklist"

    else:
        res = "==> It's a TOR exit node and in blacklist"

    return jsonify("[+] Your public Ip: " + myip + " " + res), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5008, debug=True)
