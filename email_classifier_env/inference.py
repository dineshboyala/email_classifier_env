import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

print("[START]")

# Reset environment
res = requests.post(f"{API_BASE_URL}/reset", json={
    "episode_id": "test-1",
    "seed": 42
})

data = res.json()
done = False

step_count = 0

while not done and step_count < 10:
    obs = data["observation"]
    email = obs["current_email"]

    if email is None:
        break

    subject = email["subject"].lower()

    # 🔥 Simple agent logic
    if "win" in subject:
        action = {
            "action_type": "classify",
            "email_id": email["id"],
            "value": "spam"
        }
    elif "meeting" in subject:
        action = {
            "action_type": "reply",
            "email_id": email["id"],
            "value": "important"
        }
    else:
        action = {
            "action_type": "classify",
            "email_id": email["id"],
            "value": "important"
        }

    print(f"[STEP] {action}")

    res = requests.post(f"{API_BASE_URL}/step", json=action)
    data = res.json()

    done = data["done"]
    step_count += 1

print("[END]")