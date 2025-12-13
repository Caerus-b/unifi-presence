from flask import Flask, jsonify, request
import requests
import time
import os

UNIFI_URL = os.getenv("UNIFI_URL") # e.g https://10.10.10.10:8080
API_KEY = os.getenv("UNIFI_KEY") 
SITE_ID = os.getenv("UNIFI_SITE")
DEVICE_NAME = os.getenv("DEVICE_NAME")
API_HEADER_KEY = os.getenv("API_HEADER_KEY")

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
    

def require_api_key(func):
    # Route decorator
    def wrapper(*args, **kwargs):
        if API_HEADER_KEY:
            key = request.headers.get("X-API-KEY")
            if key != API_HEADER_KEY:
                return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@app.route("/")
@require_api_key
def route():
    return jsonify({
        "device_connected": is_device_live(),
        "timestamp": int(time.time())
    })

if __name__ == "__main__":
    if SITE_ID is None:
        get_site_id()
    app.run(host="0.0.0.0", port=5000)
