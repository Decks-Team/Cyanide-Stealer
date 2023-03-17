from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from lib import keyauth

keyAuth = keyauth.Keyauth("cyanide", "1ELEEIPBpf")
keyAuth.init()

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": ["http://localhost:8080", "http://127.0.0.1:3000"]}})

@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    r = keyAuth.login(username, password, None)

    if not r["success"]:
        return jsonify({'error': r["message"]}), 401

    return r

if __name__ == '__main__':
    app.run(port=8080)
