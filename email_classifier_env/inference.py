import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

print("[START]")

# RESET
res = requests.post(f"{API_BASE_URL}/reset", json={
    "episode_id": "test-1",
    "seed": 42
})

try:
    data = res.json()
except:
    print("RESET ERROR:", res.text)
    exit()

print("RESET:", data)

done = data.get("done", False)
step_count = 0

while not done and step_count < 10:
    obs = data.get("observation", {})
    email = obs.get("current_email")

    if email is None:
        done = True
        continue

    subject = email["subject"].lower()

    # ✅ smart agent
    if "win" in subject:
        action_payload = {
            "action": {
                "action_type": "classify",
                "email_id": email["id"],
                "value": "spam"
            }
        }
    else:
        action_payload = {
            "action": {
                "action_type": "classify",
                "email_id": email["id"],
                "value": "important"
            }
        }

    print(f"[STEP] {action_payload}")

    res = requests.post(f"{API_BASE_URL}/step", json=action_payload)

    try:
        data = res.json()
        print("STEP:", data)
    except:
        print("STEP ERROR:", res.text)
        break

    done = data.get("done", False)
    step_count += 1

print("[END]")