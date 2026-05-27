import requests
import json
import os
from datetime import datetime

# ==============================
# CONFIGURATION
# ==============================

URLS_TO_MONITOR = [
    "https://example.com",
    "https://www.procwire.com/null"
]

TIMEOUT_SECONDS = 10

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

STATE_FILE = "monitor_state.json"

# ==============================
# LOAD STATE
# ==============================

def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE, "r") as file:
            return json.load(file)
    except:
        return {}

# ==============================
# SAVE STATE
# ==============================

def save_state(state):
    with open(STATE_FILE, "w") as file:
        json.dump(state, file)

# ==============================
# SEND ALERT
# ==============================

def send_alert(message):
    payload = {
        "content": message
    }
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
    except Exception as e:
        print(f"Failed to send alert: {e}")

# ==============================
# CHECK WEBSITE
# ==============================

def check_website(url):
    try:
        response = requests.get(url, timeout=TIMEOUT_SECONDS)

        if not response.ok:
            return False, f"Website issue detected: {url} returned {response.status_code}"

        return True, None

    except requests.exceptions.Timeout:
        return False, f"Timeout detected for {url}"

    except requests.exceptions.ConnectionError:
        return False, f"Connection error for {url}"

    except Exception as e:
        return False, f"Unexpected error for {url}: {e}"

# ==============================
# MAIN
# ==============================

def main():
    state = load_state()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\nRunning uptime check at {current_time}\n")

    for url in URLS_TO_MONITOR:

        is_up, error_message = check_website(url)

        previous_status = state.get(url, "UP")

        # Website went DOWN
        if not is_up and previous_status == "UP":
            send_alert(f"🚨 Website DOWN: {error_message}")
            state[url] = "DOWN"
            print(error_message)

        # Website recovered
        elif is_up and previous_status == "DOWN":
            send_alert(f"✅ Incident Resolved: {url} is back online.")
            state[url] = "UP"
            print(f"{url} recovered")

        # No status change
        else:
            print(f"No change for {url}")

    save_state(state)

if __name__ == "__main__":
    main()
