from pymongo import MongoClient
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

from re import findall
class ip_checker(object):
    def __init__(self, ipaddress):
        self.ip_address = ipaddress.split("/")[0]

    # This method checking wheter the given ip address is valid or not and return str yes or no
    def is_valid(self):
        if not findall(
            "(?i)^(\d|\d\d|1[0-9][0-9]|2[0-9][0-5]).(\d|\d\d|1[0-9][0-9]|2[0-9][0-5]).(\d|\d\d|1[0-9][0-9]|2[0-9][0-5]).(\d|\d\d|1[0-9][0-9]|2[0-9][0-5])$",
            self.ip_address,
        ):
            return str("No")
        else:
            return str("Yes")

    # This method checks whether the given ipaddress is private or public and return str private or public
    def is_private(self):
        if findall(
            "(?i)^192.168.(\d|\d\d|1[0-9][0-9]|2[0-9][0-5]).(\d|\d\d|1[0-9][0-9]|2[0-9][0-5])$",
            self.ip_address,
        ):
            return str("Private")
        elif findall("(?i)^127.\d{1,3}.\d{1,3}.\d{1,3}$", self.ip_address):
            return str("Private")
        elif findall(
            "(?i)^10.(\d|\d\d|1[0-9][0-9]|2[0-9][0-5]).(\d|\d\d|1[0-9][0-9]|2[0-9][0-5]).(\d|\d\d|1[0-9][0-9]|2[0-9][0-5])$",
            self.ip_address,
        ):
            return str("Private")
        elif findall(
            "(?i)^172.(1[6-9]|2[0-9]|3[0-1]).(\d|\d\d|1[0-9][0-9]|2[0-9][0-5]).(\d|\d\d|1[0-9][0-9]|2[0-9][0-5])$",
            self.ip_address,
        ):
            return str("Private")
        else:
            return str("Public")

    # Check if the ip address is public or not
    def is_public(self):
        if self.is_valid() and not self.is_private():
            return True
        else:
            return False

import socket
import requests
class my_ip:
    def __init__(self) -> None:
        pass
    def myprivateip():
        return socket.gethostbyname_ex(socket.gethostname())[2][3]
    def mypublicip():
        PROXY_CHECK_URL = "https://branchup.pro/whatsmyip.php"
        data = requests.get(PROXY_CHECK_URL)  # get public ip address
        myip = data.text.splitlines()
        myip = myip[0].split(":")[1].strip('"{}')  # tach string de lay rieng ip address
        return myip