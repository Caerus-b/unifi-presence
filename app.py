from flask import Flask, jsonify
import requests
import time
import os

# Read from environment variables from docker
UNIFI_URL = os.getenv("UNIFI_URL")
USERNAME = os.getenv("UNIFI_USER")
PASSWORD = os.getenv("UNIFI_PASS")
API_KEY = os.getenv("UNIFI_KEY")
DEVICE_MAC = os.getenv("DEVICE_MAC")

app = Flask(__name__)
session = requests.Session()
session.verify = False  # ignore SSL warnings for self-signed certs

def login():
    payload = {"username": USERNAME, "password": PASSWORD}
    r = session.post(f"{UNIFI_URL}/api/login", json=payload)
    r.raise_for_status()
    print("Logged in to UniFi controller.")

def is_phone_connected():
    try:
        r = session.get(f"{UNIFI_URL}/proxy/network/api/s/default/stat/sta")
        if r.status_code == 401:  # session expired
            login()
            r = session.get(f"{UNIFI_URL}/proxy/network/api/s/default/stat/sta")

        clients = r.json().get("data", [])
        for client in clients:
            if client.get("mac", "").lower() == PHONE_MAC.lower():
                return True
        return False
    except Exception as e:
        print("Error checking UniFi:", e)
        return False

@app.route("/presence")
def presence_api():
    return jsonify({
        "phone_nearby": is_phone_connected(),
        "timestamp": int(time.time())
    })

if __name__ == "__main__":
    login()
    app.run(host="0.0.0.0", port=5000)
