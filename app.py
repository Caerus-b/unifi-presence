from flask import Flask, jsonify
import requests
import time
import os

UNIFI_URL = os.getenv("UNIFI_URL") # e.g https://10.10.10.10:8080
API_KEY = os.getenv("UNIFI_KEY") 
SITE_ID = os.getenv("UNIFI_SITE")
DEVICE_NAME = os.getenv("DEVICE_NAME")



app = Flask(__name__)
session = requests.Session()
session.verify = False  # ignore SSL warnings for self-signed certs

headers = {'X-API-KEY': API_KEY}
def get_site_id():
    global SITE_ID
    if SITE_ID is None:
        print("No site ID specified, detecting automatically")
        res = session.get(f"{UNIFI_URL}/proxy/network/integration/v1/sites", headers=headers)
        if res.status_code == 401:  
            print("Failed to authenticate with Unifi Application while grabbing site ID.")
        sites = res.json().get("data", [])
        for site in sites:
            print(f'Found Site: {site.get("name", "")} with ID: {site.get("id", "")}')
        if sites:
            SITE_ID = sites[0].get("id")

def is_device_live():
    try:
        res = session.get(f"{UNIFI_URL}/proxy/network/integration/v1/sites/{SITE_ID}/clients", headers=headers)
        if res.status_code == 401:  
            print("Failed to authenticate with Unifi Application while grabbing clients.")
        clients = res.json().get("data", [])
        for client in clients:
            if client.get("name", "").lower() == DEVICE_NAME.lower():  # Filter response data entries for device name
                return True
        return False
    except Exception as error:
        print("Error checking UniFi:", error)
        return False

@app.route("/")
def route():
    return jsonify({
        "device_connected": is_device_live(),
        "timestamp": int(time.time())
    })

if __name__ == "__main__":
    if SITE_ID is None:
        get_site_id()
    app.run(host="0.0.0.0", port=5000)
