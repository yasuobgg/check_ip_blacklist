# app lib
from sanic import Sanic
from sanic import json as sanic_json
from sanic_cors import CORS

# local lib
from ip_and_mongo import MyMongodb, ip_checker, my_ip
from find_bad_ip import find_bad_ip, find_tor_node

app = Sanic(__name__)
CORS(app)

mongodb = MyMongodb("mongodb://admin:admin@localhost:27017/", "ip_blacklist", "ip_ver1")

@app.route("/insert_ip", methods=["post"])
def insert_ip(request):
    find_bad_ip()
    return sanic_json("inserted successful")


@app.route("/check_ip", methods=["post"])
def check_ip(request):

    ip = request.json.get("ip")

    check = ip_checker(ip)

    f = mongodb.findone({"ip": ip})
    if f == 0:
        res = "Do not in blacklist"
    else:
        res = "blacklist"
    return sanic_json(
        {
            "Your input ip": ip,
            "Is valid": check.is_valid(),
            "Is public or private": check.is_private(),
            "Type": res,
        }
    )


@app.route("/check_my_ip", methods=["post"])
def check_my_ip(request):
    public_ip = my_ip.mypublicip()  # lay public ip address
    private_ip = my_ip.myprivateip()  # lay private ip address

    check_ip = ip_checker(public_ip)  # khoi tao class ip_checker

    f = mongodb.findone({"ip": public_ip})  # find in mongodb blacklist

    tor = find_tor_node(public_ip)  # find in tor

    # condition for your public ip
    if f == 0 and tor == 0:
        res = "It's NOT a TOR exit node and NOT in blacklist"
    elif f == 1 and tor == 0:
        res = "It's NOT a TOR exit node and in blacklist"
    elif f == 0 and tor == 1:
        res = "It's a TOR exit node and NOT in blacklist"
    else:
        res = "It's a TOR exit node and in blacklist"

    return sanic_json(
        {
            "Your public ip": public_ip,
            "Your private ip": private_ip,
            "Is valid ip": check_ip.is_valid(),
            "Is public or private": check_ip.is_private(),
            "Type": res,
        }, status=200
    )
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5008, debug=True, auto_reload=True)
