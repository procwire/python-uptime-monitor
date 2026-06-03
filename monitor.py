import requests
import json
import os
from datetime import datetime

# ==============================
# CONFIGURATION
# ==============================

URLS_TO_MONITOR = [
    "https://example.com",
    "https://api.example.com/health"
]

TIMEOUT_SECONDS = 10
MAX_RETRIES = 2          # Number of retries before treating a site as down
RETRY_DELAY_SECONDS = 3  # Seconds to wait between retries

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
# CHECK WEBSITE (with retries)
# ==============================

def check_website(url):
    last_error = None

    for attempt in range(1 + MAX_RETRIES):
        try:
            response = requests.get(url, timeout=TIMEOUT_SECONDS)

            if response.ok:
                return True, None

            # Some APIs deliberately return non-2xx codes even when healthy.
            # If that applies to your endpoint, you can adjust this check.
            last_error = f"Website issue detected: {url} returned {response.status_code}"

        except requests.exceptions.Timeout:
            last_error = f"Timeout detected for {url}"

        except requests.exceptions.ConnectionError:
            last_error = f"Connection error for {url}"

        except requests.exceptions.SSLError:
            last_error = f"SSL certificate error for {url} — certificate may be expired or invalid"

        except Exception as e:
            last_error = f"Unexpected error for {url}: {e}"

        if attempt < MAX_RETRIES:
            print(f"Attempt {attempt + 1} failed for {url}. Retrying in {RETRY_DELAY_SECONDS}s...")
            import time
            time.sleep(RETRY_DELAY_SECONDS)

    return False, last_error

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
            print(f"ALERT SENT: {error_message}")

        # Website recovered
        elif is_up and previous_status == "DOWN":
            send_alert(f"✅ Incident Resolved: {url} is back online.")
            state[url] = "UP"
            print(f"{url} recovered")

        # No status change
        else:
            print(f"No change for {url} (currently {previous_status})")

    save_state(state)

if __name__ == "__main__":
    main()
